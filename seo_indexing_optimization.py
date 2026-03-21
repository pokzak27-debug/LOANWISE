#!/usr/bin/env python3
"""
SEO indexing optimization:
- Create HTML sitemap linking all pages
- Add sitemap link to nav
- Add lastmod to sitemap.xml
- Add last-updated to pages missing it
- Add preload for critical CSS
- Fix robots.txt domain consistency
"""
import os
import re
from datetime import datetime

BASE = "/Users/mac/Desktop/LoanWise"
SITEMAP_DATE = datetime.now().strftime("%Y-%m-%d")

# All HTML files grouped by section
PAGES_BY_SECTION = {
    "Main": ["index.html"],
    "Calculators": [
        "car-loan-calculator.html", "auto-loan-calculator.html", "personal-loan-calculator.html",
        "business-loan-calculator.html", "mortgage-calculator.html", "interest-calculator.html",
        "simple-interest-calculator.html",
    ],
    "Loan Amounts": [
        "loan-2000-monthly-payment.html", "loan-3000-monthly-payment.html", "loan-4000-monthly-payment.html",
        "loan-5000-monthly-payment.html", "loan-6000-monthly-payment.html", "loan-7000-monthly-payment.html",
        "loan-8000-monthly-payment.html", "loan-9000-monthly-payment.html", "loan-10000-monthly-payment.html",
        "loan-11000-monthly-payment.html", "loan-12000-monthly-payment.html", "loan-14000-monthly-payment.html",
        "loan-15000-monthly-payment.html", "loan-16000-monthly-payment.html", "loan-18000-monthly-payment.html",
        "loan-20000-monthly-payment.html", "loan-25000-monthly-payment.html", "loan-30000-monthly-payment.html",
        "loan-35000-monthly-payment.html", "loan-40000-monthly-payment.html", "loan-45000-monthly-payment.html",
        "loan-50000-monthly-payment.html",
    ],
    "Car Loan Tools": [
        "car-loan-15000-monthly-payment.html", "car-loan-20000-monthly-payment.html", "car-loan-25000-monthly-payment.html",
        "car-loan-30000-monthly-payment.html", "car-loan-40000-monthly-payment.html", "car-loan-50000-monthly-payment.html",
        "car-loan-60000-monthly-payment.html", "how-much-car-loan-can-i-afford.html", "car-loan-monthly-payment-calculator.html",
        "auto-loan-calculator-48-months.html", "auto-loan-calculator-60-months.html", "car-loan-with-trade-in-calculator.html",
    ],
    "Personal Loans": [
        "personal-loan-2000-payment.html", "personal-loan-3000-payment.html", "personal-loan-4000-payment.html",
        "personal-loan-5000-payment.html", "personal-loan-6000-payment.html", "personal-loan-7000-payment.html",
        "personal-loan-8000-payment.html", "personal-loan-9000-payment.html", "personal-loan-10000-payment.html",
        "personal-loan-11000-payment.html", "personal-loan-12000-payment.html", "personal-loan-14000-payment.html",
        "personal-loan-15000-payment.html", "personal-loan-18000-payment.html", "personal-loan-20000-payment.html",
        "personal-loan-25000-payment.html", "debt-consolidation-loan-calculator.html", "home-improvement-loan-calculator.html",
    ],
    "Mortgage Tools": [
        "mortgage-15-year-calculator.html", "mortgage-30-year-calculator.html", "mortgage-100k-payment.html",
        "mortgage-125k-payment.html", "mortgage-150k-payment.html", "mortgage-175k-payment.html",
        "mortgage-200k-payment.html", "mortgage-225k-payment.html", "mortgage-250k-payment.html",
        "mortgage-275k-payment.html", "mortgage-300k-payment.html", "mortgage-350k-payment.html",
        "mortgage-400k-payment.html", "mortgage-450k-payment.html", "mortgage-500k-payment.html",
    ],
    "Business Loans": [
        "business-loan-10000-payment.html", "business-loan-20000-payment.html", "business-loan-50000-payment.html",
    ],
    "Loan Tools": [
        "loan-calculator-with-down-payment.html", "loan-calculator-with-extra-payments.html",
        "loan-calculator-with-interest-breakdown.html", "simple-loan-payment-example.html",
        "how-to-calculate-loan-monthly-payment.html",
    ],
    "By Country": [
        "loan-calculator-usa.html", "loan-calculator-uk.html", "loan-calculator-canada.html",
        "loan-calculator-australia.html", "loan-calculator-uae.html", "loan-calculator-morocco.html",
        "loan-calculator-india.html", "loan-calculator-singapore.html", "loan-calculator-new-zealand.html",
        "loan-calculator-ireland.html",
    ],
    "Company": ["about.html", "contact.html"],
    "Legal": ["privacy-policy.html", "terms.html"],
}

