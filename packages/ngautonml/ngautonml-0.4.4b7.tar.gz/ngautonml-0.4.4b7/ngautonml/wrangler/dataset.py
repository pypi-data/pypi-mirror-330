'''Holds a dataset.'''

# Copyright (c) 2025 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

from enum import Enum
import copy
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd


from ..config_components.impl.config_component import ConfigComponent
from ..problem_def.task import DataType, TaskType
from ..problem_def.problem_def_interface import ProblemDefInterface
from ..tables.impl.table import Table, TableFactory


def df_to_dict_json_friendly(df: pd.DataFrame) -> Dict:
    '''Same as DataFrame.to_dict(orient='list') but converts NaN to None.'''
    retval = df.replace([np.nan], [None]).to_dict(orient='list')
    return retval


class Error(BaseException):
    '''Base class for all model-related exceptions.'''
    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return self.__class__.__name__ + '(' + ',\n'.join(self.args) + ')'


class DatasetKeyError(Error, KeyError):
    '''Raise when a fit() or predict() method is passed an input dataset
    that is missing required keys.'''


class DatasetValueError(Error, ValueError):
    '''Raise when a dataset has the correct keys but invalid value(s)'''


class MetadataError(Error):
    '''Raise when a dataset is invalid metadata.'''


class RoleName(Enum):
    '''Possible column roles'''
    INDEX = 'index'
    TARGET = 'target'
    ATTRIBUTE = 'attribute'

    # For testing only
    TEST_ROLE = 'test_role'

    # For time series only
    TIME = 'time'
    TIMESERIES_ID = 'timeseries_id'
    PAST_EXOGENOUS = 'past_exogenous'
    FUTURE_EXOGENOUS = 'future_exogenous'


class Column():
    '''Defines a column in a dataset'''
    _name: str

    def __init__(self,
                 name: str):
        self._name = name

    @property
    def name(self) -> str:
        '''The column's name'''
        return str(self._name)

    def __eq__(self, other: Any):
        if not isinstance(other, Column):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return self._name.__hash__()

    def __str__(self) -> str:
        return f'Column({self.name})'

    def __repr__(self) -> str:
        return f'ngautonml.wrangler.dataset.Column ({self.name})'


class DatasetKeys(Enum):
    '''Standard keys used in the Dataset object passed between models'''
    DATAFRAME = 'dataframe'
    TARGET = 'target'
    COVARIATES = 'covariates'
    PREDICTIONS = 'predictions'
    PROBABILITIES = 'probabilities'
    HYPERPARAMS = 'hyperparams'
    GROUND_TRUTH = 'ground_truth'

    # Indicator of an error during fitting a pipeline
    ERROR = 'error'

    # Temporary key for migrating to Tables
    DATAFRAME_TABLE = 'dataframe_table'

    # for time series forecasting only
    STATIC_EXOGENOUS = 'static_exogenous'
    DYNAMIC_EXOGENOUS = 'dynamic_exogenous'

    # for keras image processing only
    KERAS_DS = 'keras_ds'
    KERAS_VALIDATE = 'keras_validate'


