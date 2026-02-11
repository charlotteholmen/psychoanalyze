class TestPsychometricFunction:
    def test_preparing_plot_of_psychometric_function(self) -> None:
        from psychoanalyze import psi

        fig = psi.plot()
        assert fig.layout.yaxis.title.text == "% Correct"
