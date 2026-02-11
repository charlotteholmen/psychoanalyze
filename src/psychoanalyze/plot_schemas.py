from __future__ import annotations

import pandera as pa
from pandera import Field
from pandera.typing import Series


class PsychometricFunctionSchema(pa.DataFrameModel):
    Magnitude: Series[float]
    Hit_Rate: Series[float] = Field(alias="Hit Rate")
    Hits: Series[int] = Field(nullable=True)
    n_trials: Series[int] = Field(nullable=True, alias="n trials")

    class Config:
        strict = True
        coerce = True


class ThresholdVsTimeSchema(pa.DataFrameModel):
    Days: Series[int]
    threshold_mean: Series[float]
    Subject: Series[str]
    threshold_ci_low: Series[float] = Field(nullable=True)
    threshold_ci_high: Series[float] = Field(nullable=True)
    Days_log: Series[float] = Field(nullable=True)
    Days_z: Series[float] = Field(nullable=True)

    class Config:
        strict = True
        coerce = True


class WeberCurvesSchema(pa.DataFrameModel):
    Standard: Series[float]
    threshold: Series[float]
    Subject: Series[str]
    weber_fraction: Series[float] = Field(nullable=True, alias="Weber fraction")
    ci_low: Series[float] = Field(nullable=True)
    ci_high: Series[float] = Field(nullable=True)
    Standard_log: Series[float] = Field(nullable=True)
    Standard_z: Series[float] = Field(nullable=True)
    k: Series[float] = Field(nullable=True)
    beta: Series[float] = Field(nullable=True, alias="β")

    class Config:
        strict = True
        coerce = True


class StrengthDurationSchema(pa.DataFrameModel):
    pulse_width: Series[int] = Field(alias="Pulse Width")
    threshold: Series[float]
    Subject: Series[str]
    ci_low: Series[float] = Field(nullable=True)
    ci_high: Series[float] = Field(nullable=True)
    PW_log: Series[float] = Field(nullable=True)
    PW_z: Series[float] = Field(nullable=True)
    Irh: Series[float] = Field(nullable=True)
    tau: Series[float] = Field(nullable=True, alias="τ")

    class Config:
        strict = True
        coerce = True
