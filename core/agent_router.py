"""Lightweight task router used to classify complex requests without executing them."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TaskRoute:
    agent: str
    reason: str


class AgentRouter:
    """Deterministic first-pass router; the LLM remains responsible for final tool choice."""

    RULES = (
        ("code", "coding", "developer"),
        ("bug", "error", "traceback", "developer"),
        ("file", "pdf", "document", "excel", "file"),
        ("screen", "camera", "image", "vision", "vision"),
        ("weather", "weather"),
        ("research", "research"),
        ("smart home", "home_assistant"),
    )

    def route(self, text: str) -> TaskRoute:
        low = text.lower()
        for *keywords, agent in self.RULES:
            if any(k in low for k in keywords):
                return TaskRoute(agent, f"Matched keywords: {', '.join(keywords)}")
        return TaskRoute("general", "No specialist keyword matched")
