Feature: Dashboard visualization panel

    As a researcher
    I want interactive psychometric plots
    So that I can inspect results and uncertainty

    Background:
        Given the dashboard is running
        And I have points with "Intensity" and "Hit Rate"
        And I have fitted psychometric curves

    Scenario: Show a credible band around the fitted curve
        Given I have posterior samples for a fitted block
        When I render the psychometric plot
        Then a credible band should appear around the fitted curve
        And the credible band should represent a 90% interval

    Scenario: Enable interactive exploration
        When I view the psychometric plot
        Then I should be able to zoom the plot
        And I should be able to pan the plot
        And hovering a point should show its values
