'''Tests for one_hot_encoder.'''
# pylint: disable=missing-function-docstring, duplicate-code, missing-class-docstring
# pylint: disable=redefined-outer-name

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

from typing import Generator, Optional, Tuple

import pandas as pd
import pytest

from ....algorithms.impl.fittable_algorithm_instance import UntrainedError
from ....wrangler.dataset import Dataset, DatasetKeys

from .one_hot_encoder import OneHotModel, OneHotModelInstance


@pytest.fixture(autouse=True)
def model_and_data() -> Generator[Tuple[OneHotModelInstance, Dataset], None, None]:
    instance = OneHotModel().instantiate()

    # Simple example dataset from:
    # https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html

    students = [['Male', 1], ['Female', 3], ['Female', 2]]

    students_df = pd.DataFrame(students, columns=['gender', 'group'])

    students_dataset = Dataset({
        DatasetKeys.DATAFRAME.value: students_df})

    yield ((instance, students_dataset))


class TestOneHotEncoder:
    def test_sunny_day(self, model_and_data) -> None:
        instance, students_dataset = model_and_data
        assert isinstance(instance, OneHotModelInstance)
        assert isinstance(students_dataset, Dataset)

        instance.fit(students_dataset)
        result: Optional[Dataset] = instance.predict(students_dataset)

        assert result is not None
        students = [[1, 0.0, 1.0], [3, 1.0, 0.0], [2, 1.0, 0.0]]
        expected_result = pd.DataFrame(students, columns=['group', 'gender_Female', 'gender_Male'])

        assert result.dataframe.equals(expected_result)

    def test_untrained(self, model_and_data) -> None:
        instance, students_dataset = model_and_data
        assert isinstance(instance, OneHotModelInstance)
        assert isinstance(students_dataset, Dataset)

        with pytest.raises(UntrainedError):
            instance.predict(students_dataset)

    def test_unfamiliar_category(self, model_and_data) -> None:
        '''If the encoder encounters a category it wasn't fit on,
        we want it to put a 0 in all columns for that category instead of failing.'''
        instance, students_dataset = model_and_data
        assert isinstance(instance, OneHotModelInstance)
        assert isinstance(students_dataset, Dataset)

        instance.fit(students_dataset)

        df1: pd.DataFrame = students_dataset.dataframe
        df2 = pd.DataFrame({'gender': ['Non-binary'], 'group': [2]})
        students_dataset.dataframe = pd.concat([df1, df2], ignore_index=True)
        result: Optional[Dataset] = instance.predict(students_dataset)

        assert result is not None
        students = [
            [1, 0.0, 1.0],
            [3, 1.0, 0.0],
            [2, 1.0, 0.0],
            [2, 0.0, 0.0]]
        expected_result = pd.DataFrame(students, columns=['group', 'gender_Female', 'gender_Male'])
        assert result.dataframe.equals(expected_result)
