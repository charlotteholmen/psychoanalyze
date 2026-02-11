from dataclasses import dataclass

import numpy as np
import pymc as pm
import xarray as xr


@dataclass
class NormalParams:
    mu: float
    sigma: float


@dataclass
class LogisticPrior:
    x0: NormalParams
    k_sigma: float


def run_prior_predictive(
    n_trials: int = 100,
    logistic_prior: LogisticPrior = LogisticPrior(
        x0=NormalParams(mu=0, sigma=0.5), k_sigma=2.0
    ),
) -> pm.backends.arviz.InferenceData:
    intensities = xr.DataArray(
        np.random.choice(
            (np.arange(-3, 4) * logistic_prior.x0.sigma) + logistic_prior.x0.mu,
            size=n_trials,
        ),
        dims="trial",
    )
    with pm.Model():
        intensity = pm.Data("x", intensities, dims="trial")
        x0 = pm.Normal("x0", mu=logistic_prior.x0.mu, sigma=logistic_prior.x0.sigma)
        k = pm.HalfNormal("k", sigma=logistic_prior.k_sigma)
        gamma = pm.Beta("gamma", alpha=1, beta=9)
        lam = pm.Beta("lambda", alpha=1, beta=9)
        logit_p = pm.invlogit(k * (intensity - x0))
        p = gamma + (1 - gamma - lam) * logit_p
        pm.Bernoulli("y", p=p, dims="trial")
        idata = pm.sample_prior_predictive()
    return idata
