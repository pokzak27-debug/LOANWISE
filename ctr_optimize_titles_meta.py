#!/usr/bin/env python3
"""
CTR-optimized title and meta description rewrite.

Rules:
- Titles: main keyword, benefit, urgency (Instant/Fast/Free), max 60 chars
- Meta: keyword, what user gets, free/instant/easy, max 155 chars, CTA

Run: python3 ctr_optimize_titles_meta.py
"""

import os
import re
import html

BASE = os.path.dirname(os.path.abspath(__file__))

# CTR-optimized title and meta by page type
# Titles max 60 chars; meta max 155 chars
TITLES_META = {
    "index.html": (
        "Loan Calculator – Monthly Payment Free &amp; Instant",
        "Calculate monthly payment, total interest, and loan cost in seconds. Free, easy calculator. No signup—try now.",
    ),
    "car-loan-calculator.html": (
        "Car Loan Calculator – Payment Free &amp; Instant",
        "Get your car loan monthly payment in seconds. Free, easy tool. Compare rates &amp; terms. No signup—calculate now.",
    ),
    "auto-loan-calculator.html": (
        "Auto Loan Calculator – Monthly Payment Instantly",
        "Calculate auto loan payment and total interest in seconds. Free, instant. Compare 48 vs 60 months—try now.",
    ),
    "personal-loan-calculator.html": (
        "Personal Loan Calculator – Payment Free &amp; Fast",
        "See your personal loan monthly payment in seconds. Free, easy. Total cost before you apply. No signup—try now.",
    ),
    "business-loan-calculator.html": (
        "Business Loan Calculator – Payment Free &amp; Fast",
        "Calculate business loan monthly payment and total interest. Free, instant. Compare terms easily. No signup.",
    ),
    "mortgage-calculator.html": (
        "Mortgage Calculator – Monthly Payment Free &amp; Fast",
        "Get principal &amp; interest in seconds. Free mortgage calculator. Compare rates. No signup—calculate now.",
    ),
    "interest-calculator.html": (
        "Interest Calculator – Free &amp; Instant",
        "Calculate interest on any loan. Free, easy tool. See total cost. No signup—try now.",
    ),
    "simple-interest-calculator.html": (
        "Simple Interest Calculator – I=P×R×T Free",
        "Calculate simple interest with I=P×R×T. Free, instant. Compare to compound. No signup—try now.",
    ),
    "loan-calculator-with-down-payment.html": (
        "Loan Calculator with Down Payment – Free &amp; Easy",
        "Enter price and down payment—see your real monthly payment instantly. Free, easy. No signup—calculate now.",
    ),
    "loan-calculator-with-extra-payments.html": (
        "Extra Payment Calculator – See Savings Instantly",
        "See how extra payments cut interest and shorten your loan. Free, instant. No signup—try it now.",
    ),
    "loan-calculator-with-interest-breakdown.html": (
        "Loan Interest Breakdown – Free Calculator",
        "Year-by-year principal vs interest. Free, instant. See where your money goes. No signup—try now.",
    ),
    "simple-loan-payment-example.html": (
        "Simple Loan Example – $10k Walkthrough Free",
        "Learn loan math with a $10k example. Free calculator included. Understand payments in minutes. Start here.",
    ),
    "how-to-calculate-loan-monthly-payment.html": (
        "How to Calculate Loan Payment – Free Guide",
        "Step-by-step loan payment formula. Free calculator. Understand the math. No signup—try now.",
    ),
    "used-car-loan-calculator.html": (
        "Used Car Loan Calculator – Payment Free &amp; Fast",
        "Calculate used car loan payment. Higher rates typical. Free, instant. Compare before you buy. Try now.",
    ),
    "car-loan-with-trade-in-calculator.html": (
        "Car Loan with Trade-In Calculator – Free",
        "Factor trade-in value into your car payment. Free, easy. See real monthly cost. No signup—try now.",
    ),
    "how-much-car-loan-can-i-afford.html": (
        "How Much Car Loan Can I Afford – Free Calculator",
        "See what you can afford. Free, instant. Monthly payment based on your budget. No signup—try now.",
    ),
    "car-loan-monthly-payment-calculator.html": (
        "Car Loan Monthly Payment Calculator – Free",
        "Get car loan payment in seconds. Free, easy. Compare terms. No signup—calculate now.",
    ),
    "auto-loan-refinance-calculator.html": (
        "Auto Loan Refinance Calculator – See If You Save",
        "Should you refinance? Compare current vs lower rate. Free, instant. See savings in seconds. Try now.",
    ),
    "debt-consolidation-loan-calculator.html": (
        "Debt Consolidation Calculator – Free &amp; Instant",
        "Compare single payment vs multiple debts. Free, easy. See if it saves. No signup—calculate now.",
    ),
    "home-improvement-loan-calculator.html": (
        "Home Improvement Loan Calculator – Free",
        "Calculate renovation loan payment. Free, instant. Compare terms. No signup—try now.",
    ),
    "bad-credit-loan-calculator.html": (
        "Bad Credit Loan Calculator – Estimate Payment",
        "Realistic payments for lower credit. Free, instant. See monthly cost before you apply. Try now.",
    ),
    "mortgage-30-year-calculator.html": (
        "30-Year Mortgage Calculator – Payment Free &amp; Fast",
        "30-year payment in seconds. Free calculator. See P&amp;I and total interest. No signup—try now.",
    ),
    "mortgage-15-year-calculator.html": (
        "15-Year Mortgage Calculator – Save Interest Fast",
        "15-year payment instantly. Pay off faster, save interest. Free. Compare with 30-year—try now.",
    ),
    "about.html": (
        "About LoanWise – Free Loan Calculators",
        "Free loan calculators for everyone. Simple, fast, no signup. Learn more about LoanWise.",
    ),
    "contact.html": (
        "Contact LoanWise – Free Calculators",
        "Get in touch. Questions about our free loan calculators? Contact us.",
    ),
    "sitemap.html": (
        "Sitemap – All Loan Calculators | LoanWise",
        "Complete sitemap of free loan calculators: car, personal, mortgage, business. Find any tool—browse now.",
    ),
    "terms.html": (
        "Terms of Use – Free Calculators | LoanWise",
        "LoanWise terms: free calculators for estimates only. Simple rules. Verify with your lender. Read here.",
    ),
    "privacy-policy.html": (
        "Privacy Policy – LoanWise Free Calculators",
        "How we handle data: plain English. No account needed. Simple and transparent. Read here.",
    ),
}

