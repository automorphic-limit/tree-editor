# Recursive Trie-Like Dictionary Structure

## Overview

This document describes a recursive nested dictionary structure used in the provided `cat_tree`, `dict_trie_forward`, and `dict_trie_reverse` data sets. It serves as a formal reference for understanding, implementing, and traversing this structure.

---

## Natural Language Description

The structure is a **recursive trie-like tree** where:

- **Each node is a dictionary (map).**
- **Keys are strings** that encode semantic information (they can be full concepts, categories, words, or individual letters).
- **Leaves are strictly empty dictionaries (**``**).**
- **Internal nodes** may have zero or more child nodes.
- **The absence of children (i.e., an empty dictionary) marks the end of a path.**

### Key Properties

- **Recursive:** Each child node is itself the same type of dictionary.
- **Leaves:** Always `{}` (empty dictionary).
- **Keys:** Contain meaningful data.
- **Traversal:** Supports both depth-first and breadth-first traversal.

---

## Algebraic Data Type (ADT) Definition

```text
TrieTree := Empty | Map[String, TrieTree]
```

- **Empty:** Terminal node, represented as `{}`.
- **Map[String, TrieTree]:** Dictionary where each key maps to another TrieTree.

---

## Example Structures

### Example 1: Category Tree (from `cat_tree`)

```json
{
  "Category Theory": {
    "Foundations": {
      "Objects and Morphisms": {}
    }
  }
}
```

- "Category Theory" is the root.
- "Foundations" is a child node.
- "Objects and Morphisms" is a leaf node.

### Example 2: Word Trie (from `dict_trie_forward`)

```json
{
  "a": {
    "a": {
      "a": {
        " ": {}
      }
    }
  }
}
```

- Represents the string "aaa " with each level corresponding to one character.

---

## Type Representations in Programming Languages

### C

```c
typedef struct TrieNode {
    char *key;
    struct TrieNode **children;
    size_t child_count;
} TrieNode;
```

### Python

```python
TrieTree = dict[str, 'TrieTree']  # Recursive dictionary
```

### Rust

```rust
use std::collections::HashMap;

struct TrieNode {
    children: HashMap<String, TrieNode>,
}
```

### Lisp

```lisp
;; Each node is an association list (alist)
;; '((key . subtree) (key . subtree) ...)
;; Leaves are empty lists '()
```

---

## Summary of Formal Properties

- Recursive definition
- Deterministic terminal condition (empty dictionary)
- Each key holds semantic or structural information
- Structure supports common tree operations (traversal, insertion, lookup)

---

## Notes

If required, traversal algorithms, serialization schemes, and language-specific parsers can be provided for this structure.

