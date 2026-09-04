"""Local configuration + secret handling for MARK L.

Secrets are never required to be committed to source control.  Gemini API keys
can be supplied through GEMINI_API_KEY or stored in the ignored local
config/api_keys.json file created by the first-run UI.
"""
from __future__ import annotations

import json
import os
import platform
import sys
from pathlib import Path
from typing import Any


def get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


BASE_DIR = get_base_dir()
CONFIG_DIR = BASE_DIR / "config"
CONFIG_FILE = CONFIG_DIR / "api_keys.json"


def _platform_os() -> str:
    return {
        "Windows": "windows",
        "Darwin": "mac",
        "Linux": "linux",
    }.get(platform.system(), "linux")


def ensure_config_dir() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_api_keys() -> dict[str, Any]:
    """Load local settings.  Returns an empty mapping when not configured."""
    if not CONFIG_FILE.exists():
        return {}
    try:
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[Config] Could not read {CONFIG_FILE.name}: {exc}")
        return {}


def _write_config(data: dict[str, Any]) -> None:
    ensure_config_dir()
    tmp = CONFIG_FILE.with_suffix(".tmp")
    tmp.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    tmp.replace(CONFIG_FILE)


def save_api_keys(gemini_api_key: str) -> None:
    """Persist the user's Gemini key locally in an ignored file."""
    key = (gemini_api_key or "").strip()
    data = load_api_keys()
    if key:
        data["gemini_api_key"] = key
    else:
        data.pop("gemini_api_key", None)
    _write_config(data)


def get_gemini_key() -> str | None:
    """Prefer environment secrets, then fall back to the ignored local file."""
    env_key = os.getenv("GEMINI_API_KEY", "").strip()
    if env_key:
        return env_key
    local_key = str(load_api_keys().get("gemini_api_key", "")).strip()
    return local_key or None


def is_configured() -> bool:
    key = get_gemini_key()
    return bool(key and len(key) > 15)


def get_config_value(key: str, default: Any = None) -> Any:
    return load_api_keys().get(key, default)


def get_assistant_name() -> str:
    return str(get_config_value("assistant_name", "JARVIS") or "JARVIS").strip()


def get_user_name() -> str:
    return str(get_config_value("user_name", "") or "").strip()


def get_os() -> str:
    return str(get_config_value("os_system", _platform_os()) or _platform_os()).lower()


def save_setting(key: str, value: Any) -> None:
    """Persist one non-secret local setting."""
    if not key or key == "gemini_api_key":
        raise ValueError("Use save_api_keys() for secret credentials.")
    data = load_api_keys()
    data[key] = value
    _write_config(data)


def save_assistant_config(assistant_name: str, user_name: str) -> None:
    data = load_api_keys()
    data["assistant_name"] = (assistant_name or "").strip() or "JARVIS"
    data["user_name"] = (user_name or "").strip()
    _write_config(data)


def get_brief_enabled() -> bool:
    return bool(get_config_value("morning_brief_enabled", True))


def save_brief_enabled(enabled: bool) -> None:
    data = load_api_keys()
    data["morning_brief_enabled"] = bool(enabled)
    _write_config(data)
