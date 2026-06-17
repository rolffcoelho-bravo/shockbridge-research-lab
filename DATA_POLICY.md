# Data Policy

This repository follows a real-data research discipline.

## Principles

- Use real public data whenever possible.
- Avoid synthetic data unless clearly labelled as toy/demo data.
- Store raw and processed data separately.
- Preserve reproducibility through static files when appropriate.
- Document sources and transformations.
- Avoid hidden manual edits.
- Avoid look-ahead bias in time-series modelling.

## Folder Structure

data/raw/  
Stores raw downloaded or manually exported datasets.

data/processed/  
Stores cleaned and transformed datasets used by the research pipeline.

## Public Repo Constraint

This public repository may use simplified datasets or public-safe examples. Proprietary ShockBridge Pulse data layers and commercial signal logic remain private.
