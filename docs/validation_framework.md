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

<!-- SHOCKBRIDGE_PUBLIC_FOOTER_START -->

---

## Citation and attribution

If you use, reference, quote, adapt, or build from this public research evidence layer, please cite:

Pereira, R. (2026). *ShockBridge Research Lab: Public Evidence Layer for Macro-Financial Shock Transmission Research* [Computer software]. GitHub. https://github.com/rolffcoelho-bravo/shockbridge-research-lab

Author: Rodolfo Pereira  
Website: www.shockbridgepulse.com  
Email: rolffcoelho@hotmail.com  

© 2026 Rodolfo Pereira. Free to read and use with attribution. Please cite the author and repository when referencing this work.

<!-- SHOCKBRIDGE_PUBLIC_FOOTER_END -->
