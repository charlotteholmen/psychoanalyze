import pandas as pd

from psychoanalyze import plot, psi


class TestPsychometricFunction:
    def test_psi_plot_empty_dataframe(self):
        fig = psi.plot(points=pd.DataFrame({"percent_correct": [], "magnitude": []}))
        assert fig.layout.yaxis.title.text == "percent_correct"
        assert fig.layout.xaxis.title.text == "magnitude"


class TestPlotsEntrypoint:
    def test_plot_all_returns_four_target_plots(self) -> None:
        trials = pd.DataFrame(
            {
                "Magnitude": [1.0, 2.0],
                "Result": [True, False],
            }
        )

        plots = plot.all(trials)

        assert set(plots.keys()) == {
            "Psychometric function",
            "Threshold vs Time",
            "Strength-duration",
            "Weber curves",
        }
