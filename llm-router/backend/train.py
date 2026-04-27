from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "prompts.csv"
MODEL_PATH = BASE_DIR / "models" / "classifier.pkl"


def build_pipeline() -> Pipeline:
    """Create the baseline week-1 text classification pipeline."""
    return Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    ngram_range=(1, 2),
                    min_df=1,
                    max_df=0.95,
                    strip_accents="unicode",
                ),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=2000,
                    class_weight="balanced",
                    multi_class="auto",
                ),
            ),
        ]
    )


def main() -> None:
    print("Step 1: Loading labeled prompt data...")
    dataset = pd.read_csv(DATA_PATH)
    print(f"Loaded {len(dataset)} rows from {DATA_PATH}.")
    print("\nClass balance:")
    print(dataset["label"].value_counts().sort_index())

    print("\nStep 2: Splitting train/test data...")
    x_train, x_test, y_train, y_test = train_test_split(
        dataset["prompt"],
        dataset["label"],
        test_size=0.2,
        random_state=42,
        stratify=dataset["label"],
    )
    print(f"Train rows: {len(x_train)}")
    print(f"Test rows: {len(x_test)}")

    print("\nStep 3: Training TF-IDF + Logistic Regression baseline...")
    pipeline = build_pipeline()
    pipeline.fit(x_train, y_train)

    print("\nStep 4: Evaluating the classifier...")
    predictions = pipeline.predict(x_test)
    print("\nClassification report:")
    print(classification_report(y_test, predictions, digits=3))

    labels = ["weak", "moderate", "strong"]
    print("Confusion matrix (rows=true, cols=predicted):")
    print(confusion_matrix(y_test, predictions, labels=labels))

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"\nStep 5: Saved model to {MODEL_PATH}")
    print("Why this matters: the router can now load the classifier without retraining each request.")


if __name__ == "__main__":
    main()
