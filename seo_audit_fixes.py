#!/usr/bin/env python3
"""
SEO quality audit and fixes for LoanWise.
- Fix canonical URL inconsistency
- Vary duplicate meta descriptions
- Vary duplicate H1s
- Check broken links
- Strengthen thin content
"""

import os
import re
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
CANONICAL_BASE = "https://loanwisecalc.com"


def discover_pages():
    return set(
        f for f in os.listdir(BASE)
        if f.endswith(".html") and os.path.isfile(os.path.join(BASE, f))
    )


def fix_canonicals(files):
    """Fix pages using loanwise.site to use loanwisecalc.com"""
    fixes = []
    for fname in files:
        path = os.path.join(BASE, fname)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if "loanwise.site" in content:
            content = content.replace("https://www.loanwise.site/", f"{CANONICAL_BASE}/")
            content = content.replace("https://www.loanwise.site", CANONICAL_BASE)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            fixes.append(fname)
    return fixes


def vary_car_loan_meta(files):
    """Vary car loan amount page meta descriptions."""
    car_amounts = sorted([
        f for f in files if re.match(r"car-loan-\d+-monthly-payment\.html", f)
    ], key=lambda x: int(re.search(r"car-loan-(\d+)-", x).group(1)))
    variations = [
        "Free calculator. Compare 48, 60, or 72 months. See monthly cost and total interest. No signup.",
        "Free tool. Dealer-ready numbers. Adjust rate and term. Compare before you buy. No signup.",
        "Free instant estimate. Compare terms. See total interest. Plan your budget. No signup.",
    ]
    for i, fname in enumerate(car_amounts):
        m = re.search(r"car-loan-(\d+)-", fname)
        amt = int(m.group(1))
        fmt = f"${amt:,}" if amt >= 1000 else f"${amt}"
        variation = variations[i % len(variations)]
        meta = f"{fmt} car loan payment in seconds. {variation}"
        path = os.path.join(BASE, fname)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(
            r'<meta name="description" content="[^"]*"',
            f'<meta name="description" content="{meta}"',
            content,
            count=1,
        )
        content = re.sub(
            r'<meta property="og:description" content="[^"]*"',
            f'<meta property="og:description" content="{meta}"',
            content,
            count=1,
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


def vary_business_loan_meta(files):
    """Vary business loan amount page meta descriptions."""
    for fname in ["business-loan-10000-payment.html", "business-loan-20000-payment.html", "business-loan-50000-payment.html"]:
        if fname not in files:
            continue
        amt = re.search(r"(\d+)", fname).group(1)
        metas = {
            "10000": "$10k business loan payment in seconds. Free tool. Plan cash flow. Compare terms. No signup.",
            "20000": "$20k business loan—see monthly payment and total cost. Free calculator. Plan before you borrow.",
            "50000": "$50k business loan payment estimate. Free tool. Model repayment. Compare rates. No signup.",
        }
        meta = metas.get(amt, "")
        if not meta:
            continue
        path = os.path.join(BASE, fname)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(
            r'<meta name="description" content="[^"]*"',
            f'<meta name="description" content="{meta}"',
            content,
            count=1,
        )
        content = re.sub(
            r'<meta property="og:description" content="[^"]*"',
            f'<meta property="og:description" content="{meta}"',
            content,
            count=1,
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


def vary_loan_amount_meta(files):
    """Vary general loan amount page meta - many use similar wording."""
    variations = [
        "{fmt} loan payment in seconds. Free calculator. See monthly cost and total interest. No signup. Calculate now.",
        "{fmt} loan—free payment estimate. Compare rates and terms. See total interest. No signup.",
        "Monthly payment for a {fmt} loan. Free tool. Adjust rate and term. No signup. Calculate now.",
    ]
    for i, fname in enumerate(sorted([
        f for f in files if re.match(r"loan-\d+-monthly-payment\.html", f)
    ], key=lambda x: int(re.search(r"loan-(\d+)-", x).group(1)))):
        m = re.search(r"loan-(\d+)-", fname)
        amt = int(m.group(1))
        fmt = f"${amt:,}" if amt >= 1000 else f"${amt}"
        meta = variations[i % len(variations)].format(fmt=fmt)
        path = os.path.join(BASE, fname)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(
            r'<meta name="description" content="[^"]*"',
            f'<meta name="description" content="{meta}"',
            content,
            count=1,
        )
        content = re.sub(
            r'<meta property="og:description" content="[^"]*"',
            f'<meta property="og:description" content="{meta}"',
            content,
            count=1,
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


def vary_h1_subtle(files):
    """Add subtle H1 variations for car/loan amount pages."""
    h1_variations = [
        " — Free, Fast Estimate",
        " — Free &amp; Fast Online",
        " — Free Online Calculator",
    ]
    for i, fname in enumerate(sorted([
        f for f in files if re.match(r"car-loan-\d+-monthly-payment\.html", f)
    ], key=lambda x: int(re.search(r"car-loan-(\d+)-", x).group(1)))):
        m = re.search(r"car-loan-(\d+)-", fname)
        amt = int(m.group(1))
        fmt = f"${amt:,}" if amt >= 1000 else f"${amt}"
        suffix = h1_variations[i % len(h1_variations)]
        new_h1 = f"<h1>Car Loan {fmt} Monthly Payment{suffix}</h1>"
        path = os.path.join(BASE, fname)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(
            r'<h1>Car Loan \$[\d,]+ Monthly Payment — [^<]+</h1>',
            new_h1,
            content,
            count=1,
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


def check_broken_links(files):
    """Find internal hrefs (relative) that point to non-existent files."""
    broken = []
    for fname in files:
        path = os.path.join(BASE, fname)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        for m in re.finditer(r'href="([^"]+\.html)"', content):
            href = m.group(1)
            if href.startswith("http"):
                continue  # Skip full URLs (canonical, external)
            target = href.split("#")[0].split("?")[0].lstrip("/")
            if target and target not in files:
                broken.append((fname, href))
    return broken


def add_contextual_link_to_thin_pages(files):
    """Add an extra contextual link in thin content sections."""
    # Pages with very short content-section - add a link to related calculator
    pass  # Skip for now - content seems adequate


def main():
    files = discover_pages()
    print("SEO Audit & Fixes")
    print("=" * 40)

    # 1. Fix canonicals
    canon_fixes = fix_canonicals(files)
    print(f"Fixed canonical URLs: {len(canon_fixes)} pages")
    for f in canon_fixes:
        print(f"  - {f}")

    # 2. Vary duplicate metas
    vary_car_loan_meta(files)
    print("Varied car loan meta descriptions")
    vary_business_loan_meta(files)
    print("Varied business loan meta descriptions")
    vary_loan_amount_meta(files)
    print("Varied general loan amount meta descriptions")

    # 3. Vary H1s
    vary_h1_subtle(files)
    print("Varied car loan H1s")

    # 4. Check broken links
    broken = check_broken_links(files)
    if broken:
        print(f"\nBroken links found: {len(broken)}")
        for src, href in broken[:20]:
            print(f"  {src} -> {href}")
    else:
        print("\nNo broken internal links found.")

    print("\nDone.")


if __name__ == "__main__":
    main()
