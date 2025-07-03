from __future__ import annotations

from textual.reactive import reactive
from textual.widgets import Static

# ── The application ────────────────────────────────────────────
class PathHeader(Static):
    path: str = reactive("")

    def render(self) -> str:
        return self.path