LABELS = {
    "index.html": "Loan Calculator",
    "car-loan-calculator.html": "Car Loan Calculator",
    "auto-loan-calculator.html": "Auto Loan Calculator",
    "personal-loan-calculator.html": "Personal Loan Calculator",
    "business-loan-calculator.html": "Business Loan Calculator",
    "mortgage-calculator.html": "Mortgage Calculator",
    "interest-calculator.html": "Interest Calculator",
    "simple-interest-calculator.html": "Simple Interest Calculator",
    "loan-2000-monthly-payment.html": "Loan for $2,000",
    "loan-3000-monthly-payment.html": "Loan for $3,000",
    "loan-5000-monthly-payment.html": "Loan for $5,000",
    "loan-7000-monthly-payment.html": "Loan for $7,000",
    "loan-8000-monthly-payment.html": "Loan for $8,000",
    "loan-10000-monthly-payment.html": "Loan for $10,000",
    "loan-12000-monthly-payment.html": "Loan for $12,000",
    "loan-15000-monthly-payment.html": "Loan for $15,000",
    "loan-20000-monthly-payment.html": "Loan for $20,000",
    "loan-4000-monthly-payment.html": "Loan for $4,000",
    "loan-6000-monthly-payment.html": "Loan for $6,000",
    "loan-9000-monthly-payment.html": "Loan for $9,000",
    "loan-11000-monthly-payment.html": "Loan for $11,000",
    "loan-14000-monthly-payment.html": "Loan for $14,000",
    "loan-16000-monthly-payment.html": "Loan for $16,000",
    "loan-18000-monthly-payment.html": "Loan for $18,000",
    "loan-25000-monthly-payment.html": "Loan for $25,000",
    "loan-30000-monthly-payment.html": "Loan for $30,000",
    "loan-35000-monthly-payment.html": "Loan for $35,000",
    "loan-40000-monthly-payment.html": "Loan for $40,000",
    "loan-45000-monthly-payment.html": "Loan for $45,000",
    "loan-50000-monthly-payment.html": "Loan for $50,000",
    "car-loan-10000-monthly-payment.html": "Car Loan for $10,000",
    "car-loan-12000-monthly-payment.html": "Car Loan for $12,000",
    "car-loan-14000-monthly-payment.html": "Car Loan for $14,000",
    "car-loan-15000-monthly-payment.html": "Car Loan for $15,000",
    "car-loan-18000-monthly-payment.html": "Car Loan for $18,000",
    "car-loan-20000-monthly-payment.html": "Car Loan for $20,000",
    "car-loan-25000-monthly-payment.html": "Car Loan for $25,000",
    "car-loan-30000-monthly-payment.html": "Car Loan for $30,000",
    "car-loan-40000-monthly-payment.html": "Car Loan for $40,000",
    "car-loan-50000-monthly-payment.html": "Car Loan for $50,000",
    "car-loan-22000-monthly-payment.html": "Car Loan for $22,000",
    "car-loan-28000-monthly-payment.html": "Car Loan for $28,000",
    "car-loan-35000-monthly-payment.html": "Car Loan for $35,000",
    "car-loan-45000-monthly-payment.html": "Car Loan for $45,000",
    "car-loan-55000-monthly-payment.html": "Car Loan for $55,000",
    "car-loan-60000-monthly-payment.html": "Car Loan for $60,000",
    "car-loan-70000-monthly-payment.html": "Car Loan for $70,000",
    "car-loan-80000-monthly-payment.html": "Car Loan for $80,000",
    "how-much-car-loan-can-i-afford.html": "How Much Car Loan Can I Afford?",
    "car-loan-monthly-payment-calculator.html": "Car Loan Monthly Payment",
    "auto-loan-calculator-36-months.html": "36 Month Auto Loan",
    "auto-loan-calculator-48-months.html": "48 Month Auto Loan",
    "auto-loan-calculator-60-months.html": "60 Month Auto Loan",
    "auto-loan-calculator-72-months.html": "72 Month Auto Loan",
    "used-car-loan-calculator.html": "Used Car Loan Calculator",
    "car-loan-with-trade-in-calculator.html": "Car Loan with Trade-In",
    "personal-loan-3000-payment.html": "Personal Loan for $3,000",
    "personal-loan-5000-payment.html": "Personal Loan for $5,000",
    "personal-loan-8000-payment.html": "Personal Loan for $8,000",
    "personal-loan-10000-payment.html": "Personal Loan for $10,000",
    "personal-loan-15000-payment.html": "Personal Loan for $15,000",
    "personal-loan-2000-payment.html": "Personal Loan for $2,000",
    "personal-loan-4000-payment.html": "Personal Loan for $4,000",
    "personal-loan-6000-payment.html": "Personal Loan for $6,000",
    "personal-loan-7000-payment.html": "Personal Loan for $7,000",
    "personal-loan-9000-payment.html": "Personal Loan for $9,000",
    "personal-loan-11000-payment.html": "Personal Loan for $11,000",
    "personal-loan-12000-payment.html": "Personal Loan for $12,000",
    "personal-loan-14000-payment.html": "Personal Loan for $14,000",
    "personal-loan-18000-payment.html": "Personal Loan for $18,000",
    "personal-loan-20000-payment.html": "Personal Loan for $20,000",
    "personal-loan-25000-payment.html": "Personal Loan for $25,000",
    "debt-consolidation-loan-calculator.html": "Debt Consolidation Loan",
    "home-improvement-loan-calculator.html": "Home Improvement Loan",
    "mortgage-15-year-calculator.html": "15-Year Mortgage",
    "mortgage-30-year-calculator.html": "30-Year Mortgage",
    "mortgage-150k-payment.html": "Mortgage for $150k",
    "mortgage-200k-payment.html": "Mortgage for $200k",
    "mortgage-250k-payment.html": "Mortgage for $250k",
    "mortgage-300k-payment.html": "Mortgage for $300k",
    "mortgage-100k-payment.html": "Mortgage for $100k",
    "mortgage-125k-payment.html": "Mortgage for $125k",
    "mortgage-175k-payment.html": "Mortgage for $175k",
    "mortgage-225k-payment.html": "Mortgage for $225k",
    "mortgage-275k-payment.html": "Mortgage for $275k",
    "mortgage-350k-payment.html": "Mortgage for $350k",
    "mortgage-400k-payment.html": "Mortgage for $400k",
    "mortgage-450k-payment.html": "Mortgage for $450k",
    "mortgage-500k-payment.html": "Mortgage for $500k",
    "business-loan-10000-payment.html": "Business Loan for $10,000",
    "business-loan-20000-payment.html": "Business Loan for $20,000",
    "business-loan-50000-payment.html": "Business Loan for $50,000",
    "loan-calculator-with-down-payment.html": "Loan with Down Payment",
    "loan-calculator-with-extra-payments.html": "Loan with Extra Payments",
    "loan-calculator-with-interest-breakdown.html": "Loan with Interest Breakdown",
    "simple-loan-payment-example.html": "Simple Loan Example",
    "how-to-calculate-loan-monthly-payment.html": "How to Calculate Loan Payment",
    "loan-calculator-usa.html": "USA",
    "loan-calculator-uk.html": "UK",
    "loan-calculator-canada.html": "Canada",
    "loan-calculator-australia.html": "Australia",
    "loan-calculator-uae.html": "UAE",
    "loan-calculator-morocco.html": "Morocco",
    "loan-calculator-india.html": "India",
    "loan-calculator-singapore.html": "Singapore",
    "loan-calculator-new-zealand.html": "New Zealand",
    "loan-calculator-ireland.html": "Ireland",
    "about.html": "About",
    "contact.html": "Contact",
    "privacy-policy.html": "Privacy Policy",
    "terms.html": "Terms",
}


