Feature: Psychometric function

As a user of psychoanalyze
I want to be able to plot psychometric functions from trial data
So that I can analyze perceptual thresholds and sensitivities.

    Scenario: Preparing a plot of the psychometric function
        Given no data
        When I try to plot the psychometric function
        Then it should create a plot with "% Correct" on the y-axis
