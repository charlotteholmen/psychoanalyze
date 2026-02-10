# Architecture & Planning Diagrams

This folder contains D2 source files and rendered SVG diagrams that visualize system architecture, data flows, and planning.

## Main Architecture Diagram

- **[plan.d2](./plan.d2)** ([rendered](../figures/plan.svg)) - Top-level dependency graph showing feature development order and revision planning

## System Architecture

- **[architecture.d2](./architecture.d2)** ([rendered](../figures/architecture.svg)) - Three-pillar design: data processing, interactive dashboard, Python API

## Analysis & Modeling Flows

- **[bayesian-workflow.d2](./bayesian-workflow.d2)** - Gelman's principled Bayesian workflow with prior/posterior checks
- **[bayes-analysis.d2](./bayes-analysis.d2)** - Hierarchical Bayesian model fitting pipeline
- **[gelman-workflow.d2](./gelman-workflow.d2)** - Workflow steps and decision points
- **[hierarchical_model.d2](./hierarchical_model.d2)** - Hierarchical structure for multi-block fitting

## Data & Plot Specifications

- **[psychometric-function.d2](./psychometric-function.d2)** - Psychometric curve generation and visualization
- **[weber-curves.d2](./weber-curves.d2)** - Weber's law modeling and power-law analysis
- **[strength-duration.d2](./strength-duration.d2)** - Strength-duration curve fitting
- **[threshold-vs-time.d2](./threshold-vs-time.d2)** - Temporal threshold evolution analysis
- **[full_model.d2](./full_model.d2)** - Complete system architecture diagram

## Engineering Approach

- **[plan-engineeringApproach.md](./plan-engineeringApproach.md)** - Technical approach: declarative artifacts, data contracts, BDD, atomic TDD cycles
