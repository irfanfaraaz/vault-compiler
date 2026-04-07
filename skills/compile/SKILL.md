---
description: "Compile recent coding session observations from claude-mem into structured knowledge articles in the Obsidian vault. Use when the user says /compile, 'compile my sessions', 'compile knowledge', 'sync to vault', or wants to manually trigger knowledge compilation."
argument-hint: "[project-name] [--all] [--since YYYY-MM-DD] [--recompile]"
allowed-tools: ["mcp__plugin_claude-mem_mcp-search__search", "mcp__plugin_claude-mem_mcp-search__timeline", "mcp__plugin_claude-mem_mcp-search__get_observations", "mcp__plugin_claude-mem_mcp-search__smart_search", "Read", "Write", "Edit", "Glob", "Bash"]
---

# Compile Sessions to Vault

Compile recent claude-mem observations into structured knowledge articles in the Obsidian vault at `11-CodeMemory/{project}/`.

## Vault Output Location

```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian Vault/11-CodeMemory/
├── {project}/
│   ├── index.md           # Per-project knowledge catalog
│   ├── concepts/          # Atomic knowledge articles
│   ├── connections/       # Cross-cutting insights linking 2+ concepts
│   └── qa/                # Filed Q&A (valuable answers worth keeping)
└── cross-project/
    ├── index.md
    └── connections/       # Patterns spanning multiple projects
```

## Compilation Workflow

1. **Fetch observations** from claude-mem using MCP tools:
   - Use `search` with project filter to get recent observations
   - Use `timeline` to understand session chronology
   - Use `get_observations` for full observation content

2. **Filter uncompiled observations:**
   - Read `{project}/index.md` to find what's already compiled
   - Check the `last_compiled` date in index frontmatter
   - Only process observations newer than last compilation

3. **Synthesize into articles:**
   For each cluster of related observations, create ONE of:

   **Concept article** (`concepts/`):
   ```yaml
   ---
   type: code-knowledge
   category: concept
   project: {project-name}
   created: YYYY-MM-DD
   updated: YYYY-MM-DD
   compiled_from: ["obs#123", "obs#456"]
   tags: [tag1, tag2]
   ---
   ```
   - One concept per article (atomic)
   - Include: what it is, why it matters, code snippets if relevant, gotchas
   - Name: `concepts/descriptive-kebab-name.md`

   **Connection article** (`connections/`):
   ```yaml
   ---
   type: code-knowledge
   category: connection
   project: {project-name}
   created: YYYY-MM-DD
   links: ["[[concepts/a]]", "[[concepts/b]]"]
   compiled_from: ["obs#789"]
   tags: [tag1, tag2]
   ---
   ```
   - Links 2+ concepts with an insight
   - Name: `connections/concept-a-and-concept-b.md`

   **Q&A article** (`qa/`):
   ```yaml
   ---
   type: code-knowledge
   category: qa
   project: {project-name}
   created: YYYY-MM-DD
   compiled_from: ["obs#101"]
   tags: [tag1, tag2]
   ---
   ```
   - A question that was answered during a session, worth preserving
   - Name: `qa/descriptive-question.md`

4. **Update index.md:**
   ```yaml
   ---
   type: code-knowledge-index
   project: {project-name}
   last_compiled: YYYY-MM-DD
   ---
   ```
   Add new articles to the catalog table:
   `| [[concepts/name]] | One-line summary | 2026-04-07 |`

5. **Report results:**
   - How many observations processed
   - How many articles created/updated
   - Any observations skipped (too trivial, duplicates)

## Arguments

- **project-name**: Compile only this project (e.g., `/compile pebbo`)
- **--all**: Compile all projects
- **--since YYYY-MM-DD**: Only process observations after this date
- **--recompile**: Wipe all existing articles for the project and rebuild from scratch. Useful when articles have drifted or you want a clean slate. Deletes all files in `concepts/`, `connections/`, `qa/` and resets `index.md`, then recompiles all observations from the beginning.
- No args: Compile current project (detect from working directory or ask)

## Deduplication Rules

- Before creating a new concept, search existing concepts for overlap
- If a new observation reinforces an existing concept, UPDATE the existing article (bump `updated`, add to `compiled_from`)
- If a new observation contradicts an existing concept, create a connection article explaining the contradiction
- Never create two articles about the same concept

## Cross-Project Connections

After per-project compilation, check if any new concepts connect to concepts in other projects. If so, create articles in `cross-project/connections/`.
