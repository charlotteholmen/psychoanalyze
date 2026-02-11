"""PsychoAnalyze dashboard as a marimo notebook.

Interactive data simulation & analysis for psychophysics.
Replaces the former Dash dashboard (removed).
"""

import marimo

__generated_with = "0.19.8"
app = marimo.App(width="full", app_title="PsychoAnalyze")

with app.setup:
    import psychoanalyze as psy


@app.cell
def _():
    import xarray as xr
    import arviz_stats as azs
    import altair as alt
    import numpy as np
    import pymc as pm
    from scipy.special import expit
    import pandas as pd
    from arviz_base import load_arviz_data
    import marimo as mo

    import arviz_plots as azp

    return alt, azp, azs, expit, mo, np, pd, xr


@app.cell
def _(mo):
    x0_mu = mo.ui.number(label="x0_mu", value=0)
    x0_sigma = mo.ui.number(label="x0_sigma", value=1)
    k_sigma = mo.ui.number(label="k_sigma", value=1)
    mo.vstack([x0_mu, x0_sigma, k_sigma])
    return k_sigma, x0_mu, x0_sigma


@app.cell
def _(k_sigma, x0_mu, x0_sigma):
    logistic_prior = psy.simulate.LogisticPrior(
        x0=psy.simulate.NormalParams(
            mu=x0_mu.value,
            sigma=x0_sigma.value,
        ),
        k_sigma=k_sigma.value,
    )
    return (logistic_prior,)


@app.cell
def _(logistic_prior):
    prior_samples = psy.simulate.run_prior_predictive(
        n_trials=100,
        logistic_prior=logistic_prior,
    )
    return (prior_samples,)


@app.cell
def _(azs, prior_samples):
    prior_params = (
        (
            azs.summary(prior_samples, group="prior", fmt="xarray").sel(
                summary=["mean", "eti89_ub", "eti89_lb"]
            )[["lambda", "gamma", "x0", "k"]]
        )
        .to_dataframe()
        .T
    )
    return (prior_params,)


@app.cell
def _(alt, expit, logistic_prior, np, pd, prior_params, prior_samples, xr):
    x = (np.linspace(-3, 3) * logistic_prior.x0.sigma) + logistic_prior.x0.mu

    mean_params = prior_params["mean"]
    y = mean_params["gamma"] + (1 - mean_params["gamma"] - mean_params["lambda"]) * expit(
        mean_params["k"] * (x - mean_params["x0"])
    )
    fit_line = (
        alt.Chart(data=pd.DataFrame({"x": x, "p": y})).mark_line().encode(x="x", y="p")
    )
    _sample_data_grouped = (
        prior_samples.prior.sel(draw=0, chain=0)
        .merge(prior_samples.constant_data)
        .groupby("x")
    )
    data_points = (
        alt.Chart(
            xr.Dataset(
                {
                    "p": _sample_data_grouped.mean()["y"],
                    "n": _sample_data_grouped.count()["y"],
                }
            )
            .to_dataframe()
            .reset_index()
        )
        .mark_point()
        .encode(x="x", y="p", size="n")
    )
    fit_line + data_points
    return


@app.cell
def _(azp, prior_samples):
    pc = azp.plot_dist(
        prior_samples,
        var_names=["x0", "k", "gamma", "lambda"],
        kind="ecdf",
        group="prior",
    )
    pc.show()
    return


if __name__ == "__main__":
    app.run()