# Meta variations for general loans (avoid duplicates)
META_GENERAL = [
    "Monthly payment, total interest, and cost. Free, instant. Compare rates & terms. Try now.",
    "See your payment and total cost in seconds. Free, easy. No signup needed. Calculate now.",
    "Get payment estimate instantly. Free tool. Compare terms. No signup—try now.",
]


def format_amount(amt):
    if amt >= 1000:
        return f"${amt:,}"
    return f"${amt}"


def get_title_meta(fname, amount=None, amount_k=None, country=None):
    """Return (title, meta) for a page. Ensure uniqueness."""
    if fname in TITLES_META:
        return TITLES_META[fname]

    # General loan: loan-N-monthly-payment.html
    m = re.match(r"loan-(\d+)-monthly-payment\.html", fname)
    if m:
        amt = int(m.group(1))
        fmt = format_amount(amt)
        title = f"Loan for {fmt} – Monthly Payment Instantly"
        if len(title) > 60:
            title = f"Loan {fmt} – Payment Free &amp; Fast"
        meta_idx = amt % len(META_GENERAL)
        meta = f"{fmt} loan: {META_GENERAL[meta_idx]}"
        return (title, meta[:155])

    # Car loan: car-loan-N-monthly-payment.html
    m = re.match(r"car-loan-(\d+)-monthly-payment\.html", fname)
    if m:
        amt = int(m.group(1))
        fmt = format_amount(amt)
        title = f"Car Loan {fmt} – Payment Free &amp; Instant"
        if len(title) > 60:
            title = f"Car Loan {fmt} – Payment Instantly"
        metas = [
            f"{fmt} car loan: monthly payment and total interest. Free, easy. Compare terms—try now.",
            f"Get {fmt} auto loan payment in seconds. Free, instant. See total cost. No signup.",
            f"{fmt} car payment calculator. Free, easy. Compare 48 vs 60 months. Try now.",
        ]
        meta = metas[amt % len(metas)]
        return (title, meta[:155])

    # Personal loan: personal-loan-N-payment.html
    m = re.match(r"personal-loan-(\d+)-payment\.html", fname)
    if m:
        amt = int(m.group(1))
        fmt = format_amount(amt)
        title = f"Personal Loan {fmt} – Payment Free &amp; Fast"
        if len(title) > 60:
            title = f"Personal Loan {fmt} – Payment Instantly"
        metas = [
            f"{fmt} personal loan: see monthly payment before you apply. Free, instant. No signup—try now.",
            f"Calculate {fmt} personal loan payment. Free, easy. Total cost in seconds. Try now.",
            f"{fmt} personal loan monthly cost. Free calculator. Compare terms. No signup—calculate now.",
        ]
        meta = metas[amt % len(metas)]
        return (title, meta[:155])

    # Business loan: business-loan-N-payment.html
    m = re.match(r"business-loan-(\d+)-payment\.html", fname)
    if m:
        amt = int(m.group(1))
        fmt = format_amount(amt)
        title = f"Business Loan {fmt} – Payment Free &amp; Fast"
        meta = f"{fmt} business loan payment. Free, instant. Compare terms. No signup—calculate now."
        return (title[:60], meta[:155])

    # Mortgage: mortgage-Nk-payment.html
    m = re.match(r"mortgage-(\d+)k-payment\.html", fname)
    if m:
        k = m.group(1)
        ki = int(k)
        if ki >= 100:
            fmt = f"${ki:,}k"
        else:
            fmt = f"${k}k"
        title = f"Mortgage {fmt} – Payment Free &amp; Instant"
        metas = [
            f"{fmt} mortgage: principal and interest in seconds. Free, easy. Compare rates—try now.",
            f"Calculate {fmt} home loan payment. Free, instant. See P&I. No signup.",
            f"{fmt} mortgage payment calculator. Free tool. Adjust rate and term. Try now.",
        ]
        meta = metas[ki % len(metas)]
        return (title[:60], meta[:155])

    # Country: loan-calculator-{slug}.html
    m = re.match(r"loan-calculator-([a-z-]+)\.html", fname)
    if m:
        slug = m.group(1)
        label = slug.replace("-", " ").title()
        if slug == "usa":
            label = "USA"
        elif slug == "uk":
            label = "UK"
        elif slug == "uae":
            label = "UAE"
        title = f"{label} Loan Calculator – Payment Free &amp; Fast"
        meta = f"{label} loan payment in seconds. Free, instant. Personal, auto, mortgage. No signup—try now."
        return (title[:60], meta[:155])

    # Auto term: auto-loan-calculator-N-months.html
    m = re.match(r"auto-loan-calculator-(\d+)-months\.html", fname)
    if m:
        months = m.group(1)
        title = f"{months}-Month Auto Loan – Payment Free &amp; Fast"
        meta = f"{months}-month car loan payment. Free, instant. Compare terms. No signup—try now."
        return (title[:60], meta[:155])

    return None


