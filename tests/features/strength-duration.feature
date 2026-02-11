@tier:domain
Feature: Strength-duration analysis

    As a researcher
    I want to analyze strength-duration data
    So that I can understand temporal integration

    Background:
        Given the dashboard is running


    Scenario: Plot amplitude-modulated data
        Given I have strength-duration data with "Dimension" set to "Amp"
        When I render the strength-duration plot
        Then the x-axis should display fixed pulse width
        And the y-axis should display threshold amplitude

    Scenario: Plot width-modulated data
        Given I have strength-duration data with "Dimension" set to "Width"
        When I render the strength-duration plot
        Then the x-axis should display fixed amplitude
        And the y-axis should display threshold pulse width


