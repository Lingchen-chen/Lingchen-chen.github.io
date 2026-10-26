#!/usr/bin/env python3
"""Check the static site's internal links, assets, and bibliography coverage."""

from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.ids = set()
        self.links = []
        self.papers = 0
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            value = attrs["id"]
            if value in self.ids:
                raise ValueError(f"Duplicate ID in {self.path}: {value}")
            self.ids.add(value)
        if tag == "article" and attrs.get("class") == "paper":
            self.papers += 1
        for name in ("href", "src"):
            if attrs.get(name):
                self.links.append(attrs[name])


def check_site(directory):
    directory = directory.resolve()
    paths = [directory / "index.html", directory / "publications/index.html", directory / "404.html"]
    paths.extend(sorted((directory / "_design-preview").glob("*.html")))
    pages = {path: Page(path) for path in paths}
    checked = 0
    for path, page in pages.items():
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            if url.path.startswith("/"):
                target = directory / unquote(url.path.lstrip("/"))
            elif url.path:
                target = path.parent / unquote(url.path)
            else:
                target = path
            target = target.resolve()
            if not target.is_relative_to(directory):
                raise ValueError(f"Link leaves the site: {path}: {link}")
            if target.is_dir():
                target /= "index.html"
            if not target.is_file():
                raise ValueError(f"Missing file: {path}: {link}")
            if url.fragment:
                target_page = pages.get(target) or Page(target)
                if unquote(url.fragment) not in target_page.ids:
                    raise ValueError(f"Missing anchor: {path}: {link}")
            checked += 1

    bibliography = (ROOT / "data/publications.bib").read_text(encoding="utf-8")
    expected = set(re.findall(r"@(?:article|inproceedings|misc)\s*\{\s*([^,\s]+)\s*,", bibliography, re.IGNORECASE))
    publications = pages[directory / "publications/index.html"]
    missing = expected - publications.ids
    if missing or publications.papers != len(expected):
        raise ValueError(f"Bibliography mismatch: {sorted(missing)}; expected {len(expected)} papers, found {publications.papers}")
    if not (directory / ".nojekyll").is_file():
        raise ValueError("Missing .nojekyll")
    print(f"Validated {len(pages)} pages, {checked} internal references, and all {len(expected)} publications.")


if __name__ == "__main__":
    check_site(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT)
