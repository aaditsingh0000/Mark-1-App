"""Public-safe configuration helpers."""
from __future__ import annotations

import platform

from memory.config_manager import get_config_value


def _platform_os() -> str:
    return {"Windows": "windows", "Darwin": "mac", "Linux": "linux"}.get(
        platform.system(), "linux"
    )


def get_config() -> dict:
    """Return non-secret/local settings from the user's ignored config file."""
    from memory.config_manager import load_api_keys
    return load_api_keys()


def get_os() -> str:
    return str(get_config_value("os_system", _platform_os()) or _platform_os()).lower()


def is_windows() -> bool:
    return get_os() == "windows"


def is_mac() -> bool:
    return get_os() == "mac"


def is_linux() -> bool:
    return get_os() == "linux"
