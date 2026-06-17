# Validation Framework

Financial time-series models must be validated with discipline.

This repository emphasizes validation principles that matter in real research and capital-facing environments.

## Core Validation Rules

- No look-ahead bias
- No random train/test split for time-series forecasting tasks
- Use chronological splits
- Use walk-forward validation where appropriate
- Compare against simple benchmarks
- Track model stability
- Document limitations
- Separate research experiments from production claims

## Public-Safe Validation Modules

The public repository will include simplified validation utilities that demonstrate:

- time-series split logic
- benchmark comparison
- basic leakage checks
- performance reporting
