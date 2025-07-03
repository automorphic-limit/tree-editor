from __future__ import annotations

import sys
from typing import Any

from textual.app import App, ComposeResult
from textual import on
from textual.widgets import (
    Tree,
    Header,
    Footer,
)

# ── TreeNode is only used for *type hints* ─────────────────────
from textual.widgets._tree import TreeNode  # ← internal, but safe for typing

from widgets.prompt_tree import PromptTree
from widgets.path_header import PathHeader
from widgets.edit_overlay import EditOverlay
from widgets.file_overlays import FileSaveOverlay
from widgets.messages import EditNode, FileSelected

# ── Test Components ────────────────────────────────────────────
class TestPromptTree(PromptTree):
    """Test version of PromptTree with sample data."""
    def __init__(self):
        super().__init__("test")
        self.root.data = {"key": "test", "value": {
            "string": "Hello World",
            "number": 42,
            "list": [1, 2, 3],
            "nested": {
                "key1": "value1",
                "key2": "value2"
            }
        }}
        self._populate_tree(self.root.data["value"], parent=self.root)
        self.root.expand_all()

class TestEditOverlay(EditOverlay):
    """Test version of EditOverlay with sample node."""
    def __init__(self):
        # Create a test node
        test_tree = PromptTree("test")
        test_tree.root.data = {"key": "test", "value": "Test Value"}
        super().__init__(test_tree.root)

class TestFileBrowser(FileSaveOverlay):
    """Test version of FileSaveOverlay."""
    def __init__(self):
        super().__init__()


# ── Test App ──────────────────────────────────────────────────
class TestApp(App):
    """App for testing individual components."""
    TITLE = "Component Tests"
    SUB_TITLE = "Test each component individually"

    BINDINGS = [
        ("1", "test_tree", "Test Tree"),
        ("2", "test_editor", "Test Editor"),
        ("3", "test_browser", "Test Browser"),
        ("q", "quit", "Quit"),
    ]

    CSS = """
    TestPromptTree {
        height: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    def action_test_tree(self) -> None:
        """Test the PromptTree component."""
        self.mount(TestPromptTree())

    def action_test_editor(self) -> None:
        """Test the EditOverlay component."""
        self.mount(TestEditOverlay())

    def action_test_browser(self) -> None:
        """Test the FileSaveOverlay component."""
        self.mount(TestFileBrowser())

class PromptApp(App):
    TITLE = "Tree"
    SUB_TITLE = "Viewer and Editor"

    CSS = """
    PromptTree {
        height: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        self.path_header = PathHeader()
        yield Header()
        yield self.path_header
        self.prompt_tree = PromptTree("prompt")
        self.prompt_tree.root.data = {"key": "root", "value": {}}
        yield self.prompt_tree
        yield Footer()

    def on_mount(self) -> None:
        self._populate_tree({}, parent=self.prompt_tree.root)
        self.update_path_header()
        #self.prompt_tree.root.expand_all()

    def get_node_path(self, node):
        path = []
        while node and node.parent is not None:
            path.append(str(node.data.get("key", "")))
            node = node.parent
        return list(reversed(path))

    def update_path_header(self):
        node = self.prompt_tree.cursor_node
        self.path_header.path = "•".join(self.get_node_path(node)) if node else ""

    def watch_prompt_tree__cursor_line(self, value):
        self.update_path_header()

    @on(EditNode)
    def open_editor(self, event: EditNode) -> None:
        self.mount(EditOverlay(event.node))

    @on(FileSelected)
    def handle_file_selection(self, event: FileSelected) -> None:
        if not event.path:
            self.notify("No file path provided", severity="error")
            return
        if event.action == "save":
            self.prompt_tree.save_to_file(event.path)
        elif event.action == "load":
            self.prompt_tree.load_from_file(event.path)
        else:
            self.notify("Invalid action", severity="error")

    def _populate_tree(self, data: Any, parent: TreeNode | None = None) -> None:
        if parent is None:
            parent = self.prompt_tree.root

        if isinstance(data, dict):
            for k, v in data.items():
                node = parent.add(str(k), {"key": k, "value": v})
                self._populate_tree(v, node)
        elif isinstance(data, list):
            for i, v in enumerate(data):
                node = parent.add(f"[{i}]", {"key": i, "value": v})
                self._populate_tree(v, node)

    @on(Tree.NodeSelected)
    def _on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        self.update_path_header()

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        TestApp().run()
    else:
        PromptApp().run()

# ── run it ─────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
