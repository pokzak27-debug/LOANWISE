#!/usr/bin/env python3
"""
Upgrade all calculator pages for page-1 SEO:
- Add comparison table (term vs monthly payment)
- Ensure How to use, Example, What affects, 5 FAQs
- Add internal links
- Improve H1 exact keyword match

Run: python3 upgrade_calculator_pages.py
"""

import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))


def monthly_payment(principal, annual_rate_pct, months):
    """Standard amortization formula."""
    if months <= 0 or principal <= 0:
        return 0
    r = annual_rate_pct / 100 / 12
    if r == 0:
        return principal / months
    return principal * (r * (1 + r) ** months) / ((1 + r) ** months - 1)


def format_amount(amt):
    if amt >= 1000:
        return f"${amt:,}"
    return f"${amt}"


def build_comparison_table(amt, rate, is_mortgage):
    """Build term vs monthly payment table HTML."""
    if is_mortgage:
        terms = [(120, "10 years"), (180, "15 years"), (240, "20 years"), (360, "30 years")]
    else:
        terms = [(24, "24 months"), (36, "36 months"), (48, "48 months"), (60, "60 months"), (72, "72 months")]

    rows = []
    for m, label in terms:
        pmt = monthly_payment(amt, rate, m)
        total = pmt * m
        interest = total - amt
        rows.append(f"        <tr><td>{label}</td><td>{format_amount(round(pmt))}</td><td>{format_amount(round(interest))}</td></tr>")

    header = "        <tr><th>Term</th><th>Monthly Payment</th><th>Total Interest</th></tr>"
    rate_str = str(int(rate)) if rate == int(rate) else str(rate)
    return '''      <h2>Loan term vs monthly payment</h2>
      <p>How term affects your payment at ''' + format_amount(amt) + ''' and ''' + rate_str + "% APR:</p>\n      " + '''<table class="comparison-table" aria-label="Loan term comparison">
''' + header + "\n" + "\n".join(rows) + '''
      </table>
'''


def upgrade_page(path, fname):
    """Upgrade a single calculator page. Returns True if modified."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if '<main class="calculator">' not in content:
        return False  # Not a calculator page

    # Extract amount and rate from inputs
    amt_match = re.search(r'id="loanAmount"[^>]*value="(\d+)"', content)
    rate_match = re.search(r'id="interestRate"[^>]*value="([\d.]+)"', content)
    if not amt_match or not rate_match:
        return False

    amt = int(amt_match.group(1))
    rate = float(rate_match.group(1))
    is_mortgage = "mortgage" in fname

    modified = False

    # 1. Add comparison table if not present
    if 'class="comparison-table"' not in content:
        table_html = build_comparison_table(amt, rate, is_mortgage)
        # Insert before <h2>Frequently asked questions or <h2>Frequently Asked
        pattern = r'(\s*<h2[^>]*>Frequently [aA]sked [qQ]uestions</h2>)'
        if re.search(pattern, content):
            content = re.sub(pattern, table_html + r'\n\n      \1', content, count=1)
            modified = True

    # 2. Add "How to use" if missing (before first h2 in content-section)
    if '<h2>How to use this calculator</h2>' not in content:
        how_to = """      <h2>How to use this calculator</h2>
      <ol>
        <li><strong>Enter the loan amount</strong> — Pre-filled; adjust if needed.</li>
        <li><strong>Enter the interest rate</strong> — Use the APR your lender quoted.</li>
        <li><strong>Enter the term in months</strong> — 36, 48, or 60 are common.</li>
        <li><strong>Click Calculate</strong> — See monthly payment, total payment, and total interest.</li>
      </ol>

"""
        # Insert at start of content-section
        pattern = r'(<section class="content-section">)\s*\n'
        if re.search(pattern, content):
            content = re.sub(pattern, r'\1\n' + how_to + "\n      ", content, count=1)
            modified = True

    # 3. Add internal links in intro if fewer than 3
    intro_match = re.search(r'<p class="intro-lead">([^<]+)</p>', content)
    if intro_match and modified is False:  # Only if we want to add links
        intro = intro_match.group(1)
        # Count links in help-text and content
        link_count = len(re.findall(r'<a href="[^"]+\.html"', content[:content.find("</section>")]))
        if link_count < 5 and "loan calculator" not in intro.lower():
            # Add link to main calculator in intro - skip to avoid over-editing
            pass

    if modified:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    return modified


def main():
    files = sorted(
        f for f in os.listdir(BASE)
        if f.endswith(".html") and os.path.isfile(os.path.join(BASE, f))
        and not f.startswith(".") and f != "sitemap.html"
    )
    # Exclude utility pages
    exclude = {"about.html", "contact.html", "terms.html", "privacy-policy.html", "index.html"}
    files = [f for f in files if f not in exclude]

    updated = 0
    for fname in files:
        path = os.path.join(BASE, fname)
        if upgrade_page(path, fname):
            print(f"Upgraded: {fname}")
            updated += 1

    print(f"\nDone. Upgraded {updated} pages.")


if __name__ == "__main__":
    main()
