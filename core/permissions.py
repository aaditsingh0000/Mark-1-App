"""Central safety gate for actions that can change or destroy user data/system state."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import threading


class PermissionManager:
    """Small, dependency-free permission policy with session-scoped approvals."""

    RISKY = {
        "delete": "Delete files or folders",
        "send_message": "Send a message",
        "install": "Install or download software",
        "power": "Restart or shut down the computer",
        "system_change": "Change system settings",
        "execute": "Execute an arbitrary command",
        "home_assistant": "Control a smart-home device",
    }

    def __init__(self, base_dir: Path | None = None) -> None:
        self.base_dir = base_dir or self._base_dir()
        self.path = self.base_dir / "config" / "permissions.json"
        self._lock = threading.RLock()
        self._session_approved: set[str] = set()

    @staticmethod
    def _base_dir() -> Path:
        if getattr(sys, "frozen", False):
            return Path(sys.executable).parent
        return Path(__file__).resolve().parent.parent

    def _load(self) -> dict:
        with self._lock:
            try:
                return json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                return {"always_allow": []}

    def _save(self, data: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def requires_confirmation(self, action: str) -> bool:
        action = action.strip().lower()
        if action in self._session_approved:
            return False
        return action not in set(self._load().get("always_allow", []))

    def request(self, action: str, detail: str = "") -> str:
        action = action.strip().lower()
        label = self.RISKY.get(action, action)
        suffix = f" — {detail}" if detail else ""
        return f"CONFIRM_REQUIRED: {label}{suffix}. Ask the user for confirmation before continuing."

    def approve_once(self, action: str) -> None:
        self._session_approved.add(action.strip().lower())

    def revoke_session_approvals(self) -> None:
        self._session_approved.clear()
