import subprocess
import sys
import os
from datetime import datetime


if len(sys.argv) != 3:
    print("Usage: python create-post.py <file_name> <post_title>")
    sys.exit(1)

file_name = sys.argv[1]
post_title = sys.argv[2]

posts_path : str = "./posts"


# creates the posts and post entry folder

os.makedirs(f"{posts_path}/{file_name}", exist_ok=True)

header : str = f"""%{post_title}

<header>
    <a class="name" href="../../index.html">Nazareno Gonella</a><nav><a class="title" href="">BLOG</a> &nbsp;&nbsp; <a class="title" href="mailto:nazagonella2@gmail.com">CONTACT</a> &nbsp;&nbsp; <a class="title" href="">CV</a></nav>
</header>

<hr />

## {post_title}

%DATE%

---
"""

with open(f"{posts_path}/{file_name}/{file_name}.md", "w", encoding="utf-8") as f:
    f.write(header)


# adds the post entry to home.md

home_path : str = "./home.md"
date_entry = datetime.now().strftime("%d/%m/%Y")
post_entry : str = f"{date_entry}: [**{post_title}**]({posts_path}/{file_name}/index.html)  \n"

with open(home_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

lines.insert(6, post_entry)

with open(home_path, "w", encoding="utf-8") as f:
    f.writelines(lines)


subprocess.run([
    "vim",
    f"{posts_path}/{file_name}/{file_name}.md"
])
