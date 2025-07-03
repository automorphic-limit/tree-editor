from __future__ import annotations

import os
from typing import Any

from textual.message import Message

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