class Metadata():
    '''Metadata.'''
    _roles: Dict[RoleName, List[Column]]
    _pos_labels: Dict[RoleName, Any]
    _task: Optional[TaskType]
    _data_type: Optional[DataType]
    _problem_def: Optional[ProblemDefInterface]

    def __init__(self,
                 problem_def: Optional[ProblemDefInterface] = None,
                 roles: Optional[Dict[RoleName, List[Column]]] = None,
                 pos_labels: Optional[Dict[RoleName, Any]] = None,
                 task: Optional[TaskType] = None,
                 data_type: Optional[DataType] = None) -> None:
        self._problem_def = problem_def
        self._roles = roles or {}
        self._pos_labels = pos_labels or {}
        if problem_def is None:
            self._task = task
            self._data_type = data_type
        else:
            self._task = task or problem_def.task.task_type
            self._data_type = data_type or problem_def.task.data_type

    def get_conf(self, config_name: str) -> ConfigComponent:
        '''Get a plugin conf ConfigComponent'''
        assert self._problem_def is not None, 'BUG: _problem_def should be resolved in __init__().'
        return self._problem_def.get_conf(config_name=config_name)

    @property
    def roles(self) -> Dict[RoleName, List[Column]]:
        '''roles maps role names to lists of columns with that role.'''
        return self._roles.copy()

    @property
    def task(self) -> Optional[TaskType]:
        '''Data science task that is being approached with this dataset.'''
        return self._task

    @property
    def data_type(self) -> Optional[DataType]:
        '''Type of data contained in this dataset (image, tabular, etc)'''
        return self._data_type

    @property
    def target(self) -> Optional[Column]:
        '''Get name and index of target column if it exists.'''
        if RoleName.TARGET not in self._roles or len(self._roles[RoleName.TARGET]) == 0:
            return None
        assert len(self._roles[RoleName.TARGET]) <= 1, 'Must have at most 1 target column'
        return self._roles[RoleName.TARGET][0]

    @property
    def pos_labels(self) -> Dict[RoleName, Any]:
        '''maps role names to a positive value for columns with that role'''
        return self._pos_labels.copy()

    def override_roles(self, roles=Dict[RoleName, List[Column]]) -> 'Metadata':
        '''Return a copy of metadata with new roles.'''
        other = copy.deepcopy(self)
        other._roles = roles  # pylint: disable=protected-access
        return other

    @property
    def problem_def(self) -> Optional[ProblemDefInterface]:
        '''Get the problem definition object'''
        return self._problem_def


