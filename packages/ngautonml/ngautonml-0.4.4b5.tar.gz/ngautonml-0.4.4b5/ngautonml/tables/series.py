'''A Table representing a pandas Series.'''

# Copyright (c) 2025 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

from typing import List, Union

import numpy as np
import pandas as pd

from .impl.table import TableFactory, Table
from .impl.table_catalog import TableCatalog

from .dataframe import DataFrameTable


class SeriesTable(DataFrameTable):
    '''A Table representing a pandas Series.

    This Table can only have one column.
    '''
    name = 'series'
    _value: pd.Series  # type: ignore[assignment]
    my_type = pd.Series  # type: ignore[assignment]

    @property
    def columns(self) -> List[Union[int, str]]:
        '''Return the column names of the table.'''
        return [str(self._value.name)]

    @columns.setter
    def columns(self, value: List[Union[int, str]]) -> None:
        '''Set the column names of the table.'''
        self._value.name = value[0]


def as_numpy(from_table: Table) -> np.ndarray:
    '''Export a SeriesTable to a numpy array.'''
    assert isinstance(from_table, SeriesTable)
    if from_table.shape[1] == 1:
        return from_table.value().to_numpy().flatten()
    return from_table.value().to_numpy()


def as_dataframe(from_table: Table) -> pd.DataFrame:
    '''Export a SeriesTable to a pandas DataFrame.'''
    assert isinstance(from_table, SeriesTable)
    return pd.DataFrame(from_table.value())


def register(catalog: TableCatalog):
    '''Register the SeriesTable with the catalog.'''
    catalog.register(SeriesTable)
    TableFactory.register_constructor(pd.Series, SeriesTable)
    TableFactory.register_exporter(
        from_type=pd.Series, to_type=pd.Series, exporter=SeriesTable.value)
    TableFactory.register_exporter(
        from_type=pd.Series, to_type=np.ndarray, exporter=as_numpy)
    TableFactory.register_exporter(
        from_type=pd.Series, to_type=pd.DataFrame, exporter=as_dataframe)