def create_html_sitemap():
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sitemap – All Loan Calculators | LoanWise</title>
  <meta name="description" content="Complete sitemap of all free loan calculators: car, personal, mortgage, business, and country-specific tools.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://www.loanwise.site/sitemap.html">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header class="site-header">
    <div class="site-header-inner">
      <nav class="site-nav" aria-label="Main navigation">
        <a href="index.html" class="site-logo">
          <span class="logo-icon" aria-hidden="true">L</span>
          <span class="logo-text">LoanWise</span>
        </a>
        <div class="site-nav-scroll">
          <a href="index.html">Home</a>
          <a href="sitemap.html">Sitemap</a>
          <a href="car-loan-calculator.html">Car Loan</a>
          <a href="personal-loan-calculator.html">Personal Loan</a>
          <a href="mortgage-calculator.html">Mortgage</a>
          <a href="about.html">About</a>
          <a href="contact.html">Contact</a>
        </div>
      </nav>
    </div>
  </header>

  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="index.html">Home</a>
      <span class="breadcrumb-sep" aria-hidden="true">›</span>
      <span aria-current="page">Sitemap</span>
    </nav>
    <header class="page-header">
      <h1>Sitemap – All Pages</h1>
      <p class="subtitle">Every loan calculator and tool in one place. Last updated: ''' + SITEMAP_DATE + '''</p>
    </header>

    <main class="page-content">
      <p class="intro-lead">Use this page to find any calculator or navigate the site. All tools are free and require no signup.</p>

