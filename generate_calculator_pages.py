#!/usr/bin/env python3
"""
Generate SEO-friendly long-tail calculator pages for LoanWise.

Uses the template system:
- config/page_types.py     — Page definitions (amounts, countries, special intent)
- templates/page_template.html — Base HTML structure with {{ placeholders }}
- templates/content_variations.py — Intro, example, FAQ, how-to variations for uniqueness

Run: python generate_calculator_pages.py

After generating new pages, run: python3 apply_internal_links.py
to add breadcrumbs, Related Calculators, and silo links.

HOW TO ADD NEW PAGES:
  See config/page_types.py — add entries to the appropriate list.
  Then run this script. After generation, run apply_internal_links.py and
  update_for_new_pages.py to update sitemap.
"""

import os
from datetime import datetime

from config.page_types import (
    GENERAL_LOAN_AMOUNTS,
    CAR_LOAN_AMOUNTS,
    PERSONAL_LOAN_AMOUNTS,
    MORTGAGE_AMOUNTS,
    COUNTRIES,
    SPECIAL_INTENT_PAGES,
)
from templates.content_variations import (
    pick_variation,
    pick_faqs,
    format_faqs_html,
    INTRO_LOAN_AMOUNT,
    INTRO_CAR_LOAN,
    INTRO_PERSONAL_LOAN,
    INTRO_MORTGAGE,
    INTRO_COUNTRY,
    INTRO_SPECIAL_INTENT,
    EXAMPLE_LOAN_AMOUNT,
    EXAMPLE_CAR_LOAN,
    EXAMPLE_MORTGAGE,
    FAQ_LOAN_AMOUNT,
    FAQ_CAR_LOAN,
    FAQ_PERSONAL_LOAN,
    FAQ_MORTGAGE,
    FAQ_SPECIAL_INTENT,
    FAQ_COUNTRY,
    HOW_TO_LOAN_AMOUNT,
    HOW_TO_CAR_LOAN,
    HOW_TO_PERSONAL_LOAN,
    HOW_TO_MORTGAGE,
    HOW_TO_SPECIAL_INTENT,
    HOW_TO_COUNTRY,
    WHAT_AFFECTS_LOAN_AMOUNT,
    WHAT_AFFECTS_CAR_LOAN,
    WHAT_AFFECTS_PERSONAL_LOAN,
    WHAT_AFFECTS_MORTGAGE,
    WHAT_AFFECTS_SPECIAL_INTENT,
    WHAT_AFFECTS_COUNTRY,
)

BASE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE, "templates", "page_template.html")
CANONICAL_BASE = "https://loanwisecalc.com"
LAST_UPDATED = datetime.now().strftime("%B %Y")

# Shared HTML fragments (keeps current site layout and branding)
NAV_HTML = '''  <header class="site-header">
    <div class="site-header-inner">
      <nav class="site-nav" aria-label="Main navigation">
        <a href="index.html" class="site-logo"><span class="logo-icon" aria-hidden="true">L</span><span class="logo-text">LoanWise</span></a>
        <div class="site-nav-scroll">
        <a href="index.html">Home</a>
        <a href="car-loan-calculator.html">Car Loan</a>
        <a href="auto-loan-calculator.html">Auto Loan</a>
        <a href="personal-loan-calculator.html">Personal Loan</a>
        <a href="business-loan-calculator.html">Business Loan</a>
        <a href="mortgage-calculator.html">Mortgage</a>
        <a href="interest-calculator.html">Interest</a>
        <a href="simple-interest-calculator.html">Simple Interest</a>
        <a href="loan-calculator-usa.html">USA</a>
        <a href="loan-calculator-uk.html">UK</a>
        <a href="loan-calculator-canada.html">Canada</a>
        <a href="loan-calculator-uae.html">UAE</a>
        <a href="loan-calculator-morocco.html">Morocco</a>
        <a href="loan-calculator-australia.html">Australia</a>
        <a href="about.html">About</a>
        <a href="contact.html">Contact</a>
        <a href="privacy-policy.html">Privacy Policy</a>
        <a href="sitemap.html">Sitemap</a>
        <a href="terms.html">Terms</a>
        </div>
      </nav>
    </div>
  </header>'''

