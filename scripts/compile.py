#!/usr/bin/env python3
"""
vault-compiler: Compile claude-mem observations into Obsidian vault knowledge articles.

This script is triggered by:
- SessionEnd hook (automatic)
- PreCompact hook (safety net)
- /compile skill (manual)

It reads from claude-mem's MCP tools and writes structured knowledge
articles to 11-CodeMemory/{project}/ in the Obsidian vault.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, date
from pathlib import Path

# Vault location
VAULT_PATH = Path.home() / "Library" / "Mobile Documents" / "iCloud~md~obsidian" / "Documents" / "Obsidian Vault"
CODE_MEMORY_PATH = VAULT_PATH / "11-CodeMemory"


def get_vault_path():
    """Return the vault path, checking it exists."""
    if not VAULT_PATH.exists():
        print(f"ERROR: Vault not found at {VAULT_PATH}", file=sys.stderr)
        sys.exit(1)
    return VAULT_PATH


def ensure_project_dirs(project: str):
    """Create project directory structure if it doesn't exist."""
    project_path = CODE_MEMORY_PATH / project
    for subdir in ["concepts", "connections", "qa"]:
        (project_path / subdir).mkdir(parents=True, exist_ok=True)

    # Create index.md if it doesn't exist
    index_path = project_path / "index.md"
    if not index_path.exists():
        today = date.today().isoformat()
        index_path.write_text(f"""---
type: code-knowledge-index
project: {project}
last_compiled: {today}
---

# {project.title()} — Code Knowledge

Compiled from claude-mem session observations.

## Concepts

| Page | Summary | Updated |
|------|---------|---------|
| — | No articles yet | — |

## Connections

| Page | Summary | Updated |
|------|---------|---------|
| — | No articles yet | — |

## Q&A

| Page | Summary | Updated |
|------|---------|---------|
| — | No articles yet | — |
""")

    return project_path


def log_compilation(trigger: str, project: str = "unknown", articles_created: int = 0):
    """Append a compilation record to a simple log file."""
    log_path = CODE_MEMORY_PATH / "compile.log"
    timestamp = datetime.now().isoformat()
    entry = f"[{timestamp}] trigger={trigger} project={project} articles={articles_created}\n"

    CODE_MEMORY_PATH.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(entry)


def main():
    parser = argparse.ArgumentParser(description="Compile claude-mem observations to vault")
    parser.add_argument("--trigger", choices=["session-end", "pre-compact", "manual"],
                        default="manual", help="What triggered this compilation")
    parser.add_argument("--project", type=str, default=None,
                        help="Project name to compile")
    parser.add_argument("--since", type=str, default=None,
                        help="Only process observations after this date (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be compiled without writing")

    args = parser.parse_args()

    # Ensure vault exists
    get_vault_path()
    CODE_MEMORY_PATH.mkdir(parents=True, exist_ok=True)

    # For hook triggers, just log and ensure dirs exist
    # The actual compilation is done by the /compile skill via Claude
    # This script handles the scaffolding and logging
    if args.trigger in ("session-end", "pre-compact"):
        project = args.project or "general"
        ensure_project_dirs(project)
        log_compilation(args.trigger, project)
        print(f"vault-compiler: {args.trigger} logged for {project}")
        return

    # For manual trigger, ensure project dirs
    if args.project:
        ensure_project_dirs(args.project)
        log_compilation(args.trigger, args.project)
        print(f"vault-compiler: ready to compile {args.project}")
    else:
        print("vault-compiler: no project specified, use --project <name>")


if __name__ == "__main__":
    main()
