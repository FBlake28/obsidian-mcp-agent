\# Vault Folder Guide



Static reference for distinguishing top-level folders. Only consult this

when routing a note to a folder is ambiguous — most notes' correct folder

will be obvious from content.



\- \*\*00-Indexes\*\* — Currently unused by this agent. Originally proposed as

&#x20; the inbox, but replaced by 99-Unsorted since that's where Obsidian

&#x20; already defaults new notes. Reserved for possible future use; the agent

&#x20; does not read or write here.



\- \*\*01-Learning\*\* — The largest folder. Coursework and learning notes from

&#x20; Stevens (grad program) and independent online courses. Default landing

&#x20; spot for most academic/conceptual notes (ML, stats, CS theory, etc.)

&#x20; unless the note is really about a specific tool/library (see 02) or

&#x20; work-related (see 03).



\- \*\*02-Code Notes\*\* — General-purpose reference on specific tools,

&#x20; libraries, or platforms (e.g. a Python library, a SQL platform).

&#x20; Distinction from 01-Learning: 02 is tool/library reference material

&#x20; useful across contexts; 01 is tied to a specific course or learning

&#x20; path. A note on "how pandas groupby works" → 02. A note on "Assignment 3

&#x20; concepts from Stevens ML course" → 01, even if it discusses pandas.



\- \*\*03-Work\*\* — Professional career material: resumes, networking

&#x20; trackers, certifications, academic projects, consulting timesheets,

&#x20; company research. Distinction from 01: 03 is about career/professional

&#x20; application, not conceptual learning, even if the underlying topic

&#x20; overlaps.



\- \*\*04-Personal\*\* — Non-professional, non-learning personal life: health,

&#x20; 3D printing, hobbies.



\- \*\*05-Tags\*\* — Not a content folder. Holds tag-hub notes only. The agent

&#x20; reads this folder live to get the current valid tag list; it never

&#x20; writes new notes here and never invents new tags.



\- \*\*06-Assets\*\* — Screenshots and other embedded media. The agent doesn't

&#x20; read or write here.



\- \*\*07-Templates\*\* — Note templates (e.g. Quick Note). The agent reads

&#x20; from here (`list\_templates`/`read\_template`) but never writes here.



\- \*\*08-Workflow Guides\*\* — Guides for specific multi-step workflows (e.g.

&#x20; building an AI agent, running an ML project end-to-end). Distinction

&#x20; from 01/02: these are process/how-to guides spanning multiple steps,

&#x20; not a single concept or tool.



\- \*\*99-Unsorted\*\* — INBOX for this agent. Obsidian already defaults newly

&#x20; created notes to this folder, so raw rough notes land here with no

&#x20; extra step. The agent scans this folder's top level only (excluding

&#x20; the `\_processed` subfolder) for notes waiting to be formatted. Once

&#x20; processed, `archive\_inbox\_note` moves them to `99-Unsorted/\_processed`.

&#x20; Note: this folder was also the user's pre-existing manual-sort habit —

&#x20; that overlap is known and not being solved this weekend.

