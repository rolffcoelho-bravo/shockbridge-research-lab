"""Machine-learning regime classification demo."""

from dataclasses import dataclass

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


@dataclass
class RegimeClassifierResult:
    """Container for public demo classifier results."""

    accuracy: float
    n_train: int
    n_test: int


def train_basic_regime_classifier(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> RegimeClassifierResult:
    """Train a simple baseline classifier for public demonstration."""
    if X_train.empty or X_test.empty:
        raise ValueError("Train/test feature data cannot be empty.")

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    return RegimeClassifierResult(
        accuracy=float(accuracy),
        n_train=len(X_train),
        n_test=len(X_test),
    )
