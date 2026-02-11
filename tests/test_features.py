from psychoanalyze import psi


class TestPsychometricFunction:
    def test_preparing_plot_of_psychometric_function(self) -> None:


        fig = psi.plot()
        assert fig.layout.yaxis.title.text == "percent_correct"
