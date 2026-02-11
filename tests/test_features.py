import xarray as xr

from psychoanalyze import plot, psi


class TestPsychometricFunction:
    def test_psi_plot_empty_dataframe(self):
        points = xr.Dataset(
            {
                "hit_rate": ("sample", []),
                "magnitude": ("sample", []),
            }
        )

        fig = psi.plot(points=points)
        assert fig.layout.yaxis.title.text == "hit_rate"
        assert fig.layout.xaxis.title.text == "magnitude"


class TestPlotsEntrypoint:
    def test_plot_all_returns_four_target_plots(self) -> None:
        trials = xr.Dataset(
            {
                "Magnitude": ("trial", [1.0, 2.0]),
                "Result": ("trial", [True, False]),
            }
        )

        plots = plot.all(trials)

        assert set(plots.keys()) == {
            "Psychometric function",
            "Threshold vs Time",
            "Strength-duration",
            "Weber curves",
        }
