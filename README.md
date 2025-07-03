# Tree Editor

Mostly vibe coded from a set of core requirements. Enjoy (:)

A modern, terminal-based interactive tree editor for editing, viewing, and managing hierarchical data structures (such as JSON trees). Built with [Textual](https://github.com/Textualize/textual) and [Rich](https://github.com/Textualize/rich), it provides a fast, keyboard-driven interface for exploring and editing trees.

---

## Features

- **Interactive Tree View:**  
  Browse, expand, and collapse nodes in a hierarchical tree structure.

- **Node Editing:**  
  Edit the key and value of any node in the tree with a simple overlay editor.

- **Load/Save Trees:**  
  - Load tree data from JSON files.
  - Save the current tree to a JSON file.
  - File dialogs default to a dedicated `tree_database` directory for easy organization.

- **Keyboard Shortcuts:**  
  - `e`: Edit selected node
  - `s`: Save tree
  - `l`: Load tree
  - `x`: Expand all nodes
  - `c`: Collapse all nodes
  - Navigation and file dialogs are fully keyboard-accessible

- **Overlay File Browser:**  
  - Browse directories and select files to load or save
  - Only allows saving/loading `.json` files for safety

- **Path Header:**  
  - Shows the current path in the tree for context

---

## Installation

### 1. Clone the repository

```sh
git clone https://github.com/yourusername/tree_editor.git
cd tree_editor
```

### 2. Install with pip (using `pyproject.toml`)

```sh
pip install -e .
```

This will install all dependencies and make the `tree-editor` command available.

---

## Usage

### Run the app

```sh
tree-editor
```

- The main interface will open in your terminal.
- Use the keyboard shortcuts to navigate, edit, load, and save trees.

### Run in test mode (for component testing)

```sh
tree-editor --test
```

---

## Project Structure

```
tree_editor/
├── src/
│   ├── app.py           # Main application entry point
│   └── widgets/
│       ├── prompt_tree.py
│       ├── file_overlays.py
│       ├── edit_overlay.py
│       ├── path_header.py
│       └── messages.py
├── tree_database/       # Default directory for tree JSON files
├── pyproject.toml
└── README.md
```

---

## Requirements

- Python 3.9+
- [Textual](https://github.com/Textualize/textual) >= 0.40.0
- [Rich](https://github.com/Textualize/rich) >= 13.0.0

All dependencies are installed automatically with the pip command above.

---

## License

GNU GLPv3 License
