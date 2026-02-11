@tier:domain
Feature: Weber's law analysis

    As a researcher
    I want to analyze Weber's law data
    So that I can estimate the Weber fraction

    Background:
        Given the dashboard is running

    Scenario: Upload Weber data with required columns
        Given I have Weber data with columns "Subject", "Dimension", "Reference Charge (nC)", "Difference Threshold (nC)", "Date", "location_CI_5", "location_CI_95"
        When I upload the Weber dataset
        Then the dataset should be accepted
        And error bars should be derived from "location_CI_5" and "location_CI_95"

    Scenario: Render Weber scatter plot with trendline
        Given I have Weber data loaded
        When I render the Weber plot
        Then reference charge should be on the x-axis
        And difference threshold should be on the y-axis
        And points should be rendered as scatter markers
        And an OLS trendline should be rendered
        And points should be colored by "Subject"
        And points should use different symbols by "Dimension"
        And hover text should include "Reference Charge (nC)"
        And hover text should include "Difference Threshold (nC)"
        And hover text should include "Date"

    Scenario: Compute the Weber fraction
        Given I have an OLS slope from the Weber trendline
        When I compute the Weber fraction
        Then "k" should equal "slope / 100"
