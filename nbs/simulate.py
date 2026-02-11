"""PsychoAnalyze dashboard as a marimo notebook.

Interactive data simulation & analysis for psychophysics.
Replaces the former Dash dashboard (removed).
"""

import marimo

__generated_with = "0.19.9"
app = marimo.App(width="full", app_title="PsychoAnalyze")


@app.cell
def _():
    import psychoanalyze as ps
    import xarray as xr

    return ps, xr


@app.cell
def _(xr):
    dataset=xr.Dataset({
        "magnitude": ("sample", [0.1, 0.2, 0.3]),
        "hit_rate": ("sample", [0.1, 0.5, 0.7]),
    })
    return (dataset,)


@app.cell
def _(dataset, ps):
    ps.psi.plot(dataset)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
