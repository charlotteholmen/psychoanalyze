# Specifications & Design Documents

This folder contains executable specifications (BDD scenarios) and design documents that drive development.

## Behavior-Driven Specifications (BDD)

- **[data-pipeline.feature](./data-pipeline.feature)** - Trial aggregation pipeline scenarios (Trials → Points → Blocks → Sessions)
- **[gelman-workflow.feature](./gelman-workflow.feature)** - Complete Bayesian workflow scenarios using Gelman's principled approach

These `.feature` files are executable with pytest-bdd and serve as acceptance tests.

## Architecture & Planning Diagrams

See the [Architecture Diagrams](../architecture-diagrams/) folder for D2 source files and rendered SVGs showing:
- System architecture (three pillars)
- Data pipeline flows
- Bayesian workflow
- Psychometric function modeling
- Weber's law and strength-duration analysis

## Engineering Approach

For details on how specifications drive development, see [plan-engineeringApproach](../architecture-diagrams/plan-engineeringApproach.md) in the diagrams folder.
