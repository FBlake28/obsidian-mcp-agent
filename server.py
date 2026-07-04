import os
import re
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("obsidian-mcp-agent")

VAULT_ROOT = Path(r"E:\Obsidian Vault").resolve()


def resolve_vault_path(relative_path: str) -> Path:
    """Resolve a path relative to VAULT_ROOT, rejecting any escape via traversal."""
    resolved = (VAULT_ROOT / relative_path).resolve()
    if resolved != VAULT_ROOT and VAULT_ROOT not in resolved.parents:
        raise ValueError(f"Path '{relative_path}' escapes the vault root")
    return resolved


@mcp.tool()
def ping() -> str:
    """Test tool to verify the server is working."""
    return "pong"


@mcp.resource("guide://folder-structure")
def read_folder_guide() -> str:
    """Return the full text contents of folder-guide.md."""
    guide_path = Path(__file__).parent / "folder-guide.md"
    return guide_path.read_text(encoding="utf-8")


EXCLUDED_TOP_LEVEL_FOLDERS = {
    "07-Templates",
    "06-Assets",
    "99-Unsorted",
    "05-Tags",
    "00-Indexes",
}

_ABSTRACT_HEADING_RE = re.compile(r"^##\s*abstract\s*$", re.IGNORECASE)


def _is_section_boundary(stripped_line: str) -> bool:
    return stripped_line == "---" or bool(re.match(r"^#+\s", stripped_line))


def _extract_abstract(text: str) -> str:
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if _ABSTRACT_HEADING_RE.match(line.strip()):
            start = i + 1
            break
    if start is None:
        return ""

    collected = []
    for line in lines[start:]:
        if _is_section_boundary(line.strip()):
            break
        collected.append(line)
    return "\n".join(collected).strip()


def _list_vault_notes(folder: str | None) -> list[dict[str, str]]:
    scan_root = resolve_vault_path(folder) if folder else VAULT_ROOT
    notes = []
    for current_dir, dirnames, filenames in os.walk(scan_root):
        current_path = Path(current_dir)
        if current_path == VAULT_ROOT:
            dirnames[:] = [d for d in dirnames if d not in EXCLUDED_TOP_LEVEL_FOLDERS]

        for filename in filenames:
            if not filename.endswith(".md"):
                continue
            file_path = current_path / filename
            rel_path = file_path.relative_to(VAULT_ROOT).as_posix()
            text = file_path.read_text(encoding="utf-8")
            notes.append({"path": rel_path, "abstract": _extract_abstract(text)})
    return notes


@mcp.resource("vault://notes", name="list_vault_notes")
def list_vault_notes() -> list[dict[str, str]]:
    """List all vault notes (recursively) with their Abstract section text."""
    return _list_vault_notes(None)


@mcp.resource("vault://notes/{folder}", name="list_vault_notes")
def list_vault_notes_in_folder(folder: str) -> list[dict[str, str]]:
    """List vault notes under a specific folder (recursively) with their Abstract section text."""
    return _list_vault_notes(folder)


if __name__ == "__main__":
    mcp.run(transport="stdio")
