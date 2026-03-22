#!/usr/bin/env python3
"""
Monetization Scaling: Add missing ad-inline to calculator pages.
Ensures consistent ad placement across the site for AdSense approval.
"""
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))

AD_INLINE = '''
    <div class="ad-container"><div class="ad-slot ad-inline" aria-label="Advertisement">
      <div class="ad-placeholder">Advertisement</div>
    </div></div>

'''

def add_ad_inline(path):
    """Add ad-inline after disclaimer if missing. Returns True if modified."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "ad-slot ad-inline" in content:
        return False

    # Pattern: after disclaimer </p>, before silo-links or related or content-section
    patterns = [
        # Country pages, personal-loan: disclaimer -> silo-links
        (r'(<p class="disclaimer">[^<]*(?:<a [^>]*>[^<]*</a>[^<]*)*</p>\s*)\n(\s*<nav class="silo-links")', r'\1' + AD_INLINE + r'\2'),
        # simple-interest: disclaimer -> related-calculators (no silo)
        (r'(<p class="disclaimer">[^<]*(?:<a [^>]*>[^<]*</a>[^<]*)*</p>\s*)\n(\s*<section class="related-calculators")', r'\1' + AD_INLINE + r'\2'),
        # Fallback: disclaimer -> next section
        (r'(<p class="disclaimer">[^<]*(?:<a [^>]*>[^<]*</a>[^<]*)*</p>\s*)\n(\s*<section)', r'\1' + AD_INLINE + r'\2'),
    ]

    for pat, repl in patterns:
        new_content = re.sub(pat, repl, content, count=1)
        if new_content != content:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            return True
    return False

def main():
    targets = [
        "loan-calculator-australia.html",
        "loan-calculator-canada.html",
        "loan-calculator-morocco.html",
        "loan-calculator-uae.html",
        "loan-calculator-uk.html",
        "loan-calculator-usa.html",
        "personal-loan-calculator.html",
        "simple-interest-calculator.html",
    ]
    updated = 0
    for fname in targets:
        path = os.path.join(BASE, fname)
        if os.path.isfile(path) and add_ad_inline(path):
            print(f"Added ad-inline: {fname}")
            updated += 1
    print(f"\nDone. Updated {updated} pages.")

if __name__ == "__main__":
    main()
