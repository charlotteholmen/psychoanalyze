@tier:integration
Feature: Data generation and simulation (prior predictive)

    As a researcher
    I want to generate simulated psychophysical data via PyMC prior predictive sampling
    So that I can design experiments, check priors, and create synthetic datasets without observed data

    Background:
        Given PyMC is available
        And the psychometric model has priors for "x0", "k", "gamma", "lambda"

    Scenario: Run prior predictive sampling with default draws
        Given I have a psychometric PyMC model with defined priors
        When I run prior predictive sampling
        Then I should get an InferenceData object with a "prior_predictive" group
        And the prior predictive group should contain "obs" (observed trials or hit counts)
        And the number of prior predictive draws should be greater than zero

    Scenario: Run prior predictive sampling with a specified number of draws
        Given I have a psychometric PyMC model with defined priors
        And I set prior predictive draws to "500"
        When I run prior predictive sampling
        Then the prior predictive sample should have exactly "500" draws
        And I should get an InferenceData object with a "prior_predictive" group

    Scenario: Generate simulated trial-level data from prior predictive samples
        Given I have prior predictive samples from the psychometric model
        And I have design settings "n_blocks" and "n_levels" and "trials_per_level"
        When I generate simulated trials from the prior predictive
        Then I should get trial data with columns "Intensity", "Result", "Block"
        And the number of blocks should match "n_blocks"
        And the number of unique intensity levels should match "n_levels"
        And each intensity-level cell should have "trials_per_level" trials


    Scenario: Export prior predictive samples for downstream use
        Given I have run prior predictive sampling
        When I export the prior predictive result
        Then I should get an ArviZ InferenceData object
        And the InferenceData should have "prior" and "prior_predictive" groups
        And I should be able to pass it to ArviZ plotting functions
