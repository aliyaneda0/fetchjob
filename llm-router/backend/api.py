from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from backend.db import fetch_recent_routes, init_db, log_route
from backend.router import route_prompt


app = FastAPI(
    title="LLM Router API",
    description="Week-1 prototype API for routing prompts by predicted difficulty.",
    version="0.1.0",
)


class RouteRequest(BaseModel):
    prompt: str = Field(..., min_length=3, description="The user prompt to classify and route.")


class RouteResponse(BaseModel):
    predicted_class: str
    confidence: float
    probabilities: dict[str, float]
    model_used: str
    route_name: str
    latency_ms: int
    estimated_cost: float
    fallback_triggered: bool
    response: str


@app.on_event("startup")
def startup_event() -> None:
    init_db()


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/route", response_model=RouteResponse)
def route(request: RouteRequest) -> dict[str, Any]:
    try:
        result = route_prompt(request.prompt)
        log_route(result)
        return {
            "predicted_class": result["predicted_class"],
            "confidence": result["confidence"],
            "probabilities": result["probabilities"],
            "model_used": result["model_used"],
            "route_name": result["route_name"],
            "latency_ms": result["latency_ms"],
            "estimated_cost": result["estimated_cost"],
            "fallback_triggered": result["fallback_triggered"],
            "response": result["response"],
        }
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Routing failed: {exc}") from exc


@app.get("/history")
def history(limit: int = 20) -> list[dict[str, Any]]:
    return fetch_recent_routes(limit=limit)
