Feature: Strength-duration analysis

    As a researcher
    I want to analyze strength-duration data
    So that I can understand temporal integration

    Background:
        Given the dashboard is running

    Scenario: Upload strength-duration data with required columns
        Given I have strength-duration data with columns "Subject", "Block", "Dimension", "Fixed Magnitude", "Threshold"
        When I upload the strength-duration dataset
        Then the dataset should be accepted

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

    Scenario: Handle missing dimensions
        Given I have strength-duration data with no "Dimension" column
        When I render the strength-duration plot
        Then I should see a validation error about "Dimension"
