---
description: "Show compilation status — what's pending, last compiled date, observation counts. Use when user says /compile-status, 'what needs compiling', 'compilation status', or 'pending observations'."
argument-hint: "[project-name]"
allowed-tools: ["mcp__plugin_claude-mem_mcp-search__search", "mcp__plugin_claude-mem_mcp-search__timeline", "Read", "Glob"]
---

# Compile Status

Show the current state of knowledge compilation for the Obsidian vault.

## Workflow

1. **Read vault state:**
   - Glob `11-CodeMemory/*/index.md` to find all compiled projects
   - Read each `index.md` frontmatter for `last_compiled` date
   - Count articles per project (glob `concepts/*.md`, `connections/*.md`, `qa/*.md`)

2. **Query claude-mem:**
   - Use `timeline` to get recent session dates
   - Use `search` to count observations per project since last compilation
   - Identify which projects have uncompiled observations

3. **Present status table:**

   ```
   | Project | Last Compiled | Articles | Pending Obs | Status |
   |---------|--------------|----------|-------------|--------|
   | pebbo   | 2026-04-06   | 12       | 5           | ⚠️ needs compile |
   | agape   | 2026-04-07   | 8        | 0           | ✅ up to date |
   | general | never        | 0        | 23          | 🔴 not started |
   ```

4. **Suggest action:**
   - If pending observations exist: "Run `/compile {project}` to process them"
   - If all up to date: "All projects compiled. No action needed."

## Arguments

- **project-name**: Show status for specific project only
- No args: Show all projects
