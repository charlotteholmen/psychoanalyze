# Advanced Analysis Techniques

This document covers advanced analysis methods including streaming variational inference, Weber power-law modeling, strength-duration curves, and comprehensive Bayesian workflows.

## Streaming Variational Monte Carlo (SVMC)

### What Problem This Solves

You want to **process streaming time-series data one observation at a time** and **simultaneously**:

1. Track a latent state (`x_t`) in real time
2. Learn the system's dynamics (`f`) online
3. Quantify uncertainty (not just point estimates)
4. Support **nonlinear dynamics** and **non-Gaussian observations**
5. Maintain **constant per-step runtime** (real-time feasible)

Classical filters (EKF/UKF) fail on (2–4).
Pure particle filters struggle with proposal quality.
Pure variational inference struggles with temporal dependence.

**SVMC combines particle filtering + variational optimization** to get the best of both.

### Core Idea in One Sentence

> Treat the particle filter's *proposal distribution* as a **trainable model**, and **optimize it online** using stochastic gradients derived from particle weights.

This turns particle filtering into a **learnable system**, not a hand-tuned one.

### High-Level System Architecture

Think of SVMC as three cooperating subsystems:

#### 1. Particle Filter (SMC core)

* Maintains particles `{x_t^i, w_t^i}`
* Handles recursive Bayesian filtering
* Guarantees asymptotic correctness as particle count → ∞

#### 2. Proposal Network (learned inference model)

* Learns `r(x_t | x_{t-1}, y_t)`
* Implemented as a neural network
* Trained **online**, per timestep
* Replaces hand-designed proposals (bootstrap PF)

#### 3. Dynamics Model (generative model)

Two options:

* **Parametric** (MLP, RNN, etc.)
* **Nonparametric** (Sparse Gaussian Process)

The GP version is the most novel part of the method.

### Key Algorithmic Insight

#### The Filtering ELBO (Engineering Interpretation)

Instead of optimizing a classical VI ELBO (which is intractable online), SVMC:

* Uses **log(sum of particle weights)** as a surrogate objective
* This quantity:

  * Is computable online
  * Has unbiased gradients
  * Converges to the true filtering log-likelihood as particles ↑

**Result:** You can safely use SGD in a streaming particle filter.

This is the theoretical glue between SMC and VI.

### Streaming Loop (Pseudo-Code View)

At every timestep `t`:

```
for k in 1..NSGD:
    1. Resample ancestor particles
    2. Propose new states via learned proposal
    3. Compute importance weights
    4. Compute log(sum(weights))
    5. Take SGD step on proposal + model parameters

Final step:
    Resample full particle set
```

This is **online EM-like learning**, but:

* No batch storage
* No replay buffer
* No backward passes through time

### Sparse GP Dynamics

#### Problem

Full GPs scale as:

* Time: O(t³)
* Memory: O(t²)

Impossible for streaming.

#### Solution

Use **sparse GP with inducing points**, but with a twist:

> Each particle carries its **own posterior over GP inducing variables**.

So instead of:

* One global GP posterior (too rigid)

You get:

* A **mixture of GP posteriors**, represented by particles

#### Implementation-Relevant Consequences

* Each particle stores:

  ```python
  mu_z_i     # inducing mean
  Sigma_z_i  # inducing covariance
  ```
* These update **recursively** via closed-form Gaussian updates
* No gradient descent needed for GP updates
* Constant cost per timestep

This is a major engineering win.

### When to Use SVMC

SVMC is a strong fit if you are building:

* Online system identification
* Adaptive control systems
* Neuroscience latent dynamics models
* Robotics / tracking with unknown dynamics
* Real-time forecasting with uncertainty
* Streaming Bayesian inference engines

Especially compelling if:

* You care about **interpretable dynamics**
* You cannot afford offline retraining
* You want principled uncertainty propagation

### Implementation Considerations

If you're implementing SVMC, think in layers:

```
Inference layer:   Particle filter + resampling
Learning layer:    SGD on log(sum(weights))
Dynamics layer:    GP or neural net
Proposal layer:    Neural net inference model
```

Each layer is **loosely coupled**, which makes this very amenable to:

* Modular implementation
* Swapping dynamics models
* Experimenting with different proposals

---

## Weber Power-Law Modeling

The Weber fraction describes how stimulus discrimination sensitivity relates to stimulus magnitude:

$$\text{JND} = k \cdot I^n$$

where:
- **JND** (Just Noticeable Difference) = minimum perceptible change
- **I** = stimulus intensity
- **k** = Weber coefficient
- **n** = exponent (typically 0.5–1.5)

### Application in PsychoAnalyze

Weber modeling is useful when:
- Fitting across a wide range of stimulus intensities
- Modeling detection thresholds that scale with signal strength
- Comparing sensitivity across subjects or conditions
- Normalizing data for cross-subject analysis

---

## Strength-Duration Curves

Strength-duration curves describe how stimulus detectability depends on the interaction between amplitude and duration:

$$I = \frac{Q + \beta \cdot D}{D}$$

where:
- **I** = stimulus intensity
- **D** = stimulus duration
- **Q** = chronaxie (charge = ampere × second)
- **β** = strength-duration parameter

This is fundamental in electrical stimulation studies where different pulse widths and amplitudes produce equivalent percepts.

---

## Gelman Bayesian Workflow

The complete principled Bayesian workflow includes:

1. **Design** - Specify priors, model structure, and predictive expectations
2. **Prior predictive checks** - Verify prior generates reasonable data
3. **Inference** - MCMC sampling with convergence diagnostics
4. **Fit diagnostics** - Check R-hat, ESS, trace plots
5. **Posterior predictive checks** - Verify model captures observed data patterns
6. **Model comparison** - WAIC, LOO-CV, or Bayes factors for model selection
7. **Sensitivity analysis** - How robust are results to prior specification?

### Implementation in PsychoAnalyze

The dashboard implements the full workflow with:
- Interactive prior specification
- Real-time MCMC monitoring
- Automatic convergence check summaries
- Posterior predictive visualizations
- Model comparison metrics
- Shrinkage diagnostics

See [System Architecture](./architecture.md) for dashboard-specific details.

---

## References and Further Reading

- Gelman, A., et al. (2020). *Bayesian Workflow*. arXiv:2011.01808.
- Gelman, A., & Hill, J. (2006). *Data Analysis Using Regression and Multilevel/Hierarchical Models*. Cambridge University Press.
- Miller, J., & Abraham, D. L. (1990). A neural basis for psychophysical judgments. In: *Computational Neuroscience*.
- Prins, N., & Kingdom, F. A. A. (2018). *Applying the Model-Comparison Approach to Test Specific Research Hypotheses in Psychophysical Research Using the Palamedes Toolbox*. Frontiers in Psychology.
