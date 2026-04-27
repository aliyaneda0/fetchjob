from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "app.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS route_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT NOT NULL,
                predicted_class TEXT NOT NULL,
                confidence REAL NOT NULL,
                model_used TEXT NOT NULL,
                latency_ms INTEGER NOT NULL,
                estimated_cost REAL NOT NULL,
                fallback_triggered INTEGER NOT NULL,
                response TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()


def log_route(result: dict[str, Any]) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO route_logs (
                prompt,
                predicted_class,
                confidence,
                model_used,
                latency_ms,
                estimated_cost,
                fallback_triggered,
                response
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                result["prompt"],
                result["predicted_class"],
                result["confidence"],
                result["model_used"],
                result["latency_ms"],
                result["estimated_cost"],
                int(result["fallback_triggered"]),
                result["response"],
            ),
        )
        connection.commit()


def fetch_recent_routes(limit: int = 20) -> list[dict[str, Any]]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                prompt,
                predicted_class,
                confidence,
                model_used,
                latency_ms,
                estimated_cost,
                fallback_triggered,
                response,
                created_at
            FROM route_logs
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]
