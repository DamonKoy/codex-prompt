#!/usr/bin/env python3
"""Dependency-free structural checks for the Prompt Refiner plugin."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "prompt-refiner"
MANIFEST = PLUGIN / ".codex-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
SKILL = PLUGIN / "skills" / "prompt-refiner" / "SKILL.md"
SKILL_UI = PLUGIN / "skills" / "prompt-refiner" / "agents" / "openai.yaml"


def fail(message: str) -> None:
    raise SystemExit(f"validation failed: {message}")


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot read {path.relative_to(ROOT)}: {error}")
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def main() -> None:
    for path in (MANIFEST, MARKETPLACE, SKILL, SKILL_UI, ROOT / "README.md", ROOT / "LICENSE"):
        if not path.is_file():
            fail(f"missing required file: {path.relative_to(ROOT)}")

    manifest = read_json(MANIFEST)
    if manifest.get("name") != "prompt-refiner":
        fail("plugin manifest name must be prompt-refiner")
    if manifest.get("skills") != "./skills/":
        fail("plugin manifest must expose ./skills/")
    if not isinstance(manifest.get("version"), str) or not manifest["version"]:
        fail("plugin manifest needs a version")
    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        fail("plugin manifest needs an interface object")
    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        fail("interface.defaultPrompt must contain one to three starter prompts")
    if any(not isinstance(prompt, str) or len(prompt) > 128 for prompt in prompts):
        fail("starter prompts must be strings of at most 128 characters")

    marketplace = read_json(MARKETPLACE)
    if marketplace.get("name") != "prompt-refiner":
        fail("marketplace name must be prompt-refiner")
    expected_source = {"source": "local", "path": "./plugins/prompt-refiner"}
    entries = marketplace.get("plugins")
    if not isinstance(entries, list) or len(entries) != 1:
        fail("marketplace must expose exactly one plugin")
    entry = entries[0]
    if not isinstance(entry, dict) or entry.get("name") != "prompt-refiner":
        fail("marketplace plugin name must be prompt-refiner")
    if entry.get("source") != expected_source:
        fail("marketplace source must point to ./plugins/prompt-refiner")

    skill_text = SKILL.read_text(encoding="utf-8")
    if not skill_text.startswith("---\nname: prompt-refiner\n"):
        fail("skill frontmatter must identify prompt-refiner")
    if "[TODO:" in skill_text or "[TODO:" in MANIFEST.read_text(encoding="utf-8"):
        fail("published files must not contain TODO placeholders")

    print("validation passed: prompt-refiner package is structurally complete")


if __name__ == "__main__":
    main()
