"""Optional local wake-word adapter.

The core app does not require this dependency. Install openwakeword separately when
local wake-word gating is desired, then call WakeWordDetector.process() from the
chosen microphone pipeline.
"""
from __future__ import annotations

class WakeWordDetector:
    def __init__(self, model_name: str = "hey_jarvis") -> None:
        try:
            from openwakeword.model import Model
        except ImportError as exc:
            raise RuntimeError("Optional dependency missing: pip install openwakeword") from exc
        self._model = Model(wakeword_models=[model_name])
        self.model_name = model_name

    def process(self, pcm16) -> float:
        scores = self._model.predict(pcm16)
        if isinstance(scores, dict):
            return float(scores.get(self.model_name, 0.0))
        return 0.0
