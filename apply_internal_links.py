#!/usr/bin/env python3
"""
Automatic internal linking system for LoanWise.

Applies to ALL HTML pages in the project:
- Breadcrumb navigation (near top)
- Related Calculators section (min 5 links, silo-aware)
- Silo links on parent pages (In this section: $15k · $20k · ...)
- Ensures no orphan pages, strong topical clusters, better crawlability

Run: python3 apply_internal_links.py

Run after generate_calculator_pages.py for newly generated pages.
"""

import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
EXCLUDE = {"templates", "node_modules"}

from config.internal_linking import (
    classify_page,
    get_related_links,
    get_silo_links,
    get_silo_links_for_amount_page,
)


def discover_pages():
    """All .html files in base dir (exclude subdirs like templates)."""
    files = set()
    for f in os.listdir(BASE):
        if f.endswith(".html") and os.path.isfile(os.path.join(BASE, f)):
            files.add(f)
    return files


def build_breadcrumb(info: dict) -> str:
    """Build breadcrumb nav HTML from page info."""
    if info.get("current_label") == "Home":
        return '<nav class="breadcrumb" aria-label="Breadcrumb">\n      <span aria-current="page">Home</span>\n    </nav>'
    parts = ['<a href="index.html">Home</a>']
    parent = info.get("parent")
    parent_label = info.get("parent_label")
    # Only add parent link if it's not index (avoid "Home › Home")
    if parent and parent_label and parent != "index.html":
        parts.append('<span class="breadcrumb-sep" aria-hidden="true">›</span>')
        parts.append(f'<a href="{parent}">{parent_label}</a>')
    parts.append('<span class="breadcrumb-sep" aria-hidden="true">›</span>')
    parts.append(f'<span aria-current="page">{info["current_label"]}</span>')
    return '<nav class="breadcrumb" aria-label="Breadcrumb">\n      ' + "\n      ".join(parts) + "\n    </nav>"


def build_related_section(links: list) -> str:
    """Build Related Calculators section HTML."""
    items = "\n        ".join(f'<li><a href="{h}">{l}</a></li>' for h, l in links)
    return f'''    <section class="related-calculators" aria-labelledby="related-calculators-heading">
      <h2 id="related-calculators-heading">Related Calculators</h2>
      <ul class="related-calculators-list">
        {items}
      </ul>
    </section>'''


def apply_breadcrumb(content: str, bc_html: str) -> str:
    """Insert or replace breadcrumb after <div class="container">."""
    # Pattern: right after <div class="container">, before next element
    bc_pattern = r'<nav class="breadcrumb" aria-label="Breadcrumb">.*?</nav>'
    if re.search(bc_pattern, content, re.DOTALL):
        content = re.sub(bc_pattern, bc_html, content, count=1, flags=re.DOTALL)
    else:
        # Insert after <div class="container"> and optional whitespace
        content = re.sub(
            r'(<div class="container">)\s*\n',
            r'\1\n' + bc_html + '\n    ',
            content,
            count=1,
        )
    return content


def apply_related_section(content: str, section_html: str) -> str:
    """Replace existing Related Calculators section or add before footer."""
    existing = re.search(
        r'<section class="related-calculators" aria-labelledby="related-calculators-heading">.*?</section>',
        content,
        re.DOTALL,
    )
    if existing:
        content = content[: existing.start()] + section_html + content[existing.end() :]
    else:
        # Add before container's closing </div> (so section is inside container)
        match = re.search(r'(</section>)\s*(</div>\s*<footer)', content, re.DOTALL)
        if match:
            content = content[: match.end(1)] + "\n" + section_html + "\n  " + content[match.start(2) : match.end(2)] + content[match.end() :]
    return content


def apply_silo_links(content: str, silo_html: str, fname: str) -> str:
    """Insert silo-links nav if not present. Place before first content-section after main."""
    if '<nav class="silo-links"' in content:
        return content  # Already has silo links
    # Insert before <section class="content-section (first one after </main>)
    match = re.search(r'\s*(<section class="content-section)', content)
    if match and "</main>" in content[: match.start()]:
        insert_pos = match.start(1)  # start of <section
        content = content[:insert_pos] + "\n\n" + silo_html + "\n\n    " + content[insert_pos:]
    return content


def ensure_h2_heading(content: str) -> str:
    """Related section should use h2 for consistency (some pages have h3)."""
    return re.sub(
        r'<h3 id="related-calculators-heading">Related Calculators</h3>',
        '<h2 id="related-calculators-heading">Related Calculators</h2>',
        content,
        count=1,
    )


def main():
    all_files = discover_pages()
    updated = 0

    for fname in sorted(all_files):
        path = os.path.join(BASE, fname)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        info = classify_page(fname, all_files)
        changed = False

        # 1. Breadcrumb
        bc_html = build_breadcrumb(info)
        new_content = apply_breadcrumb(content, bc_html)
        if new_content != content:
            content = new_content
            changed = True

        # 2. Related Calculators (min 5 links)
        links = get_related_links(fname, info, all_files)
        if len(links) >= 5:
            section_html = build_related_section(links)
            content = apply_related_section(content, section_html)
            content = ensure_h2_heading(content)
            changed = True

        # 3. Silo links for parent pages (or amount pages)
        silo_html = get_silo_links(fname, all_files)
        if not silo_html:
            silo_html = get_silo_links_for_amount_page(fname, info, all_files)
        if silo_html:
            new_content = apply_silo_links(content, silo_html, fname)
            if new_content != content:
                content = new_content
                changed = True

        if changed:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated: {fname}")
            updated += 1

    print(f"\nDone. Updated {updated} pages.")


if __name__ == "__main__":
    main()