CALCULATOR_TEMPLATE = '''    <main class="calculator">
      <div class="input-group">
        <label for="currency">Currency</label>
        <select id="currency" aria-label="Select currency">
          <option value="USD">USD - US Dollar</option>
          <option value="EUR">EUR - Euro</option>
          <option value="GBP">GBP - British Pound</option>
          <option value="MAD">MAD - Moroccan Dirham</option>
          <option value="CAD">CAD - Canadian Dollar</option>
          <option value="AUD">AUD - Australian Dollar</option>
          <option value="CHF">CHF - Swiss Franc</option>
          <option value="JPY">JPY - Japanese Yen</option>
          <option value="AED">AED - UAE Dirham</option>
        </select>
      </div>
      <div class="input-group">
        <label for="loanAmount">Loan Amount</label>
        <input type="number" id="loanAmount" value="{loan_amount}" min="1" step="{loan_step}">
      </div>
      <div class="input-group">
        <label for="interestRate">Interest Rate (%)</label>
        <input type="number" id="interestRate" value="{default_rate}" min="0" max="100" step="0.1" placeholder="e.g. {default_rate}">
      </div>
      <div class="input-group">
        <label for="loanTerm">Loan Term (months)</label>
        <input type="number" id="loanTerm" value="{default_term}" min="1" max="600" step="1" placeholder="e.g. {default_term}">
      </div>
      <button type="button" id="calculateBtn">Calculate your loan now</button>
      <div class="results" id="results">
        <div class="result-card"><p class="result-label">Monthly Payment</p><p class="result-value" id="monthlyPayment">—</p></div>
        <div class="result-card"><p class="result-label">Total Payment</p><p class="result-value" id="totalPayment">—</p></div>
        <div class="result-card"><p class="result-label">Total Interest</p><p class="result-value" id="totalInterest">—</p></div>
      </div>
    </main>'''

FOOTER_HTML = '''  <footer class="site-footer">
    <div class="site-footer-inner">
      <nav class="footer-map" aria-label="Footer links">
        <div class="footer-col"><h3 class="footer-col-title">Calculators</h3>
          <ul class="footer-links">
            <li><a href="index.html">Loan Calculator</a></li>
            <li><a href="car-loan-calculator.html">Car Loan Calculator</a></li>
            <li><a href="auto-loan-calculator.html">Auto Loan Calculator</a></li>
            <li><a href="personal-loan-calculator.html">Personal Loan Calculator</a></li>
            <li><a href="business-loan-calculator.html">Business Loan Calculator</a></li>
            <li><a href="mortgage-calculator.html">Mortgage Calculator</a></li>
            <li><a href="interest-calculator.html">Interest Calculator</a></li>
            <li><a href="simple-interest-calculator.html">Simple Interest Calculator</a></li>
          </ul>
        </div>
        <div class="footer-col"><h3 class="footer-col-title">Countries</h3>
          <ul class="footer-links">
            <li><a href="loan-calculator-usa.html">USA</a></li>
            <li><a href="loan-calculator-uk.html">UK</a></li>
            <li><a href="loan-calculator-canada.html">Canada</a></li>
            <li><a href="loan-calculator-uae.html">UAE</a></li>
            <li><a href="loan-calculator-morocco.html">Morocco</a></li>
            <li><a href="loan-calculator-australia.html">Australia</a></li>
          </ul>
        </div>
        <div class="footer-col"><h3 class="footer-col-title">Company</h3>
          <ul class="footer-links"><li><a href="about.html">About</a></li><li><a href="contact.html">Contact</a></li><li><a href="sitemap.html">Sitemap</a></li></ul>
        </div>
        <div class="footer-col"><h3 class="footer-col-title">Legal</h3>
          <ul class="footer-links"><li><a href="privacy-policy.html">Privacy Policy</a></li><li><a href="terms.html">Terms</a></li></ul>
        </div>
      </nav>
      <div class="footer-bottom"><p class="copyright">© 2025 LoanWise. All rights reserved.</p></div>
    </div>
  </footer>

  <script src="script.js" defer></script>'''


