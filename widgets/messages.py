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
# ── TreeNode is only used for *type hints* ─────────────────────
from textual.widgets._tree import TreeNode  # ← internal, but safe for typing

# ── Message asking the app to open the editor ──────────────────
class EditNode(Message):
    def __init__(self, node: TreeNode[dict[str, Any]]) -> None:
        self.node = node
        super().__init__()


# ── Message for file selection ────────────────────────────────
class FileSelected(Message):
    def __init__(self, path: str, action: str) -> None:
        self.path = os.path.abspath(path)  # Convert to absolute path
        self.action = action  # "save" or "load"
        super().__init__()
