from __future__ import annotations

import os

from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import Vertical
from textual.widgets import (
    Footer,
    TextArea,
    DirectoryTree,
)

from widgets.prompt_tree import PromptTree
from widgets.messages import FileSelected

# ── Common directory browser overlay ───────────────────────────
class DirectoryBrowserOverlay(Widget):
    """Base class for directory browser overlays."""
    
    DEFAULT_CSS = """
    DirectoryBrowserOverlay {
        layer: overlay;
        margin: 2 10;
        border: heavy $accent;
        background: $panel-darken-1 80%;
    }
    DirectoryBrowserOverlay Vertical {
        height: 100%;
    }
    DirectoryBrowserOverlay DirectoryTree {
        height: 1fr;
        width: 100%;
    }
    DirectoryBrowserOverlay Footer {
        dock: bottom;
        height: 3;
    }
    """

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        ("u", "go_up", "Go Up"),
    ]

    def __init__(self, action: str):
        super().__init__()
        self.action = action
        # Get the current directory from the prompt tree
        try:
            prompt_tree = self.app.query_one(PromptTree)
            if prompt_tree and hasattr(prompt_tree, 'current_directory'):
                start_dir = prompt_tree.current_directory
                self.notify(f"Starting in directory: {start_dir}", severity="information")
            else:
                # Fallback to tree_database directory if no current directory is set
                start_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../tree_database"))
                self.notify(f"No current directory set, using tree_database: {start_dir}", severity="information")
        except Exception:
            # Fallback to tree_database directory if no prompt tree found
            start_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../tree_database"))
            self.notify(f"No prompt tree found, using tree_database: {start_dir}", severity="information")
            
        self._browser = DirectoryTree(
            path=start_dir,
            id="browser",
        )

    def compose(self) -> ComposeResult:
        """Override in subclasses to add specific footer content."""
        yield Vertical(
            self._browser,
            Footer(),
        )

    def on_mount(self) -> None:
        self._browser.focus()

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        path_str = str(event.path)
        if path_str.endswith(".json"):
            # Get the absolute path of the selected file
            selected_path = os.path.abspath(path_str)
            self.post_message(FileSelected(selected_path, self.action))
            self.dismiss()
        else:
            self.notify("Please select a JSON file", severity="warning")

    def action_cancel(self) -> None:
        """Handle cancel action."""
        self.dismiss()

    def action_go_up(self) -> None:
        """Go up to the parent directory."""
        current_path = str(self._browser.path)
        parent_path = os.path.dirname(current_path)
        
        # Don't go up if we're already at the root
        if parent_path == current_path:
            self.notify("Already at root directory", severity="warning")
            return
            
        # Check if parent directory exists and is accessible
        if not os.path.exists(parent_path) or not os.path.isdir(parent_path):
            self.notify(f"Cannot access parent directory: {parent_path}", severity="error")
            return
            
        # Navigate to parent directory
        self._browser.path = parent_path
        self.notify(f"Navigated to: {parent_path}", severity="information")

    def dismiss(self) -> None:
        """Safely remove the overlay."""
        self.remove()
        # Find the prompt tree and set focus to it
        prompt_tree = self.app.query_one(PromptTree)
        if prompt_tree:
            prompt_tree.focus()


# ── Save overlay with filename input ───────────────────────────
class FileSaveOverlay(DirectoryBrowserOverlay):
    """Overlay for saving files with filename input."""
    
    DEFAULT_CSS = """
    FileSaveOverlay {
        layer: overlay;
        margin: 2 10;
        border: heavy $accent;
        background: $panel-darken-1 80%;
    }
    FileSaveOverlay Vertical {
        height: 100%;
    }
    FileSaveOverlay DirectoryTree {
        height: 1fr;
        width: 100%;
    }
    FileSaveOverlay TextArea {
        width: 100%;
        height: 3;
        border: solid $accent;
        background: $surface;
    }
    FileSaveOverlay Footer {
        dock: bottom;
        height: 1;
    }
    """

    BINDINGS = [
        ("ctrl+s", "save", "Save"),
        ("escape", "cancel", "Cancel"),
    ]

    def __init__(self):
        super().__init__("save")
        self._input = TextArea(
            text="",
            id="filename",
        )

    def compose(self) -> ComposeResult:
        """Override to include filename input."""
        yield Vertical(
            self._browser,
            self._input,
            Footer(),
        )

    def on_mount(self) -> None:
        super().on_mount()
        # Set placeholder text after mount
        self._input.styles.placeholder = "Enter filename (e.g., myfile.json)"

    def action_save(self) -> None:
        """Handle save action with filename input."""
        filename = self._input.text.strip()
        if not filename:
            self.notify("Please enter a filename", severity="warning")
            return
            
        if not filename.endswith(".json"):
            filename += ".json"
            
        # Get the current directory from the browser's cursor node
        if self._browser.cursor_node:
            current_dir = os.path.abspath(str(self._browser.cursor_node.data.path))
            if not os.path.isdir(current_dir):
                # If the cursor is on a file, use its parent directory
                current_dir = os.path.dirname(current_dir)
        else:
            # If no cursor node, use the browser's current path
            current_dir = os.path.abspath(str(self._browser.path))
            
        self.notify(f"Saving to directory: {current_dir}", severity="information")
        
        if not os.path.isdir(current_dir):
            self.notify("Invalid directory selected", severity="error")
            return
            
        # Create the full file path
        file_path = os.path.join(current_dir, filename)
        
        # Ensure we're not trying to write to a directory
        if os.path.isdir(file_path):
            self.notify("Cannot save to a directory", severity="error")
            return
            
        self.post_message(FileSelected(file_path, self.action))
        self.dismiss()


# ── Load overlay with simple footer ───────────────────────────
class FileLoadOverlay(DirectoryBrowserOverlay):
    """Overlay for loading files with simple footer."""
    
    DEFAULT_CSS = """
    FileLoadOverlay {
        margin: 2 10;
        border: heavy $accent;
        background: $panel-darken-1 80%;
    }
    FileLoadOverlay Vertical {
        height: 100%;
    }
    FileLoadOverlay DirectoryTree {
        height: 1fr;
        width: 100%;
    }
    FileLoadOverlay Footer {
        dock: bottom;
        height: 1;
    }
    """

    BINDINGS = [
        ("l", "load", "Load"),
        ("enter", "load", "Load"),
        ("escape", "cancel", "Cancel"),
    ]

    def __init__(self):
        super().__init__("load")

    def compose(self) -> ComposeResult:
        """Override to provide simple footer."""
        yield Vertical(
            self._browser,
            Footer(),
        )

    def action_load(self) -> None:
        """Handle load action."""
        if self._browser.cursor_node:
            path_str = str(self._browser.cursor_node.data.path)
            if path_str.endswith(".json"):
                selected_path = os.path.abspath(path_str)
                self.post_message(FileSelected(selected_path, "load"))
                self.dismiss()
            else:
                self.notify("Please select a JSON file", severity="warning")
        else:
            self.notify("No file selected", severity="warning")
