'''Base class for loaders that create pandas dataframes.'''

# Copyright (c) 2024 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

import abc
import queue
import time
from typing import Any, Dict, Optional, List, Union

import pandas as pd
from sklearn.model_selection import KFold  # type: ignore[import]

from ...config_components.impl.config_component import (
    ConfigError, ValidationErrors, ParsingErrors)
from ...config_components.distributed_config import DistributedConfig
from ...problem_def.task import TaskType
from ...wrangler.constants import JSONKeys
from ...wrangler.dataset import Dataset, Column, RoleName, DatasetKeys
from ...config_components.dataset_config import DatasetFileError

from .data_loader import DataLoader


class Error(BaseException):
    '''Base class for all errors in this file.'''


class ColumnError(Error):
    '''Attempt to select columns in a dataframe that don't exist.'''


class DataframeLoader(DataLoader, metaclass=abc.ABCMeta):
    '''Base class for loaders that create pandas dataframes.'''
    _train_dataset: Dataset
    _que: queue.Queue

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._train_dataset = self._load_train()
        if self._train_dataset is not None:
            self._train_dataset.dataframe = self._str_column_names(self._train_dataset.dataframe)

        self._update_roles()

        self.validate(self._train_dataset, train=True)

        self._que = queue.Queue()
        self._que.put(self._train_dataset)

    def _update_roles(self) -> None:
        '''Give all unassigned columns the Attribute role.'''
        assigned_colnames: List[str] = []
        errors: List[ConfigError] = []

        if self._train_dataset is None:
            return

        for cols in self._metadata.roles.values():
            for col in cols:
                assigned_colnames.append(str(col.name))

        unassigned_colnames = list(
            set(self._train_dataset.dataframe.columns) - set(assigned_colnames))
        unassigned_cols = []
        for colname in unassigned_colnames:
            unassigned_cols.append(Column(colname))

        updated_roles = self._metadata.roles
        if RoleName.ATTRIBUTE not in updated_roles:
            updated_roles[RoleName.ATTRIBUTE] = []
        updated_roles[RoleName.ATTRIBUTE].extend(unassigned_cols)

        self._metadata = self._metadata.override_roles(updated_roles)

        # Because train data is already loaded, we need to update its
        # metadata separately.
        self._train_dataset._metadata = self._metadata  # pylint: disable=protected-access

        if len(errors) != 0:
            raise ParsingErrors(errors)

    def _prune_target(self, retval: Dataset) -> Dataset:
        '''remove target col if it is in data

        called by subclasses in load_test() since test data shouldn't have target

        keep target for forecasting problems
        '''
        # TODO(Merritt/Piggy): once we have a forecasting dataloader, we can
        #   do something more elegant than checking the task type here.

        if self._metadata.task != TaskType.FORECASTING:
            target = self._metadata.target
            if target is not None and target.name in retval.dataframe.columns:
                new_data = retval.dataframe.drop(
                    labels=target.name, axis=1)
                retval.dataframe = new_data

        return retval

    def _str_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = df.columns.astype(str)
        return df

    def _ensure_cols_present(self, df: pd.DataFrame, role: RoleName) -> List[ConfigError]:
        errors: List[ConfigError] = []
        if role in self._metadata.roles:
            for col in self._metadata.roles[role]:
                if col.name not in df.columns:
                    errors.append(DatasetFileError(
                        f'Column {col.name} specified under role {role}'
                        ' not found among columns in dataset. '
                        f'Found: {df.columns}'))
        return errors

    def validate(self, dataset: Optional[Dataset], train: bool = False) -> None:
        '''Raise a ValidationErrors if something about the dataset is inconsistent.'''
        if dataset is None:
            return  # A None dataset is valid.
        errors: List[ConfigError] = []

        if DatasetKeys.DATAFRAME.value in dataset:
            errors.extend(self._ensure_cols_present(dataset.dataframe, RoleName.INDEX))
            if train:
                errors.extend(self._ensure_cols_present(dataset.dataframe, RoleName.ATTRIBUTE))
                errors.extend(self._ensure_cols_present(dataset.dataframe, RoleName.TARGET))
        elif DatasetKeys.GROUND_TRUTH.value in dataset:
            errors.extend(self._ensure_cols_present(dataset.ground_truth, RoleName.INDEX))
            errors.extend(self._ensure_cols_present(dataset.ground_truth, RoleName.TARGET))
        else:
            # Raise error?
            pass

        if len(errors) != 0:
            raise ValidationErrors(errors)

    def load_train(self) -> Optional[Dataset]:
        retval = self._train_dataset
        self.validate(retval, train=True)
        return self._conditional_split(retval)

    @abc.abstractmethod
    def _load_train(self) -> Optional[Dataset]:
        ...

    def load_test(self) -> Optional[Dataset]:
        '''Load test data if it exists, otherwise None'''
        retval = self._load_test()
        if retval is None:
            return None

        retval.dataframe = self._str_column_names(retval.dataframe)

        retval = self._prune_target(retval)
        self.validate(retval)
        # Unlike train data, don't split the test data for a distributed setting.
        return retval

    @abc.abstractmethod
    def _load_test(self) -> Optional[Dataset]:
        ...

    def _load_ground_truth(self) -> Optional[Dataset]:
        '''If the target column exists in the test set, extract it as the ground truth.'''
        test_set = self._load_test()
        if test_set is None:
            print('test set is None')
            return None

        if self._metadata.target is None:
            print('target in metadata is None')

            return None

        target_name = self._metadata.target.name

        if target_name in test_set.dataframe.columns:
            retval = Dataset(metadata=self._metadata)
            retval.ground_truth = test_set.dataframe[[target_name]]
            return retval

        print(f'target name ({target_name}) not in cols ({test_set.dataframe.columns}).')
        return None

    def _dataset(self,
                 data: Any,
                 key: Union[str, DatasetKeys] = DatasetKeys.DATAFRAME,
                 cols: Optional[List[str]] = None,
                 roles: Optional[List[Union[RoleName, str]]] = None,
                 **kwargs) -> Dataset:
        '''Load a Dataset object, by placing data at the supplied key.

        As of 2023-12-04 we only know how to handle things we can turn into a pandas DataFrame.

        Args:
          data:
            Dataframe or object that can be turned into one.
          key:
            The key for the data in the dataset. Defaults to "dataframe".
          cols:
            If set, only selects supplied column(s).
            Will take union with roles if both are specified.
          roles:
            If set, only selects columns with supplied role(s).
            Will take union with cols if both are specified.
        '''

        retval = Dataset(metadata=self._metadata)

        data_df = pd.DataFrame(data)
        data_df = self._str_column_names(data_df)

        # Trim to selected columns if either cols or roles is set.
        cols_to_select = set()
        if cols is not None:
            cols_to_select.update(cols)
        if roles is not None:
            for role in roles:
                if isinstance(role, str):
                    role = RoleName[role.upper()]
                cols_to_select.update(
                    c.name for c in self._metadata.roles[role])
        if cols_to_select:
            if cols_to_select.issubset(data_df.columns):
                data_df = data_df[sorted(cols_to_select)]
            else:
                raise ColumnError(
                    f'selecting columns {cols_to_select} from '
                    f'dataframe with columns {data_df.columns};'
                    'not all requested columns are present.'
                )

        if isinstance(key, str):
            key = DatasetKeys[key.upper()]

        retval[key.value] = data_df
        return retval

    def _conditional_split(self, data: Dataset) -> Dataset:
        '''Split a dataset if we are in a distributed simulation, otherwise do nothing.

        Requires 1 <= my_id <= num_nodes.
        '''
        problem_def = self._config.metadata.problem_def
        if problem_def is None:
            return data

        distributed = problem_def.get_conf('distributed')
        assert isinstance(distributed, DistributedConfig), (
            f'BUG: Expected distributed to be a DistributedConfig, '
            f'got {type(distributed)} instead.'
        )
        distributed_split = distributed.split
        if distributed_split is None:
            return data

        # split data for a distributed simulation
        kfcv = KFold(
            n_splits=distributed_split.num_nodes,
            shuffle=True,
            random_state=distributed_split.seed  # defaults to default seed
        )

        # 1-based: 1 <= my_id <= num_nodes.
        n = distributed.my_id
        # Choose nth split.
        _, indices = next(
            (x for i, x in enumerate(
                kfcv.split(data.dataframe),
                start=1
            ) if i == n), (None, None))
        assert indices is not None, (
            f'BUG: Could not find {n}th split of {distributed_split.num_nodes} '
            f'for node {distributed.my_id}'
        )

        split_df = data.dataframe.iloc[indices]
        split_df.reset_index(inplace=True, drop=True)
        retval = data.output()
        retval.dataframe = split_df
        return retval

    def poll(self, timeout: Optional[float] = 0.0) -> Optional[Dataset]:
        next_data = self._poll(timeout=timeout)
        if next_data is None:
            return None
        next_data.dataframe = self._str_column_names(next_data.dataframe)
        self.validate(next_data)

        return self._conditional_split(data=next_data)

    def _poll(self, timeout: Optional[float] = 0.0) -> Optional[Dataset]:
        '''Return the latest unsplit dataset.'''
        if timeout is not None:
            time.sleep(timeout)
        try:
            return self._que.get(block=False, timeout=timeout)
        except queue.Empty:
            return None

    def build_dataset_from_json(self, json_data: Dict) -> Dataset:
        '''Build a Dataset object from a JSON object.'''
        retval = Dataset(metadata=self._metadata)
        data = json_data[JSONKeys.DATA.value]
        if DatasetKeys.COVARIATES.value in data:
            covariates = pd.DataFrame(data[DatasetKeys.COVARIATES.value])
            retval[DatasetKeys.COVARIATES.value] = covariates
        if DatasetKeys.TARGET.value in data:
            target = pd.DataFrame(data[DatasetKeys.TARGET.value])
            retval[DatasetKeys.TARGET.value] = target
        if DatasetKeys.DATAFRAME.value in data:
            dataframe = pd.DataFrame(data[DatasetKeys.DATAFRAME.value])
            retval[DatasetKeys.DATAFRAME.value] = dataframe
        if DatasetKeys.GROUND_TRUTH.value in data:
            ground_truth = pd.DataFrame(data[DatasetKeys.GROUND_TRUTH.value])
            retval[DatasetKeys.GROUND_TRUTH.value] = ground_truth
        return retval
