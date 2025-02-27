from __future__ import annotations

from dataclasses import dataclass
from typing import cast

import numpy as np
import pandas as pd


def and_filters(filters: list[np.ndarray]) -> np.ndarray:
    if not filters:
        raise ValueError("no filters")
    if len(filters) == 1:
        return filters[0]
    return np.bitwise_and.reduce(filters)


class BaseFilter:
    @classmethod
    def columns(cls) -> list[str]:
        return []

    def filter(self, df: pd.DataFrame, *, copy: bool = False) -> pd.DataFrame:
        b = self.booleans(df)  # pylint: disable=assignment-from-none
        if b is None:
            return df
        return df[b].copy() if copy else df[b]

    def booleans(self, df: pd.DataFrame) -> pd.Series | None:
        return None

    def and_filters(self, filters: list[np.ndarray]) -> np.ndarray:
        return and_filters(filters)


@dataclass
class PepXMLFilter(BaseFilter):
    noX: bool = True
    minProbabilityCutoff: float | None = 0.8

    @classmethod
    def columns(cls) -> list[str]:
        return ["peptide", "peptideprophet_probability", "probability"]

    def booleans(self, df: pd.DataFrame) -> pd.Series | None:
        filters: list[np.ndarray] = []

        def add(b: bool) -> None:
            filters.append(cast(np.ndarray, b))

        if self.noX:
            add(~df["peptide"].str.contains("X"))

        if self.minProbabilityCutoff:
            if "peptideprophet_probability" in df:
                add(df["peptideprophet_probability"] >= self.minProbabilityCutoff)
            elif "probability" in df:
                add(df["probability"] >= self.minProbabilityCutoff)

        return pd.Series(self.and_filters(filters))
