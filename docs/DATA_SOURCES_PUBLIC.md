# Data Sources — Public Note

The ShockBridge research framework is designed around real observed data, not synthetic data.

## Publicly described data categories

The private research stack uses market and macro-financial inputs from categories such as:

- equity indexes and sector exposures
- volatility proxies
- interest-rate series
- credit-spread proxies
- commodity prices
- gold benchmark data
- currency and dollar-pressure proxies
- emerging-market exposures
- critical-materials market proxies
- AI and compute-linked market assets

## Macro confirmation layer

The v4.3 private confirmation layer uses:

- official macro-financial series
- a local cached LBMA AM gold benchmark series
- a separate macro/gold stress anchor

The macro confirmation layer is treated as a sidecar. It does not overwrite the core market diagnostic.

## Reproducibility philosophy

The private workflow preserves:

- input manifests
- lock files
- validation reports
- local cached benchmark files where live APIs are unreliable
- audit reports
- model-status reports

This public repository does not include the private raw-data pipeline or proprietary methodology code.

<!-- SHOCKBRIDGE_PUBLIC_FOOTER_START -->

---

## Citation and attribution

If you use, reference, quote, adapt, or build from this public research evidence layer, please cite:

Pereira, R. (2026). *ShockBridge Research Lab: Public Evidence Layer for Macro-Financial Shock Transmission Research* [Computer software]. GitHub. https://github.com/rolffcoelho-bravo/shockbridge-research-lab

Author: Rodolfo Pereira  
Website: www.shockbridgepulse.com  
Email: rolffcoelho@hotmail.com  

© 2026 Rodolfo P.. Free to read and use with attribution. Please cite the author and repository when referencing this work.

<!-- SHOCKBRIDGE_PUBLIC_FOOTER_END -->

