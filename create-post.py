#!/usr/bin/env python3

import subprocess
import sys
import os
import json
from datetime import datetime


if len(sys.argv) != 3:
    print("Usage: python create-post.py <file_name> <post_title>")
    sys.exit(1)

with open("metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

file_name = sys.argv[1]
post_title = sys.argv[2]


posts_path : str = metadata["posts_path"]


# creates the posts and post entry folder
os.makedirs(f"{posts_path}/{file_name}", exist_ok=True)

date_header : datetime = datetime.now().strftime("%B {S}, %Y").replace('{S}', str(datetime.now().day))

# default template for articles
header : str = f"""---
title: {post_title}
date: {date_header}
template: template-article.html
---

---

"""

with open(f"{posts_path}/{file_name}/{file_name}.md", "w", encoding="utf-8") as f:
    f.write(header)


# adds the post entry to home.md

home_path : str = metadata["home_path"]
date_entry : datetime = datetime.now().strftime("%d/%m/%Y")
post_entry : str = f"\n{date_entry} [{post_title}]({posts_path[1:]}/{file_name}/)  \n"

anchor = "<div class=posts>"

with open(home_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if anchor in line:
        lines.insert(i + 1, post_entry)
        break

with open(home_path, "w", encoding="utf-8") as f:
    f.writelines(lines)


subprocess.run([
    "vim",
    f"{posts_path}/{file_name}/{file_name}.md"
])
