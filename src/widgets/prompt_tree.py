from __future__ import annotations

import os
from typing import Any

from rich.text import Text
from textual.widgets import Tree

# ── TreeNode is only used for *type hints* ─────────────────────
from textual.widgets._tree import TreeNode  # ← internal, but safe for typing

from widgets.messages import EditNode

# ── Tree subclass that stores {'key', 'value'} in node.data ────
class PromptTree(Tree[dict[str, Any]]):
    BINDINGS = [
        *Tree.BINDINGS,
        ("e", "edit_node", "Edit"),
        ("s", "save_tree", "Save"),
        ("l", "load_tree", "Load"),
        ("x", "expand_all", "Expand All"),
        ("c", "collapse_all", "Collapse All"),
    ]

    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../tree_database"))
        self._tree_lines_cached = None  # ensure our override is used

    

    def render_label(self, node, base, style, *args, **kwargs):
        key = node.data["key"]
        value = node.data["value"]
        preview = " - ".join(list(value.keys()))
        text = Text.from_markup(f"[bold]{key}:[/bold] {preview}")
        return text

    

    # --- keep labels exactly as given ---------------------------------
    def process_label(self, label):
        if isinstance(label, str):
            # Escape any special characters that could interfere with markup
            escaped_label = label.replace("[", "\\[").replace("]", "\\]")
            return Text.from_markup(escaped_label)     # no split(), no truncate
        return label.copy()

    # keyboard
    def action_edit_node(self) -> None:
        if self.cursor_node:
            self.post_message(EditNode(self.cursor_node))

    def action_save_tree(self) -> None:
        from widgets.file_overlays import FileSaveOverlay
        self.app.mount(FileSaveOverlay())

    def action_load_tree(self) -> None:
        from widgets.file_overlays import FileLoadOverlay
        self.app.mount(FileLoadOverlay())

    def action_expand_all(self) -> None:
        """Expand the selected node and all its descendants."""
        if self.cursor_node:
            self.cursor_node.expand_all()

    def action_collapse_all(self) -> None:
        """Collapse the selected node and all its descendants."""
        if self.cursor_node:
            self.cursor_node.collapse_all()

    

    def _tree_to_dict(self, node: TreeNode) -> Any:
        """Convert a tree node and its children to a dictionary or list."""
        if isinstance(node.data["value"], dict):
            result = {}
            for child in node.children:
                key = child.data["key"]
                result[key] = self._tree_to_dict(child)
            return result
        elif isinstance(node.data["value"], list):
            result = []
            for child in node.children:
                result.append(self._tree_to_dict(child))
            return result
        else:
            return node.data["value"]

    def save_to_file(self, path: str) -> None:
        """Save the tree data to a JSON file."""
        import json
        import os
        
        # Convert the current tree state to a dictionary
        data = self._tree_to_dict(self.root)
        
        # Create directory if it doesn't exist
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except Exception as e:
                self.notify(f"Failed to create directory: {str(e)}", severity="error")
                return
        
        # Save to a file
        try:
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
            self.notify(f"Tree saved to {path}", severity="information")
            # Update current directory to the directory of the saved file
            self.current_directory = os.path.dirname(path)
            self.notify(f"Current directory updated to: {self.current_directory}", severity="information")
        except Exception as e:
            # Escape any markup characters in the error message
            error_msg = str(e).replace("[", "\\[").replace("]", "\\]")
            self.notify(f"Failed to save: {error_msg}", severity="error")

    def load_from_file(self, path: str) -> None:
        """Load tree data from a JSON file."""
        import json
        import os
        
        if not os.path.exists(path):
            self.notify(f"File not found: {path}", severity="error")
            return
            
        try:
            with open(path, "r") as f:
                data = json.load(f)
            
            # Clear existing tree
            for child in list(self.root.children):
                child.remove()
            
            # Update root data
            self.root.data["value"] = data
            
            # Rebuild tree
            self._populate_tree(data, parent=self.root)
            #self.root.expand_all()
            
            self.notify(f"Tree loaded from {path}", severity="information")
            # Update current directory to the directory of the loaded file
            self.current_directory = os.path.dirname(path)
        except Exception as e:
            # Escape any markup characters in the error message
            error_msg = str(e).replace("[", "\\[").replace("]", "\\]")
            self.notify(f"Failed to load: {error_msg}", severity="error")

    # mouse
    async def _on_double_click(self, event) -> None:  # type: ignore
        meta = event.style.meta
        if "line" in meta:
            node = self.get_node_at_line(meta["line"])
            if node:
                await self.post_message(EditNode(node))

    def _populate_tree(self, data: Any, parent: TreeNode | None = None) -> None:
        if parent is None:
            parent = self.root

        if isinstance(data, dict):
            for k, v in data.items():
                node = parent.add(str(k), {"key": k, "value": v})
                self._populate_tree(v, node)
        elif isinstance(data, list):
            for i, v in enumerate(data):
                node = parent.add(f"[{i}]", {"key": i, "value": v})
                self._populate_tree(v, node)
