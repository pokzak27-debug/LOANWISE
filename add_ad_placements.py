#!/usr/bin/env python3
"""
Add optimized ad placement containers to all HTML pages.

Placements:
- ad-top: below H1 (after page-header)
- ad-inline: after calculator section (after disclaimer)
- ad-middle: between content-section and related-calculators
- ad-bottom: at bottom of page (before footer)

Run: python3 add_ad_placements.py
"""

import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))

AD_TOP = '''    <div class="ad-slot ad-top" aria-label="Advertisement">
      <div class="ad-placeholder">Advertisement</div>
    </div>

'''

AD_INLINE = '''
    <div class="ad-slot ad-inline" aria-label="Advertisement">
      <div class="ad-placeholder">Advertisement</div>
    </div>

'''

AD_MIDDLE = '''
    <div class="ad-slot ad-middle" aria-label="Advertisement">
      <div class="ad-placeholder">Advertisement</div>
    </div>

'''

AD_BOTTOM = '''
    <div class="ad-slot ad-bottom" aria-label="Advertisement">
      <div class="ad-placeholder">Advertisement</div>
    </div>

'''


def add_ads_to_calculator_page(content):
    """Add all 4 ad placements to a calculator page."""
    modified = content

    # 1. ad-top: after page-header </header>, before <main class="calculator">
    if 'ad-slot ad-top' not in modified:
        pattern = r'(</header>\s*)\n(\s*<main class="calculator">)'
        replacement = r'\1\n' + AD_TOP + r'\2'
        modified = re.sub(pattern, replacement, modified, count=1)

    # 2. ad-inline: after disclaimer </p>, before <section class="content-section">
    if 'ad-slot ad-inline' not in modified:
        pattern = r'(<p class="disclaimer">[^<]*</p>\s*)\n(\s*<section class="content-section">)'
        replacement = r'\1' + AD_INLINE + r'\2'
        modified = re.sub(pattern, replacement, modified, count=1)
        # Fallback: after any disclaimer
        if 'ad-slot ad-inline' not in modified:
            pattern = r'(</p>\s*)(<section class="content-section">)'
            if re.search(pattern, modified) and 'ad-inline' not in modified:
                modified = re.sub(
                    r'(<p class="disclaimer">.*?</p>\s*)',
                    r'\1' + AD_INLINE,
                    modified,
                    count=1,
                    flags=re.DOTALL,
                )

    # 3. ad-middle: after content-section </section>, before related-calculators
    if 'ad-slot ad-middle' not in modified:
        # Capture FULL related-calculators opening tag so we don't lose aria-labelledby etc
        pattern = r'(</section>\s*)\n(\s*)(<section class="related-calculators"[^>]*>)'
        replacement = r'\1\n' + AD_MIDDLE.strip() + r'\n\2\3'
        modified = re.sub(pattern, replacement, modified, count=1)

    # 4. ad-bottom: after related-calculators </section>, before container </div>
    if 'ad-slot ad-bottom' not in modified:
        # After </ul>\n    </section> of related-calculators, before \n  </div>
        pattern = r'(</section>\s*)\n(\s*</div>\s*\n\s*<footer)'
        replacement = r'\1\n' + AD_BOTTOM + r'\2'
        modified = re.sub(pattern, replacement, modified, count=1)
        if 'ad-slot ad-bottom' not in modified:
            pattern = r'(<section class="related-calculators"[^>]*>.*?</section>)\s*\n(\s*</div>)'
            replacement = r'\1\n' + AD_BOTTOM + r'\2'
            modified = re.sub(pattern, replacement, modified, count=1, flags=re.DOTALL)

    return modified


def add_ads_to_simple_page(content):
    """Add ad-top and ad-bottom to non-calculator pages."""
    modified = content

    # ad-top: after first </header> (page header) or after first h1 block
    if 'ad-slot ad-top' not in modified:
        # For about/contact: after <main class="page-content"> and h1
        pattern = r'(<h1[^>]*>.*?</h1>\s*<p class="last-updated">.*?</p>\s*)\n(\s*<section class="content-section">)'
        replacement = r'\1\n' + AD_TOP + r'\2'
        modified = re.sub(pattern, replacement, modified, count=1, flags=re.DOTALL)
        if 'ad-slot ad-top' not in modified:
            # After first h1
            pattern = r'(</h1>\s*)\n(\s*<)'
            replacement = r'\1\n' + AD_TOP + r'\2'
            modified = re.sub(pattern, replacement, modified, count=1)

    # ad-bottom: before footer
    if 'ad-slot ad-bottom' not in modified:
        pattern = r'(</section>\s*)\n(\s*</div>\s*\n\s*<footer)'
        replacement = r'\1\n' + AD_BOTTOM + r'\2'
        modified = re.sub(pattern, replacement, modified, count=1)

    return modified


def process_file(path, fname):
    """Add ad placements to a single file. Returns True if modified."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "ad-slot" in content:
        return False  # Already has ads

    # Exclude templates
    if "template" in fname.lower():
        return False

    has_calculator = '<main class="calculator">' in content
    has_content_section = '<section class="content-section">' in content
    has_related = 'related-calculators' in content

    if has_calculator:
        new_content = add_ads_to_calculator_page(content)
    elif has_content_section or has_related:
        new_content = add_ads_to_simple_page(content)
    else:
        return False  # Skip pages without standard structure

    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False


def main():
    files = sorted(
        f for f in os.listdir(BASE)
        if f.endswith(".html") and os.path.isfile(os.path.join(BASE, f))
    )
    exclude = {"templates"}
    files = [f for f in files if not any(ex in f for ex in exclude)]

    updated = 0
    for fname in files:
        path = os.path.join(BASE, fname)
        if process_file(path, fname):
            print(f"Added ads: {fname}")
            updated += 1

    print(f"\nDone. Updated {updated} pages.")


if __name__ == "__main__":
    main()
