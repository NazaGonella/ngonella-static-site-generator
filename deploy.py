import subprocess
import sys
from pathlib import Path
from datetime import datetime


# Replaces %DATE% in Markdown and HTML files with the current post date,
# and %DATEHOME% with the current home date, updating only files that contain these placeholders.
def update_dates():
    markdown_files = list(Path(".").rglob("*.md"))
    paired_files = [(md, md.parent / "index.html") for md in markdown_files]

    post_date = datetime.now().strftime("%B %d, %Y")
    home_date = datetime.now().strftime("%d/%m/%Y")
    date_updated : bool = False
    print("### FIXING DATE ###")
    for md, html in paired_files:
        if md.exists():
            md_content = md.read_text(encoding="utf-8")
            date_pattern = ""
            date = post_date
            if ("%DATE%" in md_content):
                date_pattern = "%DATE%"
            elif ("%DATEHOME%" in md_content):
                date_pattern = "%DATEHOME%"
                date = home_date
            if date_pattern:
                md_content = md_content.replace(date_pattern, date)
                md.write_text(md_content, encoding="utf-8")
                print("-> ", md)
                date_updated = True
        if html.exists():
            html_content = html.read_text(encoding="utf-8")
            date_pattern = ""
            date = post_date
            if ("%DATE%" in html_content):
                date_pattern = "%DATE%"
            elif ("%DATEHOME%" in html_content):
                date_pattern = "%DATEHOME%"
                date = home_date
            if date_pattern:
                html_content = html_content.replace(date_pattern, date)
                html.write_text(html_content, encoding="utf-8")
                print("-> ", html)
                date_updated = True

    if not date_updated:
        print("No %DATE% found.")
    print("")


def push_to_master():
    working_branch = "working"

    try:
        subprocess.run(["git", "checkout", "master"], check=True)
        subprocess.run(["git", "merge", "working"], check=True)
        subprocess.run(["git", "push", "origin", "master"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        sys.exit(1)

    print("Master branch updated")


def main():
    if "--no-date" not in sys.argv:
        update_dates()
    push_to_master()


if __name__ == "__main__":
    main()