# vault-compiler

A Claude Code plugin that compiles coding session knowledge from [claude-mem](https://github.com/thedotmack/claude-mem) into structured articles in your Obsidian vault.

## What It Does

```
claude-mem (auto-captures sessions)
    ↓ reads via MCP tools
vault-compiler (synthesizes knowledge)
    ↓ writes to
Obsidian Vault / 11-CodeMemory/{project}/
```

- **SessionEnd hook** — logs compilation trigger after each session
- **PreCompact hook** — safety net before context pruning
- **`/compile`** — manually compile recent observations into knowledge articles
- **`/compile-status`** — see what's pending compilation
- **`/addToVault`** — smart intake for any vault content (memory dumps, content ideas, wins, finance, crypto)

## Output Structure

```
11-CodeMemory/
├── pebbo/
│   ├── index.md          # Knowledge catalog
│   ├── concepts/         # Atomic knowledge articles
│   ├── connections/      # Cross-cutting insights
│   └── qa/               # Valuable Q&A
├── agape/
│   └── ...
└── cross-project/
    └── connections/      # Patterns spanning projects
```

## Prerequisites

- [claude-mem](https://github.com/thedotmack/claude-mem) plugin installed and active
- Obsidian vault at `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian Vault/`
- Python 3.9+

## Installation

```bash
# Point Claude Code to this plugin
claude --plugin-dir ~/Developer/plugins/vault-compiler

# Or add to settings
# ~/.claude/settings.json → "pluginDirs": ["~/Developer/plugins/vault-compiler"]
```

## Usage

```
/compile pebbo              # Compile Pebbo project observations
/compile --all              # Compile all projects
/compile-status             # Check what needs compiling
/addToVault                 # Add something to the vault (interactive)
/addToVault "content idea for YouTube about Solana"
```

## Dependencies

- **claude-mem** — provides session capture and MCP search tools
- **Obsidian vault** — with CLAUDE.md wiki schema (10-Wiki/) and 11-CodeMemory/

## Architecture

This plugin does NOT modify claude-mem. It reads from claude-mem's MCP tools:
- `search` — find observations by keyword/project
- `timeline` — chronological session view
- `get_observations` — full observation content

And writes structured markdown to the Obsidian vault.

## License

MIT
