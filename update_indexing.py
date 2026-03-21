#!/usr/bin/env python3
"""
Update LoanWise indexing structure after bulk page generation:
- Regenerate sitemap.xml with all pages
- Regenerate HTML sitemap with all pages by category
- Add footer navigation blocks by category to all pages
- Ensure homepage links to major category pages

Run: python3 update_indexing.py
"""

import os
import re
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
CANONICAL = "https://loanwisecalc.com"
LASTMOD = datetime.now().strftime("%Y-%m-%d")

from config.internal_linking import classify_page, _short_label


def discover_pages():
    """All .html files in base dir, excluding templates."""
    return sorted(
        f for f in os.listdir(BASE)
        if f.endswith(".html") and os.path.isfile(os.path.join(BASE, f))
        and not f.startswith(".")
    )


def build_sitemap_xml(files):
    """Generate clean sitemap.xml with all pages."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    # Index first
    if "index.html" in files:
        lines.append("")
        lines.append("<url>")
        lines.append(f"  <loc>{CANONICAL}/</loc>")
        lines.append(f"  <lastmod>{LASTMOD}</lastmod>")
        lines.append("</url>")
    for f in files:
        if f == "index.html":
            continue
        loc = f"{CANONICAL}/{f}"
        lines.append("")
        lines.append("<url>")
        lines.append(f"  <loc>{loc}</loc>")
        lines.append(f"  <lastmod>{LASTMOD}</lastmod>")
        lines.append("</url>")
    lines.append("")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def group_pages_for_sitemap(files):
    """Group pages by category for HTML sitemap."""
    all_files = set(files)
    groups = {
        "Loan Calculators": [],
        "Car Loan Calculators": [],
        "Personal Loan Calculators": [],
        "Mortgage Calculators": [],
        "Country Calculators": [],
        "Loan Tools": [],
        "Company": [],
        "Legal": [],
    }
    loan_tools = {
        "loan-calculator-with-down-payment.html",
        "loan-calculator-with-extra-payments.html",
        "loan-calculator-with-interest-breakdown.html",
        "simple-loan-payment-example.html",
        "how-to-calculate-loan-monthly-payment.html",
        "interest-calculator.html",
        "simple-interest-calculator.html",
    }
    for f in files:
        info = classify_page(f, all_files)
        cluster = info.get("cluster", "")
        label = info.get("current_label", _short_label(f))
        if f == "index.html":
            groups["Loan Calculators"].append(("index.html", "Loan Calculator"))
        elif cluster == "general" and f != "index.html":
            if f in loan_tools:
                groups["Loan Tools"].append((f, label))
            else:
                groups["Loan Calculators"].append((f, label))
        elif cluster == "car":
            groups["Car Loan Calculators"].append((f, label))
        elif cluster == "personal":
            groups["Personal Loan Calculators"].append((f, label))
        elif cluster == "mortgage":
            groups["Mortgage Calculators"].append((f, label))
        elif cluster == "country":
            groups["Country Calculators"].append((f, label))
        elif cluster == "business":
            groups["Loan Calculators"].append((f, label))  # or separate Business
        elif f in ("about.html", "contact.html", "sitemap.html"):
            groups["Company"].append((f, info.get("current_label", f)))
        elif f in ("privacy-policy.html", "terms.html"):
            groups["Legal"].append((f, info.get("current_label", f)))
    return groups


def build_footer_html(files):
    """Build footer with category blocks. Curated key pages per category."""
    all_files = set(files)

    def col(title, items, max_items=10):
        filtered = [(h, l) for h, l in items if h in all_files][:max_items]
        if not filtered:
            return ""
        lis = "\n            ".join(f'<li><a href="{h}">{l}</a></li>' for h, l in filtered)
        return f"""        <div class="footer-col">
          <h3 class="footer-col-title">{title}</h3>
          <ul class="footer-links">
            {lis}
          </ul>
        </div>"""

    loan_items = [
        ("index.html", "Loan Calculator"),
        ("car-loan-calculator.html", "Car Loan Calculator"),
        ("personal-loan-calculator.html", "Personal Loan Calculator"),
        ("mortgage-calculator.html", "Mortgage Calculator"),
        ("business-loan-calculator.html", "Business Loan Calculator"),
        ("interest-calculator.html", "Interest Calculator"),
        ("loan-10000-monthly-payment.html", "Loan for $10,000"),
        ("loan-20000-monthly-payment.html", "Loan for $20,000"),
        ("loan-calculator-with-down-payment.html", "Loan with Down Payment"),
        ("sitemap.html", "Sitemap"),
    ]
    car_items = [
        ("car-loan-calculator.html", "Car Loan Calculator"),
        ("auto-loan-calculator.html", "Auto Loan Calculator"),
        ("auto-loan-refinance-calculator.html", "Auto Loan Refinance"),
        ("car-loan-20000-monthly-payment.html", "Car Loan for $20,000"),
        ("car-loan-30000-monthly-payment.html", "Car Loan for $30,000"),
        ("used-car-loan-calculator.html", "Used Car Loan"),
        ("car-loan-with-trade-in-calculator.html", "Car Loan with Trade-In"),
        ("auto-loan-calculator-60-months.html", "60 Month Auto Loan"),
        ("how-much-car-loan-can-i-afford.html", "How Much Can I Afford"),
    ]
    personal_items = [
        ("personal-loan-calculator.html", "Personal Loan Calculator"),
        ("bad-credit-loan-calculator.html", "Bad Credit Loan"),
        ("personal-loan-10000-payment.html", "Personal Loan for $10,000"),
        ("personal-loan-20000-payment.html", "Personal Loan for $20,000"),
        ("debt-consolidation-loan-calculator.html", "Debt Consolidation"),
        ("home-improvement-loan-calculator.html", "Home Improvement Loan"),
    ]
    mortgage_items = [
        ("mortgage-calculator.html", "Mortgage Calculator"),
        ("mortgage-200k-payment.html", "Mortgage for $200k"),
        ("mortgage-300k-payment.html", "Mortgage for $300k"),
        ("mortgage-30-year-calculator.html", "30-Year Mortgage"),
        ("mortgage-15-year-calculator.html", "15-Year Mortgage"),
    ]
    country_items = [
        ("loan-calculator-usa.html", "USA"),
        ("loan-calculator-uk.html", "UK"),
        ("loan-calculator-canada.html", "Canada"),
        ("loan-calculator-australia.html", "Australia"),
        ("loan-calculator-uae.html", "UAE"),
        ("loan-calculator-morocco.html", "Morocco"),
        ("loan-calculator-india.html", "India"),
        ("loan-calculator-singapore.html", "Singapore"),
        ("loan-calculator-new-zealand.html", "New Zealand"),
        ("loan-calculator-ireland.html", "Ireland"),
    ]
    company_items = [("about.html", "About"), ("contact.html", "Contact"), ("sitemap.html", "Sitemap")]
    legal_items = [("privacy-policy.html", "Privacy Policy"), ("terms.html", "Terms")]

    loan = col("Loan Calculators", loan_items)
    car = col("Car Loan Calculators", car_items)
    personal = col("Personal Loan Calculators", personal_items)
    mortgage = col("Mortgage Calculators", mortgage_items)
    country = col("Country Calculators", country_items)
    company = col("Company", company_items)
    legal = col("Legal", legal_items)

    cols = [c for c in [loan, car, personal, mortgage, country, company, legal] if c]
    nav = "\n".join(cols)

    return f'''  <footer class="site-footer">
    <div class="site-footer-inner">
      <nav class="footer-map" aria-label="Footer links">
{nav}
      </nav>
      <div class="footer-bottom">
        <p class="copyright">© 2025 LoanWise. All rights reserved.</p>
      </div>
    </div>
  </footer>'''


def build_html_sitemap(files):
    """Build full HTML sitemap page."""
    groups = group_pages_for_sitemap(files)
    sections = []
    for title, items in groups.items():
        if not items:
            continue
        lis = "\n          ".join(f'<li><a href="{h}">{l}</a></li>' for h, l in items)
        sections.append(f"""      <section class="content-section">
        <h2>{title}</h2>
        <ul class="sitemap-list">
          {lis}
        </ul>
      </section>""")
    body_sections = "\n\n".join(sections)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sitemap – All Loan Calculators | LoanWise</title>
  <meta name="description" content="Complete sitemap of all free loan calculators: car, personal, mortgage, business, and country-specific tools.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{CANONICAL}/sitemap.html">
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
      <p class="subtitle">Every loan calculator and tool in one place. Last updated: {LASTMOD}</p>
    </header>

    <main class="page-content">
      <p class="intro-lead">Use this page to find any calculator or navigate the site. All tools are free and require no signup.</p>

{body_sections}

    </main>
  </div>

  <footer class="site-footer">
    <div class="site-footer-inner">
      <nav class="footer-map" aria-label="Footer links">
        <div class="footer-col">
          <h3 class="footer-col-title">Loan Calculators</h3>
          <ul class="footer-links">
            <li><a href="index.html">Loan Calculator</a></li>
            <li><a href="car-loan-calculator.html">Car Loan</a></li>
            <li><a href="personal-loan-calculator.html">Personal Loan</a></li>
            <li><a href="mortgage-calculator.html">Mortgage</a></li>
            <li><a href="sitemap.html">Sitemap</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h3 class="footer-col-title">Company</h3>
          <ul class="footer-links">
            <li><a href="about.html">About</a></li>
            <li><a href="contact.html">Contact</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h3 class="footer-col-title">Legal</h3>
          <ul class="footer-links">
            <li><a href="privacy-policy.html">Privacy Policy</a></li>
            <li><a href="terms.html">Terms</a></li>
          </ul>
        </div>
      </nav>
      <div class="footer-bottom">
        <p class="copyright">© 2025 LoanWise. All rights reserved.</p>
      </div>
    </div>
  </footer>
</body>
</html>'''


def apply_footer_to_pages(files, footer_html):
    """Replace footer in all HTML files."""
    # Match from <footer to </footer> inclusive
    footer_pattern = re.compile(
        r'<footer class="site-footer">.*?</footer>',
        re.DOTALL,
    )
    updated = 0
    for fname in files:
        path = os.path.join(BASE, fname)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if "<footer class=\"site-footer\">" not in content:
            continue
        new_content = footer_pattern.sub(footer_html, content, count=1)
        if new_content != content:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            updated += 1
            print(f"  Updated footer: {fname}")
    return updated


def ensure_homepage_category_links(content):
    """Ensure homepage has prominent links to major category pages."""
    # Homepage already has nav + help text. Add a block before related if missing.
    major = '''    <section class="content-section home-categories" aria-labelledby="categories-heading">
      <h2 id="categories-heading">Popular Calculators</h2>
      <p class="home-section-lede">Jump to the calculator you need:</p>
      <ul class="sitemap-list">
        <li><a href="index.html">Loan Calculator</a></li>
        <li><a href="car-loan-calculator.html">Car Loan Calculator</a></li>
        <li><a href="personal-loan-calculator.html">Personal Loan Calculator</a></li>
        <li><a href="mortgage-calculator.html">Mortgage Calculator</a></li>
        <li><a href="loan-calculator-usa.html">Loan Calculator USA</a></li>
        <li><a href="loan-calculator-uk.html">Loan Calculator UK</a></li>
        <li><a href="sitemap.html">Full Sitemap</a></li>
      </ul>
    </section>

'''
    if "home-categories" in content or "categories-heading" in content:
        return content  # Already has it
    # Insert before first <section class="content-section or before related-calculators
    match = re.search(r'(\s*)(<section class="content-section)', content)
    if match:
        insert_pos = match.start(2)
        content = content[:insert_pos] + major + content[insert_pos:]
    return content


def main():
    files = discover_pages()
    all_files = set(files)
    print(f"Found {len(files)} HTML pages")

    # 1. Regenerate sitemap.xml
    xml = build_sitemap_xml(files)
    xml_path = os.path.join(BASE, "sitemap.xml")
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"Updated sitemap.xml ({len(files)} URLs)")

    # 2. Regenerate HTML sitemap
    sitemap_html = build_html_sitemap(files)
    sitemap_path = os.path.join(BASE, "sitemap.html")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap_html)
    print("Updated sitemap.html")

    # 3. Build and apply footer to all pages
    footer_html = build_footer_html(files)
    print("Applying footer to all pages...")
    updated = apply_footer_to_pages(files, footer_html)
    print(f"  Footer updated on {updated} pages")

    # 4. Ensure homepage has category links block
    index_path = os.path.join(BASE, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        index_content = f.read()
    new_index = ensure_homepage_category_links(index_content)
    if new_index != index_content:
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(new_index)
        print("Added Popular Calculators block to homepage")
    else:
        print("Homepage already has category links")

    print("\nDone.")


if __name__ == "__main__":
    main()
