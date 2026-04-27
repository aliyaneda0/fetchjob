from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "classifier.pkl"


@lru_cache(maxsize=1)
def load_model() -> Any:
    """Load the trained model once and cache it for reuse."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Run `python backend/train.py` first."
        )
    return joblib.load(MODEL_PATH)


def predict_prompt(prompt: str) -> dict[str, Any]:
    """Return the predicted class plus class probabilities."""
    model = load_model()
    classes = list(model.classes_)
    probabilities = model.predict_proba([prompt])[0]
    predicted_class = model.predict([prompt])[0]
    probability_map = {
        label: round(float(probability), 4)
        for label, probability in zip(classes, probabilities)
    }

    return {
        "predicted_class": str(predicted_class),
        "confidence": probability_map[str(predicted_class)],
        "probabilities": probability_map,
    }
