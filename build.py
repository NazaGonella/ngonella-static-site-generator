import os
import subprocess
from pathlib import Path
from datetime import datetime

home_path : str = "./home.md"
css_path = Path("style.css").resolve()  # absolute path to CSS

markdown_files = list(Path(".").rglob("*.md"))
paired_files = [(md, md.parent / "index.html") for md in markdown_files]

current_date = datetime.now().strftime("%B %d, %Y")

print("### BUILD ###")
for md, html in paired_files:
    mtime_md = md.stat().st_mtime
    if html.exists():
        mtime_html = html.stat().st_mtime
        if mtime_html >  mtime_md:
            continue

    # compute CSS path relative to html file
    rel_css = os.path.relpath(css_path, start=html.parent)

    subprocess.run([
        "pandoc",
        "-s", str(md),
        "-o", str(html),
        "--css", rel_css,
        "-V", "title="
    ])

    # Read current content
    content = html.read_text(encoding="utf-8")

    # Replace $DATE$ with current date
    content = content.replace("%DATE%", current_date)

    # Write back
    html.write_text(content, encoding="utf-8")

    print(md, "->", html)
