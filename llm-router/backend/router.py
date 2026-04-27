from __future__ import annotations

import os
import time
from typing import Any

import httpx

from backend.predict import predict_prompt


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_WEAK_MODEL = os.getenv("OLLAMA_WEAK_MODEL", "tinyllama")
OLLAMA_MODERATE_MODEL = os.getenv("OLLAMA_MODERATE_MODEL", "phi3.5")
STRONG_API_URL = os.getenv("STRONG_API_URL", "https://api.openai.com/v1/chat/completions")
STRONG_API_MODEL = os.getenv("STRONG_API_MODEL", "gpt-4o-mini")
STRONG_API_KEY = os.getenv("STRONG_API_KEY", "")
CONFIDENCE_THRESHOLD = float(os.getenv("ROUTER_CONFIDENCE_THRESHOLD", "0.55"))


MODEL_REGISTRY = {
    "weak": {"route_name": "local_weak", "provider_model": OLLAMA_WEAK_MODEL, "estimated_cost": 0.0},
    "moderate": {"route_name": "local_moderate", "provider_model": OLLAMA_MODERATE_MODEL, "estimated_cost": 0.0},
    "strong": {"route_name": "api_strong", "provider_model": STRONG_API_MODEL, "estimated_cost": 0.02},
}


def choose_model(predicted_class: str, confidence: float) -> tuple[dict[str, Any], bool]:
    """Map the class prediction to a model and fail safe to the strong model when unsure."""
    fallback_triggered = confidence < CONFIDENCE_THRESHOLD
    if fallback_triggered:
        return MODEL_REGISTRY["strong"], True
    return MODEL_REGISTRY[predicted_class], False


def call_ollama(prompt: str, model_name: str) -> str:
    with httpx.Client(timeout=60.0) as client:
        response = client.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={"model": model_name, "prompt": prompt, "stream": False},
        )
        response.raise_for_status()
        payload = response.json()
        return payload.get("response", "").strip()


def call_strong_api(prompt: str, model_name: str) -> str:
    if not STRONG_API_KEY:
        return (
            "Strong-model fallback selected, but no STRONG_API_KEY is configured. "
            "Set the API key to call the external provider."
        )

    headers = {
        "Authorization": f"Bearer {STRONG_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": "You are the strong fallback model in an LLM routing prototype.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }

    with httpx.Client(timeout=60.0) as client:
        response = client.post(STRONG_API_URL, headers=headers, json=body)
        response.raise_for_status()
        payload = response.json()
        return payload["choices"][0]["message"]["content"].strip()


def invoke_model(prompt: str, selected_model: dict[str, Any]) -> str:
    route_name = selected_model["route_name"]
    provider_model = selected_model["provider_model"]

    if route_name in {"local_weak", "local_moderate"}:
        return call_ollama(prompt, provider_model)
    return call_strong_api(prompt, provider_model)


def route_prompt(prompt: str) -> dict[str, Any]:
    """
    Week-1 router flow:
    1. Classify prompt difficulty.
    2. Choose a model based on class and confidence.
    3. Call the selected model.
    4. Return metadata for observability.
    """
    prediction = predict_prompt(prompt)
    predicted_class = prediction["predicted_class"]
    confidence = float(prediction["confidence"])
    selected_model, fallback_triggered = choose_model(predicted_class, confidence)

    started_at = time.perf_counter()
    response_text = invoke_model(prompt, selected_model)
    latency_ms = int((time.perf_counter() - started_at) * 1000)

    return {
        "prompt": prompt,
        "predicted_class": predicted_class,
        "confidence": round(confidence, 4),
        "probabilities": prediction["probabilities"],
        "model_used": selected_model["provider_model"],
        "route_name": selected_model["route_name"],
        "latency_ms": latency_ms,
        "estimated_cost": selected_model["estimated_cost"],
        "response": response_text,
        "fallback_triggered": fallback_triggered,
    }
