# tvg2/scripts/structure_dump.py
# ---------------------------------------------------
# Utility script to walk the TVG project directory and
# update /docs/ProjectLayout.md with a cleaned folder tree.
#
# Skips hidden folders and ignored dirs (like .venv/)
# Intended for updating folder structure design docs.

import os
from pathlib import Path

IGNORED_DIRS = {'.git', '.venv', '__pycache__', '.idea', '.mypy_cache', 'build', 'dist'}
MARKER_START = '```'
MARKER_END = '```'


def get_tree_structure(start_path: Path, prefix: str = "") -> list[str]:
    folders = []
    files = []
    entries = sorted(
        [e for e in start_path.iterdir() if not e.name.startswith('.') and e.name not in IGNORED_DIRS],
        key=lambda e: (e.is_file(), e.name.lower())
    )
    for i, entry in enumerate(entries):
        connector = "└── " if i == len(entries) - 1 else "├── "
        line = f"{prefix}{connector}{entry.name}"
        if entry.is_dir():
            folders.append((line, entry))
        else:
            files.append((line, None))

    result = []
    for line, subdir in folders + files:
        result.append(line)
        if subdir:
            extension = "    " if line.startswith("└── ") else "│   "
            result.extend(get_tree_structure(subdir, prefix + extension))
    return result


def parse_existing_structure(text_block: str) -> list[tuple[str, str]]:
    lines = text_block.strip().splitlines()
    parsed = []
    for line in lines:
        if '#' in line:
            path, comment = line.split('#', 1)
            parsed.append((path.rstrip(), f"# {comment.strip()}"))
        else:
            parsed.append((line.rstrip(), ""))
    return parsed


def merge_structure(existing_lines: list[tuple[str, str]], new_lines: list[str]) -> list[str]:
    new_set = set(new_lines)
    existing_map = {path: comment for path, comment in existing_lines}

    result = []
    handled = set()

    # Build result using fresh new_lines as the visual structure baseline
    for path in new_lines:
        comment = existing_map.get(path, "")
        if '[REMOVED]' in comment:
            comment = ''
        result.append((path, comment))
        handled.add(path)

    # Insert missing lines from original structure in original positions
    for path, comment in existing_lines:
        if path not in new_set and path not in handled:
            if comment:
                if '[REMOVED]' not in comment:
                    comment = f"# [REMOVED] {comment[2:]}".rstrip()
            else:
                comment = "# [REMOVED]"
            result.insert(existing_lines.index((path, existing_map.get(path, ""))), (path, comment))
            handled.add(path)

    max_path_length = max((len(p) for p, _ in result), default=0)
    comment_indent = (max_path_length // 4 + 2) * 4

    return [f"{path.ljust(comment_indent)}{comment}".rstrip() if comment else path for path, comment in result]


def update_markdown(file_path: Path, tree_lines: list[str]):
    if not file_path.exists():
        content = [
            "# Project Layout\n\n",
            f"`{file_path.name}`\n\n",
            "## File & Folder Structure\n",
            MARKER_START,
            *tree_lines,
            MARKER_END,
            "\n"
        ]
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            original = f.read()

        before, inside, after = original.partition(MARKER_START)
        raw_inside, inside_end, after = after.partition(MARKER_END)

        existing_lines = parse_existing_structure(raw_inside)
        merged_tree = merge_structure(existing_lines, tree_lines)

        content = [
            before,
            MARKER_START,
            *merged_tree,
            MARKER_END,
            after
        ]

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(line.rstrip() for line in content))


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    docs_file = project_root / "docs" / "ProjectLayout.md"

    print(f"Updating: {docs_file.relative_to(project_root)}\n")
    tree_output = get_tree_structure(project_root)
    update_markdown(docs_file, tree_output)
    print("✅ Folder structure updated in ProjectLayout.md")

# Notes:
# - Builds display based on new structure order
# - Inserts new items directly in-place
# - Preserves removed entries exactly where they originally appeared
# - Aligns comments to two-tab offset
