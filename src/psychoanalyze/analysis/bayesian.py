from __future__ import annotations

import polars as pl

from ..types import BayesianFitSettings, CacheBackend, FitArtifacts, LinkFunction


def fit_psychometric_bayesian(
    points: pl.DataFrame,
    settings: BayesianFitSettings,
    link: LinkFunction = LinkFunction.LOGIT,
    cache: CacheBackend | None = None,
) -> FitArtifacts:
    raise NotImplementedError


def load_cached_fit(cache: CacheBackend, key: str) -> FitArtifacts | None:
    raise NotImplementedError


def store_cached_fit(cache: CacheBackend, key: str, artifacts: FitArtifacts) -> None:
    raise NotImplementedError
