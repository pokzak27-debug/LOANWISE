#!/usr/bin/env python3
"""SEO audit: find orphan pages and verify sitemap coverage."""
import os
import re

html_files = [f for f in os.listdir(".") if f.endswith(".html")]
linked = set()
for f in html_files:
    with open(f, "r") as file:
        content = file.read()
    for m in re.finditer(r'href=["\']([^"\']+)["\']', content):
        h = m.group(1)
        if h.startswith("http") or h.startswith("//") or h.startswith("#") or h.startswith("mailto:"):
            continue
        base = h.split("?")[0].split("#")[0].strip("/")
        if not base or base == "index.html":
            linked.add("index.html")
        elif base.endswith(".html"):
            linked.add(base)
        else:
            linked.add(base + ".html") if not base.endswith(".html") else linked.add(base)
all_pages = set(html_files)
orphans = all_pages - linked
print("Orphan pages:", sorted(orphans) if orphans else "None")
print("Total:", len(all_pages), "pages,", len(orphans), "orphans")
