'''A Table representing a dictionary from str to list-like.'''

# Copyright (c) 2025 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

from typing import Any, Dict, List, Union

import numpy as np
import pandas as pd

from .impl.table import TableFactory, Table
from .impl.table_catalog import TableCatalog


class DictTable(Table):
    '''A Table representing a dictionary from str to list-like.'''
    name = 'dict'
    _value: Dict[Union[str, int], List]
    my_type = dict

    def to_csv(self, *args, **kwargs) -> str:
        '''Output the table as a CSV string.'''
        return pd.DataFrame(self._value).to_csv(*args, **kwargs)

    def as_dict(self, *args, **kwargs) -> Dict[Union[str, int], Any]:
        '''Convert table to a dictionary.'''
        return self._value

    def drop(self, columns: List[Union[int, str]]) -> Table:
        '''Return a copy of this table with selected columns dropped.'''
        return TableFactory(
            {k: v for k, v in self._value.items()
             if k not in columns})

    @property
    def empty(self) -> bool:
        '''Return True if the table is empty.'''
        return len(self._value) == 0 or all(
            len(v) == 0 for v in self._value.values()
        )

    @property
    def shape(self) -> tuple:
        '''Get the shape of the table.'''
        return (len(next(iter(self._value.values()))), len(self.columns))

    @property
    def columns(self) -> List[Union[int, str]]:
        '''Return the column names of the table.'''
        return sorted(list(self._value.keys()))

    @columns.setter
    def columns(self, value: List[Union[int, str]]) -> None:
        '''Set the column names of the table.'''
        # TODO(Merritt/Piggy): We can get a sorted list of the current column names,
        # then iterate over the new column names and update the dictionary.
        raise NotImplementedError('Cannot set columns for a DictTable')


def as_dataframe(from_table: Table) -> pd.DataFrame:
    '''Export a DictTable to a pandas DataFrame.'''
    assert isinstance(from_table, DictTable)
    retval = pd.DataFrame(from_table.value())
    # Make sure columns are in a predictable order.
    return retval.reindex(from_table.columns, axis=1)


def as_numpy(from_table: Table) -> np.ndarray:
    '''Export a DictTable to a numpy array.'''
    df_table = as_dataframe(from_table)
    if df_table.shape[1] == 1:
        return df_table.to_numpy().flatten()
    return df_table.to_numpy()


def register(catalog: TableCatalog):
    '''Register the DataFrameTable with the catalog.'''
    catalog.register(DictTable)
    TableFactory.register_constructor(dict, DictTable)
    TableFactory.register_exporter(
        from_type=dict, to_type=dict, exporter=DictTable.value)
    TableFactory.register_exporter(
        from_type=dict, to_type=pd.DataFrame, exporter=as_dataframe)
    TableFactory.register_exporter(
        from_type=dict, to_type=np.ndarray, exporter=as_numpy)