class Dataset(Dict[str, Any]):
    '''Holds a dataset.
    Allows for arbitrary keys and values as long as the keys are strings.

    Standard keys: covariates, target, dataframe
    '''
    _metadata: Metadata

    def __init__(self,
                 *args,
                 metadata: Optional[Metadata] = None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        if metadata is None:
            metadata = Metadata(roles={}, pos_labels={})
        self._metadata = metadata

    def __str__(self) -> str:
        retval = 'Dataset({'
        for key, val in self.items():
            retval = f'{retval}\'{key}\': {self._str_value(val)}\n'
        retval = retval + '})'
        return retval

    def _str_value(self, value: Any) -> str:
        '''String representation of Dataset values.'''
        if isinstance(value, pd.DataFrame):
            return f'pandas.DataFrame(shape = {value.shape}, head = \n{value.head(5)})'
        return str(value)

    def to_prejson(self) -> Dict[str, Any]:
        '''Represent self as a dict that can be transformed to json.'''
        retval: Dict[str, Any] = {}
        for key, val in self.items():
            retval[key] = self._json_value(val)
        return retval

    def _json_value(self, value: Any) -> Any:
        '''Represent a value as something that can be converted to JSON.'''
        if isinstance(value, pd.DataFrame):
            return df_to_dict_json_friendly(value)
        if isinstance(value, Table):
            return value.as_dict()
        # TODO(Merritt): raise an error?
        return value

    @property
    def roles(self) -> Dict[RoleName, List[Column]]:
        '''Information about column roles in the dataset'''
        return self._metadata.roles

    @property
    def metadata(self) -> Metadata:
        '''Config metadata for use by models'''
        return self._metadata

    @property
    def dataframe(self) -> pd.DataFrame:
        '''Return the dataframe at DatasetKeys.DATAFRAME, or raise an error if it doesn't exist.'''
        if DatasetKeys.DATAFRAME_TABLE.value in self:
            return self.dataframe_table.as_(pd.DataFrame)  # type: ignore[attr-defined]  # pylint: disable=line-too-long

        if DatasetKeys.DATAFRAME.value not in self:
            if DatasetKeys.ERROR.value in self:
                raise DatasetKeyError(
                    f'Attempting to extract key "{DatasetKeys.DATAFRAME.value}" '
                    f'as input, instead found keys {list(self.keys())}. '
                    f'Error: {self[DatasetKeys.ERROR.value]}')
            raise DatasetKeyError(
                f'Attempting to extract key "{DatasetKeys.DATAFRAME.value}" '
                f'as input, instead found keys {list(self.keys())}.')
        df_value = self[DatasetKeys.DATAFRAME.value]
        if not isinstance(df_value, pd.DataFrame):
            raise DatasetValueError(
                f'Input key key {DatasetKeys.DATAFRAME.value} must point to '
                f'a pandas.DataFrame, instead found a {type(df_value)}: '
                f'{df_value}')
        return pd.DataFrame(df_value)

    @dataframe.setter
    def dataframe(self, data: pd.DataFrame) -> None:
        self[DatasetKeys.DATAFRAME.value] = data

    @property
    def dataframe_table(self) -> Table:
        '''Return the dataframe at DatasetKeys.DATAFRAME as a Table.'''
        if DatasetKeys.DATAFRAME_TABLE.value in self:
            return self[DatasetKeys.DATAFRAME_TABLE.value]
        if DatasetKeys.DATAFRAME.value not in self:
            if DatasetKeys.ERROR.value in self:
                raise DatasetKeyError(
                    f'Attempting to extract key "{DatasetKeys.DATAFRAME_TABLE.value}" '
                    f'as input, instead found keys {list(self.keys())}. '
                    f'Error: {self[DatasetKeys.ERROR.value]}')
            raise DatasetKeyError(
                f'Attempting to extract key "{DatasetKeys.DATAFRAME_TABLE.value}" '
                f'as input, instead found keys {list(self.keys())}.')
        return TableFactory(self.dataframe)
        # This method will be modified once Table migration is complete

    @dataframe_table.setter
    def dataframe_table(self, data: Table) -> None:
        '''Set the dataframe at DatasetKeys.DATAFRAME_TABLE.'''
        self[DatasetKeys.DATAFRAME_TABLE.value] = data

    @property
    def target_table(self) -> Table:
        '''Return the dataframe at DatasetKeys.TARGET as a Table.'''

        # The following 2 lines will be deleted once Table migration is complete.
        if DatasetKeys.TARGET.value in self:
            return TableFactory(self[DatasetKeys.TARGET.value])

        if self.metadata.target is not None:
            return TableFactory(self.dataframe_table[self.metadata.target.name])
        raise DatasetKeyError(
            f'Attempting to extract key "{DatasetKeys.TARGET.value}" '
            f'as input, instead found keys {list(self.keys())}.')

    @property
    def covariates_table(self) -> Table:
        '''Return the dataframe at DatasetKeys.COVARIATES as a Table.'''
        # The following 2 lines will be deleted once Table migration is complete.
        if DatasetKeys.COVARIATES.value in self:
            return TableFactory(self[DatasetKeys.COVARIATES.value])

        if self.metadata.target is not None:
            return self.dataframe_table.drop(columns=[self.metadata.target.name])

        return self.dataframe_table

    @property
    def ground_truth(self) -> pd.DataFrame:
        '''Return the dataframe at DatasetKeys.GROUND_TRUTH

        or raise an error if it doesn't exist.'''

        if DatasetKeys.GROUND_TRUTH.value not in self:
            if DatasetKeys.ERROR.value in self:
                raise DatasetKeyError(
                    f'Attempting to extract key "{DatasetKeys.GROUND_TRUTH.value}" '
                    f'as input, instead found keys {list(self.keys())}. '
                    f'Error: {self[DatasetKeys.ERROR.value]}')
            raise DatasetKeyError(
                f'Attempting to extract key "{DatasetKeys.GROUND_TRUTH.value}" '
                f'as input, instead found keys {list(self.keys())}.')
        df_value = self[DatasetKeys.GROUND_TRUTH.value]
        if not isinstance(df_value, pd.DataFrame):
            raise DatasetValueError(
                f'Input key key {DatasetKeys.GROUND_TRUTH.value} must point to '
                f'a pandas.DataFrame, instead found a {type(df_value)}: '
                f'{df_value}')
        return pd.DataFrame(df_value)

    @ground_truth.setter
    def ground_truth(self, data: pd.DataFrame) -> None:
        self[DatasetKeys.GROUND_TRUTH.value] = data

    @property
    def predictions(self) -> pd.DataFrame:
        '''Return the dataframe at DatasetKeys.PREDICTIONS
        or raise an error if it doesn't exist.'''

        if DatasetKeys.PREDICTIONS.value not in self:
            if DatasetKeys.ERROR.value in self:
                raise DatasetKeyError(
                    f'Attempting to extract key "{DatasetKeys.PREDICTIONS.value}" '
                    f'as input, instead found keys {list(self.keys())}. '
                    f'Error: {self[DatasetKeys.ERROR.value]}')
            raise DatasetKeyError(
                f'Attempting to extract key "{DatasetKeys.PREDICTIONS.value}" '
                f'as input, instead found keys {list(self.keys())}.')
        df_value = self[DatasetKeys.PREDICTIONS.value]
        if not isinstance(df_value, pd.DataFrame):
            raise DatasetValueError(
                f'Input key key {DatasetKeys.PREDICTIONS.value} must point to '
                f'a pandas.DataFrame, instead found a {type(df_value)}: '
                f'{df_value}')
        return pd.DataFrame(df_value)

    @predictions.setter
    def predictions(self, data: pd.DataFrame) -> None:
        self[DatasetKeys.PREDICTIONS.value] = data

    # TODO(Piggy): There are 20 references to this that lack the name of the target column.
    # This is arguably a bug, but it doesn't matter until we have multiple target columns.
    # The format should be something like this:
    # {
    #    'probabilities': {
    #       'target_column_name_1': [
    #           {value1: 0.6, value2: 0.4, value3: 0.0},
    #           {value1: 0.2, value2: 0.6, value3: 0.2},
    #           {value1: 0.1, value2: 0.2, value3: 0.7},
    #       },
    #       'target_column_name_2': [
    #           {4: 0.6, 5: 0.4, 6: 0.0},
    #           {4: 0.1, 5: 0.8, 6: 0.1},
    #           {4: 0.1, 5: 0.2, 6: 0.7},
    #       },
    #    },
    #    'predictions': {'target_column_name_1': [value1, value2, value3],
    #                    'target_column_name_2': [4, 5, 6]}

    def _check_for_error(self, key: DatasetKeys) -> None:
        '''Check for an error key and raise an error if it exists.'''

        if key.value not in self:
            if DatasetKeys.ERROR.value in self:
                raise DatasetKeyError(
                    f'Attempting to extract key "{key.value}" '
                    f'as input, instead found keys {list(self.keys())}. '
                    f'Error: {self[DatasetKeys.ERROR.value]}')
            raise DatasetKeyError(
                f'Attempting to extract key "{key.value}" '
                f'as input, instead found keys {list(self.keys())}.')

    @property
    def probabilities(self) -> Table:
        '''
        Return the table at `DatasetKeys.PROBABILITIES`
        or raise an error if it doesn't exist.
        '''
        self._check_for_error(DatasetKeys.PROBABILITIES)

        table = self[DatasetKeys.PROBABILITIES.value]

        if not isinstance(table, Table):
            raise DatasetValueError(
                f'Input key key {DatasetKeys.PROBABILITIES.value} must point to '
                f'a Table, instead found a {type(table)}: '
                f'{table}'
            )

        return table

    @probabilities.setter
    def probabilities(self, data: Table) -> None:
        self[DatasetKeys.PROBABILITIES.value] = data

    def output(self, override_metadata: Optional[Metadata] = None) -> 'Dataset':
        '''Return a new dataset containing same metadata and nothing else.

        Metadata can also be overriden, all preexisting metadata will be lost.
        Generally called to create a new dataset to fill with a model's output.
        '''
        return self.__class__(metadata=override_metadata or self._metadata)

    def get_dataframe(self) -> pd.DataFrame:
        '''Return the dataframe at DatasetKeys.DATAFRAME, or raise an error if it doesn't exist.'''

        return self.dataframe

    def sorted_columns(self) -> 'Dataset':
        '''Sort columns of a dataset.

        This sorts DATAFRAME and COVARIATES by column name.

        This is needed so that the distributed algorithms operate
        on the same columns in the same order.
        '''
        # TODO(Piggy/Dan): If this becomes a performance problem
        #   we can cache the column order and only sort if the
        #   columns change.
        retval = self.output()
        retval.update(self)

        keys: List[str] = []
        if DatasetKeys.DATAFRAME.value in self:
            keys.append(DatasetKeys.DATAFRAME.value)

        if DatasetKeys.COVARIATES.value in self:
            keys.append(DatasetKeys.COVARIATES.value)

        for key in keys:
            df = self[key]
            if not isinstance(df, pd.DataFrame):
                raise DatasetValueError(
                    f'Expected dataframe at {key}, instead found {df} of type {type(df)}.'
                )
            df.columns = df.columns.astype(str)
            # ^ if column names have mixed typing they cannot be sorted
            retval[key] = (
                df.sort_index(axis=1))
        return retval