def format_amount(amt):
    """Format amount for display: 2000 -> $2,000; 200000 -> $200,000"""
    if amt >= 1000:
        return f"${amt:,}"
    return f"${amt}"


def monthly_payment(principal, annual_rate_pct, months):
    """Standard amortization: M = P * r(1+r)^n / ((1+r)^n - 1)"""
    if months <= 0 or principal <= 0:
        return 0
    r = annual_rate_pct / 100 / 12
    if r == 0:
        return principal / months
    return principal * (r * (1 + r) ** months) / ((1 + r) ** months - 1)


def build_comparison_table(amt, rate, content_type):
    """Build term vs monthly payment table HTML."""
    if content_type == "mortgage":
        terms = [(120, "10 years"), (180, "15 years"), (240, "20 years"), (360, "30 years")]
    else:
        terms = [(24, "24 months"), (36, "36 months"), (48, "48 months"), (60, "60 months"), (72, "72 months")]

    rows = []
    for m, label in terms:
        pmt = monthly_payment(amt, rate, m)
        total = pmt * m
        interest = total - amt
        rows.append(f"        <tr><td>{label}</td><td>{format_amount(round(pmt))}</td><td>{format_amount(round(interest))}</td></tr>")

    rate_str = str(int(rate)) if rate == int(rate) else str(rate)
    header = '        <tr><th>Term</th><th>Monthly Payment</th><th>Total Interest</th></tr>'
    return '''      <h2>Loan term vs monthly payment</h2>
      <p>How term affects your payment at ''' + format_amount(amt) + ''' and ''' + rate_str + '''% APR:</p>
      <table class="comparison-table" aria-label="Loan term comparison">
''' + header + "\n" + "\n".join(rows) + '''
      </table>
'''


