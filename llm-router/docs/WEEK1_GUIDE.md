# Week 1 Build Guide

## What we are building

We are building a small routing system that decides which LLM should answer a prompt.

The idea is simple:

- Easy prompts should use a cheaper or weaker local model.
- Medium prompts should use a better local model.
- Hard prompts should use a stronger API model.

This is useful because not every request needs the same model quality or cost.

## Why this is a good week-1 project

This version is small enough to finish quickly, but it already proves the core idea:

- We can classify prompts by difficulty.
- We can map difficulty to model choice.
- We can expose the result through an API.
- We can log and visualize routing behavior.

That gives us a real system we can improve later with better labels, better features, better confidence rules, and real cost tracking.

## Project structure

```text
llm-router/
  data/
    prompts.csv
    app.db
  docs/
    WEEK1_GUIDE.md
  models/
    classifier.pkl
  backend/
    api.py
    db.py
    predict.py
    router.py
    train.py
  frontend/
    dashboard.py
  requirements.txt
  README.md
```

## Step 1: Create the project folder

### What we are doing

We split the prototype into clear parts:

- `data/` stores the labeled training data and runtime database.
- `models/` stores the trained classifier.
- `backend/` contains the ML pipeline, routing logic, API, and database helpers.
- `frontend/` contains the dashboard.

### Why we are doing it

This keeps training code, runtime code, and UI code separate. That matters because later we may replace the classifier, change the API, or swap the UI without restructuring everything.

## Step 2: Build the dataset manually

We created `data/prompts.csv` with 210 labeled prompts:

- 70 `weak`
- 70 `moderate`
- 70 `strong`

Manual labels are fine for week 1 because the goal is to validate the routing idea, not to build a perfect benchmark.

## Step 3: Train the classifier

The training script:

1. Loads the CSV with pandas.
2. Splits the dataset into train and test sets.
3. Builds a pipeline with `TfidfVectorizer` and `LogisticRegression`.
4. Evaluates the model.
5. Saves the trained pipeline with `joblib`.

We use this stack because TF-IDF plus Logistic Regression is a strong, fast, interpretable baseline.

## Step 4: Build the router

The router takes a prompt, gets class probabilities from the classifier, and then decides which model to use.

Base rule:

- `weak` -> `local_weak`
- `moderate` -> `local_moderate`
- `strong` -> `api_strong`

Confidence override:

- if confidence is below `0.55`, route to `api_strong`

This makes the system fail safe when the classifier is unsure.

## Step 5: Add the FastAPI endpoint

We created a single endpoint:

- `POST /route`

Input:

```json
{ "prompt": "Explain this SQL join issue" }
```

Output:

```json
{
  "predicted_class": "moderate",
  "confidence": 0.74,
  "model_used": "phi3.5",
  "latency_ms": 2300,
  "estimated_cost": 0.0,
  "response": "...",
  "fallback_triggered": false
}
```

## Step 6: Connect local and API models

The router supports:

- local models through the Ollama HTTP API
- a stronger API model through an OpenAI-compatible chat endpoint

Environment variables:

- `OLLAMA_BASE_URL`
- `OLLAMA_WEAK_MODEL`
- `OLLAMA_MODERATE_MODEL`
- `STRONG_API_URL`
- `STRONG_API_MODEL`
- `STRONG_API_KEY`

## How to run

```bash
pip install -r requirements.txt
python backend/train.py
uvicorn backend.api:app --reload
streamlit run frontend/dashboard.py
```

## What to improve in week 2

- add richer labels from real traffic
- track true cost from provider responses
- tune the confidence threshold
- benchmark local models more carefully
- add evals focused on `strong` prompt misses
