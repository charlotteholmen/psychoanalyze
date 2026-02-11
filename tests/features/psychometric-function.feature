Feature: Psychometric function

    As a researcher
    I want to model and visualize psychometric functions from trial data
    So that I can estimate thresholds and sensitivities with uncertainty

    Background:
        Given the psychoanalyze data contract is valid
        And the default link function is "logit"

    Scenario: Validate psychometric trial schema
        Given a dataset with columns "Intensity", "Result", "Block"
        And the "Result" column is binary
        When I validate the dataset for psychometric analysis
        Then the dataset should be accepted

    Scenario: Reject trial data with missing required columns
        Given a dataset missing the "Intensity" column
        When I validate the dataset for psychometric analysis
        Then the dataset should be rejected
        And the validation error should mention "Intensity"

    Scenario: Aggregate trials into points
        Given I have trial data with columns "Intensity", "Result", "Block"
        When I aggregate trials by "Intensity"
        Then I should get points with "Hits"
        And I should get points with "n trials"
        And I should get points with "Hit Rate"
        And "Hit Rate" should equal "Hits / n trials"
        And "Hit Rate" should be between 0 and 1
        And binomial confidence intervals should be calculated

    Scenario: Fit a psychometric curve per block
        Given I have points data with "Intensity", "Hits", "n trials", "Block"
        When I fit a psychometric function per block
        Then I should get block parameters with "threshold"
        And I should get block parameters with "slope"
        And I should get block parameters with "intercept"
        And "threshold" should equal "-intercept / slope"

    Scenario: Include guess and lapse rates in the psychometric function
        Given I have block parameters with "x0", "k", "gamma", "lambda"
        When I generate the psychometric curve
        Then the curve should follow "psi(x) = gamma + (1 - gamma - lambda) * F(x; x0, k)"
        And the curve should be bounded between 0 and 1

    Scenario: Compute a credible band for the psychometric curve
        Given I have posterior samples for a fitted block
        When I compute a 90% credible band for the curve
        Then I should get lower and upper bounds for each intensity
        And the bounds should be ordered with lower less than upper

    Scenario: Render the psychometric function plot
        Given I have points with "Intensity", "Hit Rate", "ci_low", "ci_high"
        And I have block parameters with "threshold", "slope", "intercept"
        When I generate the psychometric function plot
        Then the y-axis should display "Hit Rate"
        And the y-axis should use the range 0 to 1
        And observed points should be rendered as scatter markers
        And the fitted curve should be rendered as a continuous line
        And a vertical threshold marker should appear at "threshold"
        And error bars should use the binomial confidence intervals

    Scenario Outline: Apply intensity scale transforms
        Given I have psychometric points for "Intensity"
        When I set the intensity scale to "<scale>"
        Then the x-axis should display intensities in "<scale>" scale

        Examples:
            | scale  |
            | linear |
            | log    |
            | z      |

    Scenario: Restrict the plot to selected blocks
        Given I have points and fits for multiple blocks
        When I restrict the analysis to a subset of blocks
        Then only the selected blocks should be rendered in the plot

    Scenario: Generate simulated trials from model parameters
        Given I have simulation parameters "x0", "k", "gamma", "lambda"
        And I have simulation settings "n blocks" and "n levels"
        When I generate simulated trials
        Then I should get trial data with columns "Intensity", "Result", "Block"
        And the number of blocks should match "n blocks"

    Scenario: Export plot and data artifacts
        Given I have a psychometric plot and its underlying data
        When I export the plot
        Then it should be available as SVG
        And it should be available as PNG
        And it should be available as PDF
        When I export the data
        Then it should be available as CSV
        And it should be available as Parquet
        And it should be available as JSON
