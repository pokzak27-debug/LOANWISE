#!/usr/bin/env python3
"""
Add FAQPage JSON-LD schema to HTML pages that have dl.faq-list.
Run: python3 add_faq_schema.py
"""
import os
import re
import json
import html

BASE = os.path.dirname(os.path.abspath(__file__))


def strip_html(text):
    """Remove HTML tags and decode entities."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return html.unescape(text)


def extract_faqs(content):
    """Extract (question, answer) pairs from dl.faq-list."""
    faq_match = re.search(
        r'<dl class="faq-list">(.*?)</dl>',
        content,
        re.DOTALL,
    )
    if not faq_match:
        return []
    block = faq_match.group(1)
    pairs = []
    for m in re.finditer(r'<dt>(.*?)</dt>\s*<dd>(.*?)</dd>', block, re.DOTALL):
        q = strip_html(m.group(1))
        a = strip_html(m.group(2))
        if q and a and len(a) < 5000:  # schema limit
            pairs.append((q, a))
    return pairs


def build_faq_json_ld(pairs, page_url):
    """Build FAQPage JSON-LD."""
    if not pairs:
        return None
    items = []
    for q, a in pairs:
        items.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a,
            },
        })
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": items,
    }


def add_schema_to_file(path):
    """Add FAQ schema to file if it has faq-list and no existing FAQPage schema."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "FAQPage" in content or '"@type": "FAQPage"' in content:
        return False  # Already has schema

    pairs = extract_faqs(content)
    if not pairs:
        return False

    canonical = re.search(r'<link rel="canonical" href="([^"]+)"', content)
    url = canonical.group(1) if canonical else f"https://loanwisecalc.com/{os.path.basename(path)}"
    schema = build_faq_json_ld(pairs, url)
    script = '\n  <script type="application/ld+json">\n' + json.dumps(schema, indent=2) + '\n  </script>\n'

    # Insert before </head>
    if script.strip() not in content:
        content = content.replace("</head>", script + "</head>")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def main():
    files = [
        f for f in os.listdir(BASE)
        if f.endswith(".html") and os.path.isfile(os.path.join(BASE, f))
        and "template" not in f.lower()
    ]
    updated = 0
    for fname in sorted(files):
        path = os.path.join(BASE, fname)
        if add_schema_to_file(path):
            print(f"Added FAQ schema: {fname}")
            updated += 1
    print(f"\nDone. Updated {updated} pages.")


if __name__ == "__main__":
    main()
