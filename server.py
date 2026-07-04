import os
import re
from pathlib import Path
from typing import Any
from urllib.parse import unquote

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.resources.templates import ResourceTemplate

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


class _SlashTolerantResourceTemplate(ResourceTemplate):
    """A ResourceTemplate whose placeholders may contain '/', for relative file paths.

    The base implementation builds its matching regex with `[^/]+` per placeholder,
    which cannot capture multi-segment paths like '01-Learning/GenAI/RAG.md'.
    """

    def matches(self, uri: str) -> dict[str, Any] | None:
        pattern = self.uri_template.replace("{", "(?P<").replace("}", ">.+)")
        match = re.match(f"^{pattern}$", uri)
        if not match:
            return None
        return {key: unquote(value) for key, value in match.groupdict().items()}


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


def list_vault_notes_in_folder(folder: str) -> list[dict[str, str]]:
    """List vault notes under a specific folder (recursively) with their Abstract section text."""
    return _list_vault_notes(folder)


_list_vault_notes_in_folder_template = _SlashTolerantResourceTemplate.from_function(
    list_vault_notes_in_folder,
    uri_template="vault://notes/{folder}",
    name="list_vault_notes",
    description=list_vault_notes_in_folder.__doc__,
)
mcp._resource_manager._templates[_list_vault_notes_in_folder_template.uri_template] = (
    _list_vault_notes_in_folder_template
)


def read_note(path: str) -> str:
    """Return the full raw contents of a vault note at the given relative path."""
    return resolve_vault_path(path).read_text(encoding="utf-8")


_read_note_template = _SlashTolerantResourceTemplate.from_function(
    read_note,
    uri_template="vault://note/{path}",
    name="read_note",
    description=read_note.__doc__,
)
mcp._resource_manager._templates[_read_note_template.uri_template] = _read_note_template


@mcp.resource("vault://templates")
def list_templates() -> list[str]:
    """List filenames found at the top level of 07-Templates (no recursion)."""
    templates_dir = resolve_vault_path("07-Templates")
    return sorted(entry.name for entry in templates_dir.iterdir() if entry.is_file())


def read_template(name: str) -> str:
    """Return the full raw contents of a template file in 07-Templates."""
    return resolve_vault_path(f"07-Templates/{name}").read_text(encoding="utf-8")


_read_template_template = _SlashTolerantResourceTemplate.from_function(
    read_template,
    uri_template="vault://template/{name}",
    name="read_template",
    description=read_template.__doc__,
)
mcp._resource_manager._templates[_read_template_template.uri_template] = _read_template_template


@mcp.resource("vault://tags")
def list_tags() -> list[str]:
    """List bare tag names found at the top level of 05-Tags (no recursion)."""
    tags_dir = resolve_vault_path("05-Tags")
    return sorted(entry.stem for entry in tags_dir.iterdir() if entry.suffix == ".md")


@mcp.resource("vault://inbox")
def list_inbox() -> list[str]:
    """List filenames found at the top level of 99-Unsorted, excluding _processed (no recursion)."""
    inbox_dir = resolve_vault_path("99-Unsorted")
    return sorted(
        entry.name for entry in inbox_dir.iterdir() if entry.is_file() and entry.name != "_processed"
    )


def read_inbox_note(filename: str) -> str:
    """Return the full raw contents of a note in 99-Unsorted."""
    return resolve_vault_path(f"99-Unsorted/{filename}").read_text(encoding="utf-8")


_read_inbox_note_template = _SlashTolerantResourceTemplate.from_function(
    read_inbox_note,
    uri_template="vault://inbox/{filename}",
    name="read_inbox_note",
    description=read_inbox_note.__doc__,
)
mcp._resource_manager._templates[_read_inbox_note_template.uri_template] = _read_inbox_note_template


_INVALID_FILENAME_CHARS_RE = re.compile(r'[<>:"/\\|?*]')


def _sanitize_filename(filename: str) -> str:
    cleaned = _INVALID_FILENAME_CHARS_RE.sub("", filename).strip()
    if not cleaned.lower().endswith(".md"):
        cleaned += ".md"
    return cleaned


@mcp.tool()
def write_note(folder: str, filename: str, content: str) -> dict:
    """Create a new note in the vault, refusing to overwrite a note with the same filename elsewhere."""
    sanitized_filename = _sanitize_filename(filename)

    for note in _list_vault_notes(None):
        if Path(note["path"]).name.lower() == sanitized_filename.lower():
            return {
                "status": "conflict",
                "existing_path": note["path"],
                "drafted_content": content,
            }

    target_dir = resolve_vault_path(folder)
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / sanitized_filename
    target_path.write_text(content, encoding="utf-8")

    return {
        "status": "written",
        "path": target_path.relative_to(VAULT_ROOT).as_posix(),
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