def escape_html(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------------------
# Build page definitions from config
# ---------------------------------------------------------------------------

def build_pages():
    """Build full page dicts from config/page_types."""
    pages = []

    # 1. General loan amount pages
    for i, (amt, rate, term) in enumerate(GENERAL_LOAN_AMOUNTS):
        fmt = format_amount(amt)
        prev_amt = GENERAL_LOAN_AMOUNTS[i - 1][0] if i > 0 else GENERAL_LOAN_AMOUNTS[1][0]
        next_amt = GENERAL_LOAN_AMOUNTS[i + 1][0] if i < len(GENERAL_LOAN_AMOUNTS) - 1 else GENERAL_LOAN_AMOUNTS[i - 2][0] if i >= 2 else GENERAL_LOAN_AMOUNTS[0][0]
        pages.append({
            "filename": f"loan-{amt}-monthly-payment.html",
            "cluster": "general",
            "content_type": "general",
            "amount": amt,
            "default_rate": rate,
            "default_term": term,
            "loan_step": 100,
            "breadcrumb_parent": "index.html",
            "breadcrumb_parent_label": "Loan Calculator",
            "breadcrumb_current": f"Loan for {fmt}",
            "title": f"Loan for {fmt} – Monthly Payment Free & Instant",
            "meta": f"{fmt} loan payment in seconds. Free calculator. See monthly cost and total interest. No signup. Calculate now.",
            "h1": f"Loan {fmt} Monthly Payment — Free, Fast Online",
            "subtitle": f"Pre-filled for {fmt}—adjust rate and term easily",
            "help_links": f'Other amounts: <a href="loan-{prev_amt}-monthly-payment.html">{format_amount(prev_amt)}</a> · <a href="loan-{next_amt}-monthly-payment.html">{format_amount(next_amt)}</a>. Main: <a href="index.html">loan calculator</a> · <a href="personal-loan-calculator.html">personal loan calculator</a>',
            "related": [
                ("index.html", "Loan Calculator"),
                ("personal-loan-calculator.html", "Personal Loan Calculator"),
                ("car-loan-calculator.html", "Car Loan Calculator"),
                ("mortgage-calculator.html", "Mortgage Calculator"),
                ("loan-calculator-usa.html", "Loan Calculator USA"),
            ],
            "index": i,
        })

    # 2. Car loan amount pages
    for i, (amt, rate, term) in enumerate(CAR_LOAN_AMOUNTS):
        fmt = format_amount(amt)
        prev_amt = CAR_LOAN_AMOUNTS[i - 1][0] if i > 0 else CAR_LOAN_AMOUNTS[1][0]
        next_amt = CAR_LOAN_AMOUNTS[i + 1][0] if i < len(CAR_LOAN_AMOUNTS) - 1 else CAR_LOAN_AMOUNTS[i - 2][0] if i >= 2 else CAR_LOAN_AMOUNTS[0][0]
        pages.append({
            "filename": f"car-loan-{amt}-monthly-payment.html",
            "cluster": "car",
            "content_type": "car",
            "amount": amt,
            "default_rate": rate,
            "default_term": term,
            "loan_step": 100,
            "breadcrumb_parent": "car-loan-calculator.html",
            "breadcrumb_parent_label": "Car Loan Calculator",
            "breadcrumb_current": f"Car Loan for {fmt}",
            "title": f"Car Loan for {fmt} – Monthly Payment Free",
            "meta": f"{fmt} car loan payment in seconds. Free calculator. Compare terms. Dealer-ready numbers. Try it now.",
            "h1": f"Car Loan {fmt} Monthly Payment — Free, Fast Estimate",
            "subtitle": f"Pre-filled for {fmt}—change rate or term in seconds",
            "help_links": f'Also try <a href="car-loan-{prev_amt}-monthly-payment.html">{format_amount(prev_amt)}</a> · <a href="car-loan-{next_amt}-monthly-payment.html">{format_amount(next_amt)}</a>. Main: <a href="car-loan-calculator.html">car loan calculator</a> · <a href="auto-loan-calculator.html">auto loan calculator</a>',
            "related": [
                ("car-loan-calculator.html", "Car Loan Calculator"),
                ("car-loan-15000-monthly-payment.html", "Car Loan for $15,000"),
                ("car-loan-20000-monthly-payment.html", "Car Loan for $20,000"),
                ("auto-loan-calculator.html", "Auto Loan Calculator"),
                ("index.html", "Loan Calculator"),
                ("personal-loan-calculator.html", "Personal Loan Calculator"),
            ],
            "index": i,
        })

    # 3. Personal loan amount pages
    for i, (amt, rate, term) in enumerate(PERSONAL_LOAN_AMOUNTS):
        fmt = format_amount(amt)
        prev_amt = PERSONAL_LOAN_AMOUNTS[i - 1][0] if i > 0 else PERSONAL_LOAN_AMOUNTS[1][0]
        next_amt = PERSONAL_LOAN_AMOUNTS[i + 1][0] if i < len(PERSONAL_LOAN_AMOUNTS) - 1 else PERSONAL_LOAN_AMOUNTS[i - 2][0] if i >= 2 else PERSONAL_LOAN_AMOUNTS[0][0]
        pages.append({
            "filename": f"personal-loan-{amt}-payment.html",
            "cluster": "personal",
            "content_type": "personal",
            "amount": amt,
            "default_rate": rate,
            "default_term": term,
            "loan_step": 100,
            "breadcrumb_parent": "personal-loan-calculator.html",
            "breadcrumb_parent_label": "Personal Loan Calculator",
            "breadcrumb_current": f"Personal Loan for {fmt}",
            "title": f"Personal Loan for {fmt} – Free Payment Tool",
            "meta": f"{fmt} personal loan payment in seconds. Free calculator. See cost before you apply. No signup. Try now.",
            "h1": f"Personal Loan {fmt} Payment — Free &amp; Fast Estimate",
            "subtitle": f"Pre-filled for {fmt}—adjust rate and term easily",
            "help_links": f'Other amounts: <a href="personal-loan-{prev_amt}-payment.html">{format_amount(prev_amt)}</a> · <a href="personal-loan-{next_amt}-payment.html">{format_amount(next_amt)}</a>. Main: <a href="personal-loan-calculator.html">personal loan calculator</a> · <a href="index.html">loan calculator</a>',
            "related": [
                ("personal-loan-calculator.html", "Personal Loan Calculator"),
                ("index.html", "Loan Calculator"),
                ("car-loan-calculator.html", "Car Loan Calculator"),
                ("mortgage-calculator.html", "Mortgage Calculator"),
                ("loan-calculator-usa.html", "Loan Calculator USA"),
            ],
            "index": i,
        })

    # 4. Mortgage amount pages
    for i, (amt_k, rate, term) in enumerate(MORTGAGE_AMOUNTS):
        amt = amt_k * 1000
        fmt = format_amount(amt)
        pages.append({
            "filename": f"mortgage-{amt_k}k-payment.html",
            "cluster": "mortgage",
            "content_type": "mortgage",
            "amount": amt,
            "default_rate": rate,
            "default_term": term,
            "loan_step": 1000,
            "breadcrumb_parent": "mortgage-calculator.html",
            "breadcrumb_parent_label": "Mortgage Calculator",
            "breadcrumb_current": f"Mortgage for {fmt}",
            "title": f"Mortgage for {fmt} – Free Payment Calculator",
            "meta": f"{fmt} mortgage payment instantly. Free tool. Adjust rate and term. See P&I. No signup. Calculate now.",
            "h1": f"Mortgage {fmt} Payment — Free, Fast P&amp;I Estimate",
            "subtitle": "30-year term pre-filled—adjust rate to match your quote",
            "help_links": '<a href="mortgage-150k-payment.html">$150,000</a> · <a href="mortgage-200k-payment.html">$200,000</a> · <a href="mortgage-300k-payment.html">$300,000</a>. Main: <a href="mortgage-calculator.html">mortgage calculator</a> · <a href="mortgage-30-year-calculator.html">30-year calculator</a>',
            "related": [
                ("mortgage-calculator.html", "Mortgage Calculator"),
                ("mortgage-30-year-calculator.html", "30-Year Mortgage"),
                ("car-loan-calculator.html", "Car Loan Calculator"),
                ("personal-loan-calculator.html", "Personal Loan Calculator"),
                ("index.html", "Loan Calculator"),
            ],
            "index": i,
        })

    # 5. Special intent pages (from config)
    for i, p in enumerate(SPECIAL_INTENT_PAGES):
        pages.append({
            **p,
            "content_type": "special_intent",
            "index": i,
        })

    # 6. Country pages
    for i, c in enumerate(COUNTRIES):
        pages.append({
            "filename": c["filename"],
            "cluster": "country",
            "content_type": "country",
            "amount": c.get("amount", 10000),
            "default_rate": c.get("default_rate", 9),
            "default_term": c.get("default_term", 48),
            "loan_step": c.get("loan_step", 1000),
            "breadcrumb_parent": "index.html",
            "breadcrumb_parent_label": "Home",
            "breadcrumb_current": c["title"],
            "title": f"{c['title']} – Free Payment Instantly",
            "meta": f"{c['country']} loan payment in seconds. Free calculator. Personal, auto, or mortgage. No signup. Calculate now.",
            "h1": f"{c['title']} — Free, Fast Online",
            "subtitle": "Use calculator for estimates—select your currency",
            "help_links": '<a href="loan-calculator-usa.html">USA</a> · <a href="loan-calculator-uk.html">UK</a> · <a href="loan-calculator-australia.html">Australia</a> · <a href="index.html">loan calculator</a>',
            "related": [
                ("index.html", "Loan Calculator"),
                ("loan-calculator-usa.html", "Loan Calculator USA"),
                ("loan-calculator-uk.html", "Loan Calculator UK"),
                ("car-loan-calculator.html", "Car Loan Calculator"),
                ("personal-loan-calculator.html", "Personal Loan Calculator"),
            ],
            "country": c["country"],
            "index": i,
        })

    return pages


# ---------------------------------------------------------------------------
# Content section builder using variations
# ---------------------------------------------------------------------------

def build_content_section(p):
    """Build unique content section using content_variations pools."""
    amt = p.get("amount", 10000)
    fmt = format_amount(amt)
    rate = p.get("default_rate", 9)
    term = p.get("default_term", 48)
    content_type = p.get("content_type", "general")
    idx = p.get("index", 0)
    country = p.get("country", "your country")

    kw = {"amount": fmt, "rate": rate, "term": term, "country": country}
    approx_monthly = f"${round(amt / 1000 * 6.32):,}" if amt >= 1000 else f"${amt}"
    kw["approx_monthly"] = approx_monthly

    parts = []

    # How to use
    if content_type == "general":
        how_to = pick_variation(HOW_TO_LOAN_AMOUNT, idx).format(**kw)
    elif content_type == "car":
        how_to = pick_variation(HOW_TO_CAR_LOAN, idx).format(**kw)
    elif content_type == "personal":
        how_to = pick_variation(HOW_TO_PERSONAL_LOAN, idx).format(**kw)
    elif content_type == "mortgage":
        how_to = pick_variation(HOW_TO_MORTGAGE, idx).format(**kw)
    elif content_type == "country":
        how_to = pick_variation(HOW_TO_COUNTRY, idx).format(**kw)
    else:  # special_intent
        how_to = pick_variation(HOW_TO_SPECIAL_INTENT, idx)

    parts.append("      <h2>How to use this calculator</h2>\n      " + how_to)

    # Example or "What affects" section
    if content_type == "general":
        example = pick_variation(EXAMPLE_LOAN_AMOUNT, idx).format(**kw)
        parts.append("\n\n      <h2>Real-world example</h2>\n      <p>" + example + "</p>")
        parts.append("\n\n      <h2>What affects your " + fmt + " loan payment</h2>\n      " + WHAT_AFFECTS_LOAN_AMOUNT)
    elif content_type == "car":
        parts.append("\n\n      <h2>What affects a " + fmt + " car loan monthly payment?</h2>\n      " + WHAT_AFFECTS_CAR_LOAN.format(**kw))
    elif content_type == "personal":
        parts.append("\n\n      <h2>What affects your " + fmt + " personal loan payment</h2>\n      " + WHAT_AFFECTS_PERSONAL_LOAN)
    elif content_type == "mortgage":
        example = pick_variation(EXAMPLE_MORTGAGE, idx).format(**kw)
        parts.append("\n\n      <h2>What is the monthly payment on a " + fmt + " mortgage?</h2>\n      <p>" + example + "</p>\n      " + WHAT_AFFECTS_MORTGAGE)
    elif content_type == "country":
        parts.append("\n\n      <h2>Loans in " + country + "</h2>\n      " + WHAT_AFFECTS_COUNTRY)
    else:  # special_intent
        parts.append("\n\n      <h2>What affects your payment</h2>\n      " + WHAT_AFFECTS_SPECIAL_INTENT)

    # Comparison table (term vs monthly payment)
    if content_type in ("general", "car", "personal", "mortgage"):
        parts.append("\n\n      " + build_comparison_table(amt, rate, content_type))

    # FAQ (4-5 questions for better SEO)
    if content_type == "general":
        faqs = pick_faqs(FAQ_LOAN_AMOUNT, 5, idx, **kw)
    elif content_type == "car":
        faqs = pick_faqs(FAQ_CAR_LOAN, 5, idx, **kw)
    elif content_type == "personal":
        faqs = pick_faqs(FAQ_PERSONAL_LOAN, 5, idx, **kw)
    elif content_type == "mortgage":
        faqs = pick_faqs(FAQ_MORTGAGE, 5, idx, **kw)
    elif content_type == "country":
        faqs = pick_faqs(FAQ_COUNTRY, 2, idx, **kw)
    else:
        faqs = pick_faqs(FAQ_SPECIAL_INTENT, 2, idx, **kw)

    parts.append("\n\n      <h2>Frequently asked questions</h2>\n      " + format_faqs_html(faqs))

    return "".join(parts)


def build_intro(p):
    """Build intro paragraph using variation pool."""
    if p.get("intro_override"):
        return p["intro_override"]
    content_type = p.get("content_type", "general")
    idx = p.get("index", 0)
    fmt = format_amount(p.get("amount", 10000))
    country = p.get("country", "your country")

    if content_type == "general":
        return pick_variation(INTRO_LOAN_AMOUNT, idx).format(amount=fmt)
    elif content_type == "car":
        return pick_variation(INTRO_CAR_LOAN, idx).format(amount=fmt)
    elif content_type == "personal":
        return pick_variation(INTRO_PERSONAL_LOAN, idx).format(amount=fmt)
    elif content_type == "mortgage":
        return pick_variation(INTRO_MORTGAGE, idx).format(amount=fmt)
    elif content_type == "country":
        return pick_variation(INTRO_COUNTRY, idx).format(country=country)
    else:
        return pick_variation(INTRO_SPECIAL_INTENT, idx)


def build_related_html(related):
    items = "\n        ".join(f'<li><a href="{href}">{label}</a></li>' for href, label in related)
    return f'''    <section class="related-calculators" aria-labelledby="related-calculators-heading">
      <h2 id="related-calculators-heading">Related Calculators</h2>
      <ul class="related-calculators-list">
        {items}
      </ul>
    </section>'''


# ---------------------------------------------------------------------------
# Template rendering
# ---------------------------------------------------------------------------

def render_template(context):
    """Replace {{ key }} placeholders in template with context values."""
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        html = f.read()
    for key, value in context.items():
        placeholder = "{{ " + key + " }}"
        html = html.replace(placeholder, str(value))
    return html


def generate_page(p):
    """Generate full HTML for a page using the template system."""
    calculator_html = CALCULATOR_TEMPLATE.format(
        loan_amount=p["amount"],
        default_rate=p["default_rate"],
        default_term=p["default_term"],
        loan_step=p["loan_step"],
    )

    intro = build_intro(p)
    content_section = build_content_section(p)
    related_html = build_related_html(p["related"])

    breadcrumb = f'''    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="index.html">Home</a>
      <span class="breadcrumb-sep" aria-hidden="true">›</span>
      <a href="{p["breadcrumb_parent"]}">{p["breadcrumb_parent_label"]}</a>
      <span class="breadcrumb-sep" aria-hidden="true">›</span>
      <span aria-current="page">{p["breadcrumb_current"]}</span>
    </nav>'''

    disclaimer = "Estimate only." if p["cluster"] != "mortgage" else "Principal &amp; interest only—no taxes, insurance, or PMI."
    disclaimer += ' <a href="index.html">Home</a> · <a href="car-loan-calculator.html">Car loan</a>'

    context = {
        "title": p["title"],
        "meta_description": p["meta"],
        "canonical_url": f"{CANONICAL_BASE}/{p['filename']}",
        "h1": p["h1"],
        "subtitle": p["subtitle"],
        "intro": intro,
        "nav_html": NAV_HTML,
        "breadcrumb_html": breadcrumb,
        "calculator_html": calculator_html,
        "help_links": p.get("help_links", '<a href="index.html">loan calculator</a> · <a href="car-loan-calculator.html">car loan</a> · <a href="personal-loan-calculator.html">personal loan</a>'),
        "disclaimer": disclaimer,
        "content_section": content_section,
        "related_calculators_html": related_html,
        "footer_html": FOOTER_HTML,
        "last_updated": LAST_UPDATED,
    }

    return render_template(context)


def main():
    pages = build_pages()
    existing = set(f for f in os.listdir(BASE) if f.endswith(".html"))
    created = 0
    skipped = 0

    for p in pages:
        fname = p["filename"]
        if fname in existing:
            print(f"SKIP (exists): {fname}")
            skipped += 1
            continue

        html = generate_page(p)
        path = os.path.join(BASE, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Created: {fname}")
        created += 1

    print(f"\nDone. Created {created} pages, skipped {skipped} existing.")


if __name__ == "__main__":
    main()
