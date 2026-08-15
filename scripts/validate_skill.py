#!/usr/bin/env python3
"""Dependency-free structural validator for this Agent Skill."""
from __future__ import annotations

import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def parse_simple_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        fail("SKILL.md frontmatter closing delimiter not found")
    block = text[4:end]
    out: dict[str, str] = {}
    for line in block.splitlines():
        if not line or line.startswith(" ") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        out[key.strip()] = value.strip().strip('"\'')
    return out


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    skill = root / "SKILL.md"
    if not skill.is_file():
        fail(f"Missing {skill}")

    text = skill.read_text(encoding="utf-8")
    meta = parse_simple_frontmatter(text)
    name = meta.get("name", "")
    description = meta.get("description", "")

    if not name:
        fail("frontmatter.name is required")
    if not NAME_RE.fullmatch(name):
        fail("name must contain lowercase letters, numbers, and single hyphens only")
    if len(name) > 64:
        fail("name must be <= 64 characters")
    if name != root.name:
        fail(f"name '{name}' must match parent directory '{root.name}'")
    if not description:
        fail("frontmatter.description is required")
    if len(description) > 1024:
        fail("description must be <= 1024 characters")

    body = text[text.find("\n---\n", 4) + 5 :]
    if len(body.splitlines()) > 500:
        fail("SKILL.md body should stay under 500 lines for progressive disclosure")

    refs = re.findall(r"\]\((references/[^)]+)\)", body)
    missing = [ref for ref in refs if not (root / ref).is_file()]
    if missing:
        fail("Missing referenced files: " + ", ".join(sorted(set(missing))))

    print(f"OK: {name}")
    print(f"SKILL.md lines: {len(text.splitlines())}")
    print(f"Reference links checked: {len(refs)}")


if __name__ == "__main__":
    main()
