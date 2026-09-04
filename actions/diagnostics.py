"""Project and environment diagnostics. Safe: it does not modify the system."""
from __future__ import annotations
import importlib.util, platform, sys
from pathlib import Path

from memory.config_manager import get_gemini_key, get_os

def run_diagnostics() -> str:
    base = Path(__file__).resolve().parent.parent
    required = ["PyQt6","sounddevice","google.genai","PIL","requests","playwright","pyautogui","cv2","numpy","mss","psutil","fastapi","uvicorn","cryptography"]
    checks = {name: bool(importlib.util.find_spec(name)) for name in required}
    lines = [f"Python: {sys.version.split()[0]}", f"Platform: {platform.platform()}", f"Project: {base}", "Dependencies:"]
    lines += [f"  {'OK' if ok else 'MISSING'} {name}" for name, ok in checks.items()]
    key = get_gemini_key()
    lines.append(f"Gemini key: {'configured' if key and len(key) > 15 else 'missing/invalid'}")
    lines.append(f"OS setting: {get_os()}")
    overall_ready = all(checks.values()) and bool(key and len(key) > 15)
    lines.append(f"Overall: {'READY' if overall_ready else 'NEEDS_SETUP'}")
    return "\n".join(lines)
