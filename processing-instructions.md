# Inbox Note Processing Instructions

Follow this workflow whenever asked to process, clean up, or format notes
in the unsorted inbox backlog.

## Workflow

1. Call `list_inbox` to see which raw notes are waiting.
2. If empty, report that the backlog is clear and stop.
3. For each file in the inbox, one at a time:

   a. Call `read_inbox_note` to get its raw, messy content.

   b. Call `read_template` with `"Quick Note.md"` to confirm the current
      skeleton structure (date/time/status/tags fields, Abstract section,
      table-of-contents block, References section).

   c. Call `list_tags` to get the current valid tag list. Never invent a
      tag that isn't in this list — if a topic doesn't fit an existing
      tag, connect it via an inline wikilink instead.

   d. Call `list_vault_notes` to see existing notes and their abstracts.
      For any topic mentioned in the raw note that seems related to an
      existing note, call `read_note` on that candidate to confirm it's
      genuinely relevant before linking — never link on title match alone.

   e. Rewrite the raw content into the Quick Note skeleton:
      - `date::` and `time::` set to today's date/time.
      - `status:: #agent` always (never assign #baby/#teen/#adult/#retired
        — that's the user's manual judgment call after review).
      - `tags::` populated with wikilinked tags pulled only from step (c)'s
        live list, e.g. `tags:: [[python]], [[machine learning]]`. Empty
        is allowed if nothing fits.
      - Abstract section: write a clear overview paragraph. This doubles
        as the note's summary, so make it complete and readable on its
        own. Use `==highlighted==` markdown on key terms at first
        definition. Add inline `[[wikilinks]]` at first mention of any
        topic confirmed relevant in step (d) — never a links list at the
        bottom.
      - Preserve all substance from the raw note. Clean up phrasing,
        fix structure, organize into logical sections — but never
        invent new information, never drop content, never change the
        meaning of what the user wrote.
      - Use `---` for horizontal rule separators throughout.
      - Include a `### References` section near the bottom (placeholder
        is fine if the raw note had no sources).
      - If the note includes a substantial code block, wrap it in a
        collapsible `> [!info]- Title` callout rather than a bare
        fenced block.

   f. Decide the correct destination folder based on `read_folder_guide`
      and the note's actual topic/content.

   g. Call `write_note` with the folder, a plain-text topic filename
      (no date prefix), and the fully formatted content.

   h. If `write_note` returns `"conflict"`: do NOT archive the original
      inbox note yet. Report the conflict to the user in chat — the
      existing note's path and the drafted content — so they can decide
      how to proceed. Ask whether they'd like you to draft a proposed
      merge of the new information into the existing note.

      - If they ask for a merge draft, use `read_note` on the existing
        note and show the user the full proposed merged content in
        chat as a preview. Do NOT call `update_note` yet.
      - Only call `update_note` after the user has explicitly reviewed
        the proposed merged content in chat and approved writing it.
        Never call `update_note` automatically or as a routine part of
        inbox processing — it overwrites an existing note in place, and
        that always requires the user's explicit go-ahead first.
      - Once the user approves and `update_note` succeeds (or if the
        user says to leave the raw note alone for now), you may then
        call `archive_inbox_note` on the original inbox filename.

   i. If `write_note` returns `"written"`: call `archive_inbox_note` on
      the original inbox filename to move it out of the backlog.

4. After processing all files, give a short summary: how many notes were
   created, their paths, and how many conflicts (if any) still need
   manual attention or are awaiting merge approval.