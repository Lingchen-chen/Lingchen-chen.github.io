#!/usr/bin/env python3
"""Package the static website without publishing source files or tooling."""

from pathlib import Path
import shutil

from check_site import check_site

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "dist"


def build():
    check_site(ROOT)
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()
    for name in ("index.html", "404.html", "robots.txt", "sitemap.xml", ".nojekyll", "LICENSE"):
        shutil.copy2(ROOT / name, OUTPUT / name)
    for name in ("assets", "publications", "_design-preview"):
        shutil.copytree(ROOT / name, OUTPUT / name, ignore=shutil.ignore_patterns(".DS_Store"))
    check_site(OUTPUT)
    print(f"Static website ready: {OUTPUT}")


if __name__ == "__main__":
    build()
