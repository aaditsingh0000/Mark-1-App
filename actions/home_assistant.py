"""Optional Home Assistant REST integration. Disabled until explicitly configured."""
from __future__ import annotations
import os, requests

def home_assistant(action: str, entity_id: str = "", service: str = "", data: dict | None = None) -> str:
    base, token = os.getenv("HOME_ASSISTANT_URL", "").rstrip("/"), os.getenv("HOME_ASSISTANT_TOKEN", "")
    if not base or not token: return "Home Assistant is not configured. Set HOME_ASSISTANT_URL and HOME_ASSISTANT_TOKEN first."
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    try:
        if action == "status": r = requests.get(f"{base}/api/states/{entity_id}", headers=headers, timeout=8)
        elif action == "service":
            if not service or "." not in service: return "Service must look like domain.service, for example light.turn_on."
            domain, service_name = service.split(".", 1); r = requests.post(f"{base}/api/services/{domain}/{service_name}", headers=headers, json=data or {}, timeout=10)
        elif action == "list": r = requests.get(f"{base}/api/states", headers=headers, timeout=10)
        else: return "Unsupported Home Assistant action. Use status, service, or list."
        r.raise_for_status()
        if action == "list": return "\n".join(f"{x.get('entity_id')}: {x.get('state')}" for x in r.json()[:50]) or "No entities found."
        return r.text[:1500] or "Done."
    except Exception as e: return f"Home Assistant error: {e}"
