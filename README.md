# Obsidian MCP Agent

A custom Python MCP (Model Context Protocol) server that turns rough, train-of-thought notes into properly formatted, cross-linked notes in an Obsidian vault — using Claude Desktop as the interface, with no coding required at use-time.

## The Problem

I take a lot of notes during coursework and independent learning, usually typed quickly and messily during or right after a lecture. Cleaning those up into a properly formatted, well-organized note — consistent tagging, inline links to related topics, clear structure — is repetitive and easy to put off. The raw notes pile up in an "unsorted" backlog instead of becoming useful, searchable knowledge.

## What This Does

Point Claude Desktop at this MCP server, say something like "clean up my Obsidian backlog," and it will:

1. Read each raw note sitting in the vault's inbox folder.
2. Rewrite it into a consistent template — abstract, sections, references — while preserving all the original substance.
3. Tag it using only tags that already exist in the vault (never inventing new ones).
4. Add inline `[[wikilinks]]` to genuinely related existing notes, verified by actually reading the candidate note first — not just matching titles.
5. Save it to the correct folder and archive the original raw note.
6. If a note with the same name already exists, it stops and asks — it never silently overwrites.

Before/after example: see `example/before-raw-inbox-note.md` and `example/after-formatted-note.md`.

## Architecture

Built with [FastMCP](https://github.com/modelcontextprotocol/python-sdk), running as a local stdio server that Claude Desktop launches as a subprocess — no API key, no cloud hosting, uses an existing Claude Pro subscription.

**Tools exposed:**

| Tool | Purpose |
|---|---|
| `read_folder_guide` | Static notes on the vault's folder structure |
| `read_processing_instructions` | The full note-cleanup workflow, read by Claude before processing |
| `list_vault_notes` / `list_vault_notes_in_folder` | Recursive scan of existing notes and their summaries |
| `read_note` | Full content of one existing note, for verifying wikilink relevance |
| `list_templates` / `read_template` | Reads the vault's note templates |
| `list_tags` | Live scan of valid tags — never hardcoded |
| `list_inbox` / `read_inbox_note` | Reads raw notes waiting to be processed |
| `write_note` | Creates a new note; refuses to overwrite, returns a conflict instead |
| `update_note` | Overwrites an existing note — only ever called after explicit user approval of a proposed merge |
| `archive_inbox_note` | Moves a processed raw note out of the inbox |

All file paths are validated against the vault root to prevent path traversal outside the vault.

## Setup

1. Clone this repo.
2. Create a virtual environment and install dependencies: 

	python -m venv .venv
	.venv\Scripts\activate      # Windows
	pip install -r requirements.txt

3. Set the `OBSIDIAN_VAULT_PATH` environment variable to your vault's absolute path.
4. Add this server to your `claude_desktop_config.json`:

```json
  {
    "mcpServers": {
      "obsidian-mcp-agent": {
        "command": "/path/to/.venv/Scripts/python.exe",
        "args": ["/path/to/server.py"],
        "env": {
          "OBSIDIAN_VAULT_PATH": "/path/to/your/vault"
        }
      }
    }
  }
```

5. Fully restart Claude Desktop.
6. Adjust `folder-guide.md` and `processing-instructions.md` to match your own vault's conventions — these are personal to how I organize notes and will need editing for a different vault structure.

## What's Next

- A template-selection step for coursework that uses a different note format (currently only one template is supported).
- Automated validation of tag/wikilink formatting in generated output, rather than manual review.
- Possibly extending beyond a chat-driven workflow to something workflow-embedded — this was intentionally out of scope for this build.

## Notes on This Project

Built as a weekend project to learn MCP server design (tools vs. resources, path safety, conflict handling) rather than to build the most sophisticated possible agent. The `example/` folder uses entirely made-up content — no real personal notes are included in this repo.
