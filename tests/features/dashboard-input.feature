@tier:integration
Feature: Dashboard input data and simulation

    As a researcher
    I want to load or simulate trials in the dashboard
    So that the analysis pipeline has valid inputs

    Background:
        Given the dashboard is running

    Scenario: Upload trials data in a supported format
        Given I have trial data with columns "Subject", "Block", "Intensity", "Result"
        When I upload the dataset in "csv" format
        Then the dataset should be accepted
        And trials should be available for analysis

    Scenario: Reject trials data with a missing column
        Given I have trial data missing the "Intensity" column
        When I upload the dataset in "parquet" format
        Then I should see a schema validation error
        And the error should list "Intensity" as required

    Scenario: Simulate trials from model parameters
        Given I set simulation parameters "x0", "k", "gamma", "lambda"
        And I set simulation settings "n blocks" and "n levels"
        When I generate simulated trials
        Then I should get trial data with columns "Intensity", "Result", "Block"
        And the number of blocks should match "n blocks"
        And the number of intensity levels should match "n levels"

    Scenario: Default link function is logit
        Given the default link function is "logit"
        When I view the link function details
        Then the logit equation should be available

    Scenario: Toggle link function visibility
        Given the link function equation is visible
        When I toggle link function visibility
        Then the link function equation should be hidden
        When I toggle link function visibility again
        Then the link function equation should be visible

    Scenario: Lock a simulation parameter
        Given the "gamma" parameter is locked
        When I adjust the "x0" parameter
        Then the "gamma" value should remain unchanged

    Scenario: Reuse cached Bayesian fit artifacts
        Given I have a dataset and simulation settings
        When I run a Bayesian fit
        Then fit artifacts should be cached locally
        When I run the same Bayesian fit again
        Then cached artifacts should be reused