def update_file(path, fname):
    """Update title and meta in HTML file."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    result = get_title_meta(fname)
    if not result:
        return False

    title, meta = result

    # Escape for HTML attributes (& and " must be escaped)
    title_attr = html.escape(title, quote=True).replace("&#x27;", "'")
    meta_attr = html.escape(meta, quote=True).replace("&#x27;", "'")

    # Replace title
    content = re.sub(
        r"<title>.*?</title>",
        f"<title>{title}</title>",
        content,
        count=1,
    )

    # Replace meta description
    content = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{meta_attr}">',
        content,
        count=1,
    )

    # Replace og:title and og:description (use same escaped values)
    content = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{title_attr}">',
        content,
        count=1,
    )
    content = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{meta_attr}">',
        content,
        count=1,
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return True


def main():
    files = sorted(
        f for f in os.listdir(BASE)
        if f.endswith(".html") and os.path.isfile(os.path.join(BASE, f))
        and not f.startswith(".") and "templates" not in f
    )
    # Exclude templates subdir (files are in root)
    files = [f for f in files if not f.startswith("template")]

    updated = 0
    for fname in files:
        path = os.path.join(BASE, fname)
        if update_file(path, fname):
            print(f"Updated: {fname}")
            updated += 1
        else:
            print(f"Skipped (no rule): {fname}")

    print(f"\nDone. Updated {updated} pages.")


if __name__ == "__main__":
    main()
