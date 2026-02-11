Feature: Dashboard output panel

    As a researcher
    I want to filter outputs and export artifacts
    So that I can focus on specific blocks and share results

    Background:
        Given the dashboard is running
        And I have fitted psychometric curves

    Scenario: Filter plots by selected blocks
        Given I have results for multiple blocks
        When I select a subset of blocks in the output panel
        Then only the selected blocks should be shown in the plot
        And only the selected blocks should be shown in the aggregated data

    Scenario: Export plot formats
        Given I have a psychometric plot
        When I export the plot
        Then it should be available as SVG
        And it should be available as PNG
        And it should be available as PDF

    Scenario: Export data formats
        Given I have aggregated trial data
        When I export the data
        Then it should be available as CSV
        And it should be available as JSON
        And it should be available as Parquet
        And it should be available as DuckDB
