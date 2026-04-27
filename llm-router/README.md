# LLM Router

This folder contains a week-1 prototype for routing prompts to different LLM backends based on prompt complexity.

The project is intentionally simple:

1. We label prompts as `weak`, `moderate`, or `strong`.
2. We train a text classifier with TF-IDF + Logistic Regression.
3. We route prompts to a local or API model based on the predicted class.
4. We expose the router with FastAPI.
5. We show predictions, latency, and history in Streamlit.

Artifacts such as `data/app.db` and `models/classifier.pkl` are created when you run the training script or API for the first time.

Start with the step-by-step guide in `docs/WEEK1_GUIDE.md`.
