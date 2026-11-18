#!/usr/bin/env python3
"""Create a clean Skill3D production folder from repository templates."""
from pathlib import Path
import argparse, re, shutil

HERE = Path(__file__).resolve().parents[1]
TEMPLATES = HERE / "templates"

def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip()).strip("-").lower()
    if not slug:
        raise SystemExit("Project name must contain letters or numbers.")
    return slug

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name", help="Project name")
    ap.add_argument("--root", default=".", help="Workspace root (default: current directory)")
    args = ap.parse_args()
    slug = slugify(args.name)
    project = (Path(args.root).expanduser().resolve() / slug)
    if project.exists() and any(project.iterdir()):
        raise SystemExit(f"Refusing to overwrite non-empty project: {project}")
    for folder in ["input/audio", "input/references", "production", "assets/characters", "assets/props", "assets/environments", "blender", "renders/stills", "renders/frames", "output", "logs"]:
        (project / folder).mkdir(parents=True, exist_ok=True)
    for name in ["PROJECT-BRIEF.md", "SHOT-LIST.md", "ASSET-MANIFEST.md", "AUDIO-MAP.csv", "CONTINUITY.md"]:
        shutil.copy2(TEMPLATES / name, project / "production" / name)
    (project / "production" / "SOURCE-MANIFEST.md").write_text(
        "# Source Manifest\n\nList the original animation script, dialogue script, dialogue audio, and visual references here. Do not modify the originals.\n",
        encoding="utf-8")
    (project / "README.md").write_text(
        f"# {args.name}\n\nSkill3D production workspace.\n\n"
        "Put the user's original animation script and dialogue script in input/, "
        "dialogue audio in input/audio/, and references in input/references/. "
        "Keep source files unchanged.\n", encoding="utf-8")
    print(project)

if __name__ == "__main__":
    main()
