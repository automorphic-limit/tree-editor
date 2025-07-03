from __future__ import annotations

from typing import Any

from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import Vertical
from textual.widgets import (
    Footer,
    TextArea,
)

# ── TreeNode is only used for *type hints* ─────────────────────
from textual.widgets._tree import TreeNode  # ← internal, but safe for typing

# ── Modal editor with a TextArea ───────────────────────────────
class EditOverlay(Widget):
    BINDINGS = [
        ("ctrl+s", "save", "Save"),
        ("escape", "cancel", "Cancel"),
    ]

    DEFAULT_CSS = """
    EditOverlay {
        layer: overlay;
        margin: 10 20;
        border: heavy $accent;
        background: $panel-darken-1 80%;
    }
    EditOverlay Vertical {
        height: 100%;
    }
    EditOverlay TextArea {
        height: 1fr;
        width: 100%;
    }
    """

    def __init__(self, node: TreeNode[dict[str, Any]]):
        super().__init__()
        self.node = node
        self._ta = TextArea(
            text=str(node.data["value"]),
            id="input",
        )

    def compose(self) -> ComposeResult:
        yield Vertical(
            self._ta,
            Footer(),
        )

    def on_mount(self) -> None:
        self._ta.focus()

    def action_save(self) -> None:
        self.commit()

    def action_cancel(self) -> None:
        self.dismiss()

    # -----------------------------------------------------------------
    def commit(self) -> None:
        raw = self._ta.text
        # try to parse JSON / Python literal so numbers & lists survive
        try:
            import json, ast

            try:
                value = json.loads(raw)
            except json.JSONDecodeError:
                value = ast.literal_eval(raw)
        except Exception:
            value = raw  # keep as plain text

        # Update the node's value
        self.node.data["value"] = value

        # If the value is a dict or list, update the tree structure
        if isinstance(value, (dict, list)):
            # Remove all children
            for child in list(self.node.children):
                child.remove()
            
            # Add new children based on the value
            if isinstance(value, dict):
                for k, v in value.items():
                    child = self.node.add(str(k), {"key": k, "value": v})
                    if isinstance(v, (dict, list)):
                        child.allow_expand = True
            elif isinstance(value, list):
                for i, v in enumerate(value):
                    child = self.node.add(f"[{i}]", {"key": i, "value": v})
                    if isinstance(v, (dict, list)):
                        child.allow_expand = True

        self.node.refresh()  # repaint that one line
        self.dismiss()

    def dismiss(self) -> None:
        self.remove()
        self.app.set_focus(self.node.tree)  # back to tree
