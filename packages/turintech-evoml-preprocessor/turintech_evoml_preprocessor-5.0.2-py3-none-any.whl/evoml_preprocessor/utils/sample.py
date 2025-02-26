from typing import List, Optional

import numpy as np
import pandas as pd
from evoml_api_models import MlTask

from evoml_preprocessor.utils.conf.conf_manager import conf_mgr

CONF = conf_mgr.preprocess_conf  # Alias for readability
MIN_CLASS_COUNT = 20


def _get_sample_clf(
    label_column: pd.Series,
    sample_size: int,
) -> pd.Index:
    """Sampling for classification datasets
    Args:
        label_column:
            The label column data.
        sample_size:
            The sample size.

    This algorithm uses numpy choice without replacement to select random indexes, while ensuring that
    each class is sampled at least `n` times. `n` is computed as the lower value between the
    `MIN_CLASS_COUNT` and the number of instances of the minimum occurring class in the unsampled feature.

    It uses a naive approach to ensure the correct number of samples are chosen once padding for low
    sample counts is completed. We remove the excess from the most popular class, which should succeed
    as long as the sample isn't too small.

    Returns:
        A pandas index that can be used to sample rows from some dataset.

    Raises:
        ValueError: if max class count is too small
    """
    normalized_class_counts = label_column.value_counts(normalize=True)

    class_counts = (normalized_class_counts * len(label_column)).astype(int)
    sampled_class_counts = (normalized_class_counts * sample_size).astype(int)
    minimum_class_count = min(MIN_CLASS_COUNT, class_counts.min())

    # set a lower limit to the number of possible instances of each sampled class
    sampled_class_counts.loc[sampled_class_counts < minimum_class_count] = minimum_class_count
    most_common_class = class_counts.idxmax()
    sampled_class_counts.loc[most_common_class] -= sampled_class_counts.sum() - sample_size
    if sampled_class_counts.loc[most_common_class] < 0:
        raise ValueError("sampling algorithm cannot generate a viable dataset from the provided parameters")

    np_indices: List[np.ndarray] = []
    for value, count in sampled_class_counts.items():
        np_indices.append(np.random.choice(label_column.loc[label_column == value].index, count, replace=False))

    return pd.Index(np.concatenate(np_indices, axis=0))


def _get_sample_reg(
    label_column: pd.Series,
    sample_size: int,
) -> pd.Index:
    """Sampling for classification datasets
    Args:
        label_column:
            The label column data.
        max_size:
            The sample size.

    Returns:
        A pandas index that can be used to sample rows from some dataset.
    """
    return pd.Index(np.random.choice(label_column.index, sample_size, replace=False))


def get_sample(
    label_column: pd.Series,
    sample_size: int = CONF.SAMPLE_SIZE,
    task: Optional[MlTask] = MlTask.regression,
) -> pd.Index:
    """Selects a random subset of the data to perform the search on. We store this data internally for future use.
    Args:
        label_column:
            The label column data.
        max_size:
            The sample size.
        task:
            The ml task (for stratified sampling)

    Returns:
        A pandas index that can be used to sample rows from some dataset.
    """
    # Check if search_sample size > dataset, then select smallest value
    if len(label_column) >= sample_size:
        if task == MlTask.classification:
            return _get_sample_clf(label_column, sample_size)
        elif task == MlTask.regression:
            return _get_sample_reg(label_column, sample_size)
        else:
            raise NotImplementedError(f"No sampling implemented for {task}")
    else:
        return label_column.index
