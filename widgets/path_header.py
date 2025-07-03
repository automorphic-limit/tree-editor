from __future__ import annotations

import os
from typing import Any

from rich.text import Text
from textual.app import App, ComposeResult
from textual.message import Message
from textual.widget import Widget
from textual import on
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widgets import (
    Tree,
    Header,
    Footer,
    TextArea,
    DirectoryTree,
    Static,
)


# ── The application ────────────────────────────────────────────
class PathHeader(Static):
    path: str = reactive("")

    def render(self) -> str:
        return self.path
