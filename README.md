\# Obsidian MCP Agent



A custom Python MCP (Model Context Protocol) server that turns rough,

train-of-thought notes into properly formatted, cross-linked notes in an

Obsidian vault — using Claude Desktop as the interface, with no coding

required at use-time.



\## The Problem



I take a lot of notes during coursework and independent learning, usually

typed quickly and messily during or right after a lecture. Cleaning those

up into a properly formatted, well-organized note — consistent tagging,

inline links to related topics, clear structure — is repetitive and easy

to put off. The raw notes pile up in an "unsorted" backlog instead of

becoming useful, searchable knowledge.



\## What This Does



Point Claude Desktop at this MCP server, say something like "clean up my

Obsidian backlog," and it will:



1\. Read each raw note sitting in the vault's inbox folder.

2\. Rewrite it into a consistent template — abstract, sections, references —

&#x20;  while preserving all the original substance.

3\. Tag it using only tags that already exist in the vault (never inventing

&#x20;  new ones).

4\. Add inline `\[\[wikilinks]]` to genuinely related existing notes, verified

&#x20;  by actually reading the candidate note first — not just matching titles.

5\. Save it to the correct folder and archive the original raw note.

6\. If a note with the same name already exists, it stops and asks — it

&#x20;  never silently overwrites.



Before/after example: see `example/before-raw-inbox-note.md` and

`example/after-formatted-note.md`.



\## Architecture



Built with \[FastMCP](https://github.com/modelcontextprotocol/python-sdk),

running as a local stdio server that Claude Desktop launches as a

subprocess — no API key, no cloud hosting, uses an existing Claude Pro

subscription.



\*\*Tools exposed:\*\*

| Tool | Purpose |

|---|---|

| `read\_folder\_guide` | Static notes on the vault's folder structure |

| `read\_processing\_instructions` | The full note-cleanup workflow, read by Claude before processing |

| `list\_vault\_notes` / `list\_vault\_notes\_in\_folder` | Recursive scan of existing notes and their summaries |

| `read\_note` | Full content of one existing note, for verifying wikilink relevance |

| `list\_templates` / `read\_template` | Reads the vault's note templates |

| `list\_tags` | Live scan of valid tags — never hardcoded |

| `list\_inbox` / `read\_inbox\_note` | Reads raw notes waiting to be processed |

| `write\_note` | Creates a new note; refuses to overwrite, returns a conflict instead |

| `update\_note` | Overwrites an existing note — only ever called after explicit user approval of a proposed merge |

| `archive\_inbox\_note` | Moves a processed raw note out of the inbox |



All file paths are validated against the vault root to prevent path

traversal outside the vault.



\## Setup



1\. Clone this repo.

2\. Create a virtual environment and install dependencies: 

&#x09;python -m venv .venv

&#x09;.venv\\Scripts\\activate      # Windows

&#x09;pip install -r requirements.txt

3\. Set the `OBSIDIAN\_VAULT\_PATH` environment variable to your vault's

&#x20;  absolute path.

4\. Add this server to your `claude\_desktop\_config.json`:

```json

&#x20;  {

&#x20;    "mcpServers": {

&#x20;      "obsidian-mcp-agent": {

&#x20;        "command": "/path/to/.venv/Scripts/python.exe",

&#x20;        "args": \["/path/to/server.py"],

&#x20;        "env": {

&#x20;          "OBSIDIAN\_VAULT\_PATH": "/path/to/your/vault"

&#x20;        }

&#x20;      }

&#x20;    }

&#x20;  }

```

5\. Fully restart Claude Desktop.

6\. Adjust `folder-guide.md` and `processing-instructions.md` to match your

&#x20;  own vault's conventions — these are personal to how I organize notes

&#x20;  and will need editing for a different vault structure.



\## What's Next



\- A template-selection step for coursework that uses a different note

&#x20; format (currently only one template is supported).

\- Automated validation of tag/wikilink formatting in generated output,

&#x20; rather than manual review.

\- Possibly extending beyond a chat-driven workflow to something

&#x20; workflow-embedded — this was intentionally out of scope for this build.



\## Notes on This Project



Built as a weekend project to learn MCP server design (tools vs.

resources, path safety, conflict handling) rather than to build the most

sophisticated possible agent. The `example/` folder uses entirely made-up

content — no real personal notes are included in this repo.