'''
    for section, files in PAGES_BY_SECTION.items():
        html += f'      <section class="content-section">\n        <h2>{section}</h2>\n        <ul class="sitemap-list">\n'
        for f in files:
            if os.path.exists(os.path.join(BASE, f)):
                label = LABELS.get(f, f.replace(".html", "").replace("-", " ").title())
                html += f'          <li><a href="{f}">{label}</a></li>\n'
        html += "        </ul>\n      </section>\n\n"
    html += '''    </main>
  </div>

  <footer class="site-footer">
    <div class="site-footer-inner">
      <div class="footer-bottom">
        <p class="copyright">© 2025 LoanWise. <a href="index.html">Home</a> · <a href="sitemap.html">Sitemap</a> · <a href="contact.html">Contact</a></p>
      </div>
    </div>
  </footer>
</body>
</html>
'''
    path = os.path.join(BASE, "sitemap.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Created sitemap.html")


def add_sitemap_to_nav():
    """Add Sitemap link to nav in all pages that have site-nav."""
    for fname in os.listdir(BASE):
        if not fname.endswith(".html") or fname == "sitemap.html":
            continue
        path = os.path.join(BASE, fname)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if "site-nav" in content and "sitemap.html" not in content:
            # Add before Terms (after Privacy Policy)
            new_content = re.sub(
                r'(<a href="privacy-policy\.html">Privacy Policy</a>\s*)',
                r'\1<a href="sitemap.html">Sitemap</a>\n        ',
                content,
                count=1,
            )
            if new_content != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"  Added sitemap link to {fname}")


def add_last_updated():
    """Add last-updated paragraph to pages that don't have it (after page-header)."""
    last_updated_html = f'      <p class="last-updated">Last updated: {SITEMAP_DATE}</p>\n'
    count = 0
    for fname in os.listdir(BASE):
        if not fname.endswith(".html"):
            continue
        path = os.path.join(BASE, fname)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if "last-updated" in content:
            continue
        # Insert after </header> when inside page-header, before <main or next section
        if "page-header" in content and "<main" in content:
            content = re.sub(
                r'(<p class="intro-lead">[^<]+</p>\s*)(</header>\s*<main)',
                r'\1' + last_updated_html + r'\2',
                content,
                count=1,
            )
            if last_updated_html in content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"  Added last-updated to {fname}")
                count += 1


def update_sitemap_xml():
    """Add lastmod to sitemap.xml and ensure sitemap.html is included."""
    path = os.path.join(BASE, "sitemap.xml")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # Add lastmod after each </loc> when not already present
    if content.count("<lastmod>") < 2:
        content = re.sub(
            r'(<loc>[^<]+</loc>)\s*\n(\s*</url>)',
            r'\1\n  <lastmod>' + SITEMAP_DATE + r'</lastmod>\n\2',
            content,
        )
    # Add sitemap.html if not present
    if "sitemap.html" not in content:
        content = content.replace(
            "</urlset>",
            f'<url>\n  <loc>https://loanwisecalc.com/sitemap.html</loc>\n  <lastmod>{SITEMAP_DATE}</lastmod>\n</url>\n</urlset>',
        )
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated sitemap.xml with lastmod and sitemap.html")


def add_css_preload():
    """Add preload for critical CSS in head."""
    for fname in ["index.html", "car-loan-calculator.html", "personal-loan-calculator.html", "mortgage-calculator.html"]:
        path = os.path.join(BASE, fname)
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if 'rel="preload"' in content:
            continue
        content = content.replace(
            '<link rel="stylesheet" href="style.css">',
            '<link rel="preload" href="style.css" as="style">\n  <link rel="stylesheet" href="style.css">',
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Added CSS preload to {fname}")


def add_sitemap_to_footer():
    """Add Sitemap to Company footer column."""
    for fname in os.listdir(BASE):
        if not fname.endswith(".html") or fname == "sitemap.html":
            continue
        path = os.path.join(BASE, fname)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        # Add to Company column: after Contact, before </ul> (unique pattern for Company block)
        if "footer-map" in content:
            old_block = '''            <li><a href="about.html">About</a></li>
            <li><a href="contact.html">Contact</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h3 class="footer-col-title">Legal</h3>'''
            new_block = '''            <li><a href="about.html">About</a></li>
            <li><a href="contact.html">Contact</a></li>
            <li><a href="sitemap.html">Sitemap</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h3 class="footer-col-title">Legal</h3>'''
            if old_block in content:
                content = content.replace(old_block, new_block)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"  Added sitemap to footer: {fname}")


def main():
    print("1. Creating HTML sitemap...")
    create_html_sitemap()
    print("2. Adding sitemap to navigation...")
    add_sitemap_to_nav()
    print("3. Adding sitemap to footer...")
    add_sitemap_to_footer()
    print("4. Adding last-updated to pages...")
    add_last_updated()
    print("5. Updating sitemap.xml...")
    update_sitemap_xml()
    print("6. Adding CSS preload for speed...")
    add_css_preload()
    print("Done.")


if __name__ == "__main__":
    main()
