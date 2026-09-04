"""Local, privacy-friendly usage analytics for the assistant."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
import sys
from threading import Lock
_LOCK = Lock()

def _path() -> Path:
    base = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent.parent
    return base / "memory" / "analytics.json"

def record(event: str, value: str = "") -> None:
    path = _path()
    with _LOCK:
        try: data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"events": [], "counts": {}}
        except Exception: data = {"events": [], "counts": {}}
        data.setdefault("events", []).append({"time": datetime.now().isoformat(timespec="seconds"), "event": event, "value": value[:120]})
        data["events"] = data["events"][-500:]
        counts = data.setdefault("counts", {}); counts[event] = int(counts.get(event, 0)) + 1
        path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def summary() -> str:
    try: data = json.loads(_path().read_text(encoding="utf-8"))
    except Exception: return "No analytics recorded yet."
    counts = data.get("counts", {})
    return "Usage summary:\n" + "\n".join(f"- {k}: {v}" for k, v in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]) if counts else "No analytics recorded yet."
