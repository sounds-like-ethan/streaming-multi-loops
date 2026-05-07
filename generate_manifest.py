#!/usr/bin/env python3
"""Scan audio/<piece>/<category>/ and rewrite manifest.json.

Folder layout:

    audio/
      Dusk Song/
        world_sounds/
        neurotones/
        foundation/
        harmony/
        melody/
        accents/
        low_end/
      Another Piece/
        ...

Workflow:
  1. Create a new folder under audio/ named after the piece (any human-readable name).
  2. Run `python3 generate_manifest.py` — it ensures the 7 category subfolders exist
     inside every piece folder.
  3. Drop your audio files into the right category subfolders.
  4. Run the script again to refresh manifest.json.

To rename a category, edit CATEGORIES below AND the matching CATEGORIES array
near the top of index.html — the IDs in both files must match.
"""

import json
from pathlib import Path

CATEGORIES = [
    ("world_sounds", "World Sounds"),
    ("neurotones",   "Neurotones"),
    ("foundation",   "Foundation"),
    ("harmony",      "Harmony"),
    ("melody",       "Melody"),
    ("accents",      "Accents"),
    ("low_end",      "Low End"),
]

AUDIO_EXTS = {".wav", ".mp3", ".ogg", ".m4a", ".flac", ".aac", ".webm", ".opus"}


def main() -> None:
    root = Path(__file__).resolve().parent
    audio_dir = root / "audio"
    audio_dir.mkdir(exist_ok=True)

    piece_dirs = sorted(
        p for p in audio_dir.iterdir()
        if p.is_dir() and not p.name.startswith(".")
    )

    if not piece_dirs:
        print("No pieces found. Create a folder under audio/ "
              "(e.g., 'audio/Dusk Song/') and rerun.\n")

    pieces = []
    for piece_dir in piece_dirs:
        name = piece_dir.name
        cats = []
        total = 0
        for cid, label in CATEGORIES:
            cat_dir = piece_dir / cid
            cat_dir.mkdir(parents=True, exist_ok=True)
            files = sorted(
                p.name for p in cat_dir.iterdir()
                if p.is_file()
                and p.suffix.lower() in AUDIO_EXTS
                and not p.name.startswith(".")
            )
            cats.append({"id": cid, "label": label, "files": files})
            total += len(files)
        pieces.append({"id": name, "label": name, "categories": cats})
        print(f"  {name:30s} {total:3d} file(s) across {len(CATEGORIES)} categories")

    manifest = {"pieces": pieces}
    out_path = root / "manifest.json"
    out_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"\nwrote {out_path.relative_to(root)}")


if __name__ == "__main__":
    main()
