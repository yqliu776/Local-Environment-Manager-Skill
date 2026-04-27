#!/usr/bin/env python3
"""Validate the local skill folder."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


MAX_SKILL_NAME_LENGTH = 64


def validate_skill(skill_path: Path) -> tuple[bool, str]:
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as exc:
        return False, f"Invalid YAML in frontmatter: {exc}"

    if not isinstance(frontmatter, dict):
        return False, "Frontmatter must be a YAML dictionary"

    allowed_properties = {"name", "description", "license", "allowed-tools", "metadata"}
    unexpected_keys = set(frontmatter.keys()) - allowed_properties
    if unexpected_keys:
        return (
            False,
            "Unexpected key(s) in SKILL.md frontmatter: "
            + ", ".join(sorted(unexpected_keys)),
        )

    name = (frontmatter.get("name") or "").strip()
    if not name:
        return False, "Missing 'name' in frontmatter"
    if not re.match(r"^[a-z0-9-]+$", name):
        return False, f"Name '{name}' should be hyphen-case"
    if name.startswith("-") or name.endswith("-") or "--" in name:
        return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
    if len(name) > MAX_SKILL_NAME_LENGTH:
        return False, f"Name is too long ({len(name)} characters)"

    description = (frontmatter.get("description") or "").strip()
    if not description:
        return False, "Missing 'description' in frontmatter"
    if "<" in description or ">" in description:
        return False, "Description cannot contain angle brackets"
    if len(description) > 1024:
        return False, f"Description is too long ({len(description)} characters)"

    return True, "Skill is valid!"


def main() -> int:
    skill_path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    valid, message = validate_skill(skill_path)
    print(message)
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
