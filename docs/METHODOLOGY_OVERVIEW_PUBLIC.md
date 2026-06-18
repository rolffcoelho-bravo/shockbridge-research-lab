# Methodology Overview — Public Version

This document describes the public, non-proprietary architecture of the ShockBridge research framework.

## 1. Problem

Market shocks rarely move in a single line. They travel through volatility, correlations, funding channels, commodities, rates, credit, equity sectors, currencies, and macro expectations.

The framework is designed to detect when stress begins to synchronize across blocks before the macro data fully confirms the regime.

## 2. Research architecture

The private engine is organized around three layers:

### Layer 1 — Market diagnostic

The market diagnostic reads high-dimensional asset data and estimates whether stress is quiet, building, or broadly transmitted.

Publicly described inputs include:

- equities
- volatility proxies
- rates and credit proxies
- commodities
- critical materials
- currencies
- emerging-market exposures
- AI and compute-linked assets

### Layer 2 — Multiblock transmission

The system studies whether several market blocks begin to move through a common latent stress structure.

This includes a multiblock dependence bridge, horizon comparison, and concentration analysis. The goal is not to treat correlation as the whole story, but to detect when cross-market synchronization becomes economically meaningful.

### Layer 3 — Macro confirmation

A separate macro confirmation sidecar uses official macro-financial series and a local cached LBMA AM gold benchmark series.

The sidecar does not overwrite the market diagnostic. It checks whether official macro stress is confirming, partially confirming, or failing to confirm the market-led stress signal.

## 3. Interpretation logic

The research framework distinguishes between:

- market-led stress-building
- macro-confirmed stress
- curve-led warning
- broad financial stress
- commodity/gold shock confirmation
- scenario-review regimes

This distinction matters because a market-led signal may justify research review and scenario pricing before it justifies defensive action.

## 4. Public result statement

The current private stack indicates market-led stress-building, while broad macro confirmation remains incomplete. The public interpretation is therefore careful: the signal is worth monitoring, but it is not presented as a fully confirmed systemic macro-stress regime.

## 5. What remains private

The following are not public:

- exact thresholds
- weights
- signal formulas
- feature engineering
- private data-processing scripts
- machine-learning validation internals
- research-desk action rules
- portfolio or hedge-action logic

<!-- SHOCKBRIDGE_PUBLIC_FOOTER_START -->

---

## Citation and attribution

If you use, reference, quote, adapt, or build from this public research evidence layer, please cite:

Pereira, R. (2026). *ShockBridge Research Lab: Public Evidence Layer for Macro-Financial Shock Transmission Research* [Computer software]. GitHub. https://github.com/rolffcoelho-bravo/shockbridge-research-lab

Author: Rodolfo Pereira  
Website: www.shockbridgepulse.com  
Email: rolffcoelho@hotmail.com  

© 2026 Rodolfo P. Free to read and use with attribution. Please cite the author and repository when referencing this work.

<!-- SHOCKBRIDGE_PUBLIC_FOOTER_END -->


