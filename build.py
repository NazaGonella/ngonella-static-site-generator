#!/bin/python

import os
import sys
import subprocess
import json
from pathlib import Path

css_path: Path = Path("style.css").resolve()
ignored_mds = [Path("./README.md")]

rebuild_all = "--all" in sys.argv

markdown_files = [md for md in Path(".").rglob("*.md") if md not in ignored_mds]
paired_files = [(md, md.parent / "index.html") for md in markdown_files]


with open("metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

author = metadata["author"]
templates_path = metadata["templates_path"]

print("### BUILD ###")

for md, html in paired_files:
    if not rebuild_all:
        if html.exists() and html.stat().st_mtime > md.stat().st_mtime:
            continue

    relative_path_css = os.path.relpath(css_path, start=html.parent)

    template_to_use = "template-home.html"
    with md.open("r", encoding="utf-8") as f:
        lines = f.readlines()
        if lines[0].strip() == "---":
            for line in lines[1:]:
                line = line.strip()
                if line == "---":
                    break
                if line.startswith("template:"):
                    template_to_use = line.split(":", 1)[1].strip()
    
    subprocess.run([
        "pandoc", "-s", str(md),
        "-o", str(html),
        "--css", relative_path_css,
        "--template", f"{templates_path}/{template_to_use}",
        "-M", f"author={author}",
        "-f", "markdown+pipe_tables"
    ])

    print(md, "->", html)
