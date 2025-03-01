'''Tests for k_fold_splitter.py'''

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.
from typing import List

import pandas as pd

from ..problem_def.cross_validation_config import CrossValidationConfig
from ..wrangler.dataset import Dataset, Metadata, Column, RoleName

from .k_fold_splitter import KFoldSplitter

# pylint: disable=missing-function-docstring, duplicate-code


def test_split_default_hyperparams() -> None:
    dataframe = pd.DataFrame({
        'a': range(1, 1001),
        'b': range(1001, 2001),
        'c': range(2001, 3001)})
    data = Dataset(metadata=Metadata(
        roles={
            RoleName.TARGET: [Column('c')]
        }
    ))
    data.dataframe = dataframe
    dut = KFoldSplitter(cv_config=CrossValidationConfig({}))

    got = dut.split(dataset=data)

    # default n_splits: 5
    assert len(got.folds) == 5
    assert got.ground_truth is not None
    assert got.ground_truth.ground_truth.shape == (1000, 1)
    for fold in got.folds:
        # every row not in the fold should be in the train dataset
        # all three columns are in the train dataset
        assert fold.train.dataframe.shape == (800, 3)
        # total number of rows in each fold is 200
        # validate dataset does not include the target column
        assert fold.validate.dataframe.shape == (200, 2)


def test_split_is_random() -> None:
    dataframe = pd.DataFrame({
        'a': range(1, 1001),
        'b': range(1001, 2001),
        'c': range(2001, 3001)})
    data = Dataset(metadata=Metadata(
        roles={
            RoleName.TARGET: [Column('c')]
        }
    ))

    data.dataframe = dataframe
    dut = KFoldSplitter(cv_config=CrossValidationConfig({}))

    got = dut.split(dataset=data)
    assert got.folds[0].train.dataframe.iat[10, 1] == 1014

    dut2 = KFoldSplitter(cv_config=CrossValidationConfig({'seed': 1054}))
    got2 = dut2.split(dataset=data)
    assert got2.folds[0].train.dataframe.iat[10, 1] == 1015


def test_split_large_dataset() -> None:
    dataframe = pd.DataFrame(
        {
            'a': range(1, 15001),
            'b': range(1, 15001),
            'c': range(1, 15001)
        }
    )
    data = Dataset(metadata=Metadata(
        roles={
            RoleName.TARGET: [Column('c')]
        }
    ))

    data.dataframe = dataframe
    dut = KFoldSplitter(cv_config=CrossValidationConfig({}))
    got = dut.split(dataset=data)

    assert len(got.folds) == 3
    assert got.ground_truth is not None
    assert got.ground_truth.ground_truth.shape == (15000, 1)

    for fold in got.folds:
        # every row not in the fold should be in the train dataset
        # all three columns are in the train dataset
        assert fold.train.dataframe.shape == (10000, 3)

        # total number of rows in each fold is 5,000
        # validate dataset does not include the target column
        assert fold.validate.dataframe.shape == (5000, 2)


def test_split_order() -> None:
    dataframe = pd.DataFrame({
        'a': range(1, 101),
        'b': range(101, 201),
        'c': range(201, 301)})
    data = Dataset(metadata=Metadata(
        roles={
            RoleName.TARGET: [Column('c')]
        }
    ))

    data.dataframe = dataframe
    dut = KFoldSplitter(cv_config=CrossValidationConfig({}))
    got = dut.split(dataset=data)
    validate_dfs: List[pd.DataFrame] = [f.validate.dataframe for f in got.folds]
    concatenated_folds = pd.concat(validate_dfs, axis=0)
    concatenated_folds.reset_index(inplace=True, drop=True)
    assert concatenated_folds.shape == (100, 2)
    assert got.ground_truth is not None
    assert got.ground_truth.ground_truth is not None
    list_to_concat: List[pd.DataFrame] = [concatenated_folds, got.ground_truth.ground_truth]
    full_dataset = pd.concat(list_to_concat, axis=1)
    assert full_dataset.shape == (100, 3)
    assert all(full_dataset['a'] + 200 == full_dataset['c'])
