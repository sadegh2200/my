#!/usr/bin/env python3
"""Install both bundled skills project-locally, without duplicate skill IDs.

Relative symlinks keep each skill's scripts/references/assets together and work
when the checkout is moved. Never replaces an unrelated installed skill.
"""
from pathlib import Path
import os
import re

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("maalsadiqeen-1", "maalsadiqeen-reel")


def install(root: Path = ROOT) -> list[Path]:
    destination = root / ".agents" / "skills"
    destination.mkdir(parents=True, exist_ok=True)
    ids = set()
    installed = []
    for name in SKILLS:
        source = root / name
        text = (source / "SKILL.md").read_text(encoding="utf-8")
        match = re.search(r"^name:\s*(\S+)\s*$", text, re.M)
        if not match or match[1] != name or match[1] in ids:
            raise ValueError(f"Missing, conflicting or unexpected skill ID: {name}")
        ids.add(match[1])
        link = destination / name
        if link.is_symlink():
            if link.resolve() != source.resolve():
                raise FileExistsError(f"Refusing to replace another skill: {link}")
        elif link.exists():
            raise FileExistsError(f"Refusing to replace another skill: {link}")
        else:
            link.symlink_to(os.path.relpath(source, destination), target_is_directory=True)
        installed.append(link)
        print(f"Installed {match[1]} -> {link.relative_to(root)}")
    return installed


if __name__ == "__main__":
    install()
