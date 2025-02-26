from __future__ import annotations

from typing import List, Optional

import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder as _OneHotEncoder

from evoml_preprocessor.preprocess.models import CategoricalEncoder
from evoml_preprocessor.preprocess.transformers.encoders._base import Encoder
from evoml_preprocessor.types import dtype
from evoml_preprocessor.types.pandas import DataFrame, Series, SeriesTarget


class OneHotEncoder(Encoder[dtype.Categorical, dtype.Uint8]):
    """
    Encoder for performing one-hot encoding.
    Inherits the Encoder class.
    """

    slug = CategoricalEncoder.ONE_HOT_ENCODER
    columns: List[str]

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self._encoder = None

    @property
    def encoder(self) -> _OneHotEncoder:
        if self._encoder is None:
            raise ValueError("Fit must be called to set the encoder.")
        return self._encoder

    def fit(self, X: Series[dtype.Categorical], y: Optional[SeriesTarget] = None) -> None:
        # @pyright: confusion over possible dtypes
        self._encoder = _OneHotEncoder(sparse_output=False, handle_unknown="ignore", dtype=np.uint8)  # type: ignore

        # @data: no copy
        X_np = X.to_numpy().reshape(-1, 1)

        self.encoder.fit(X_np)
        self.columns = [f"{self.name}_{col}_onehot" for col in range(1, len(self.encoder.categories_[0]) + 1)]

    def transform(self, X: Series[dtype.Categorical]) -> DataFrame[dtype.Uint8]:
        X_np = X.to_numpy().reshape(-1, 1)

        transformed = self.encoder.transform(X_np)

        return pd.DataFrame(transformed, columns=self.columns, index=X.index)  # type: ignore
