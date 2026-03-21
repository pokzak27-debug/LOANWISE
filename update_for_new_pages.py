#!/usr/bin/env python3
"""Update sitemap.xml with new pages. Run after generate_calculator_pages.py"""

import os
from datetime import datetime

BASE = "/Users/mac/Desktop/LoanWise"
CANONICAL = "https://loanwisecalc.com"
LASTMOD = datetime.now().strftime("%Y-%m-%d")

NEW_PAGES = [
    "loan-4000-monthly-payment.html", "loan-6000-monthly-payment.html", "loan-9000-monthly-payment.html",
    "loan-11000-monthly-payment.html", "loan-14000-monthly-payment.html", "loan-16000-monthly-payment.html",
    "loan-18000-monthly-payment.html", "loan-25000-monthly-payment.html", "loan-30000-monthly-payment.html",
    "loan-35000-monthly-payment.html", "loan-40000-monthly-payment.html", "loan-45000-monthly-payment.html",
    "loan-50000-monthly-payment.html",
    "car-loan-10000-monthly-payment.html", "car-loan-12000-monthly-payment.html", "car-loan-14000-monthly-payment.html",
    "car-loan-18000-monthly-payment.html", "car-loan-22000-monthly-payment.html", "car-loan-28000-monthly-payment.html",
    "car-loan-35000-monthly-payment.html", "car-loan-45000-monthly-payment.html", "car-loan-55000-monthly-payment.html",
    "car-loan-70000-monthly-payment.html", "car-loan-80000-monthly-payment.html",
    "personal-loan-2000-payment.html", "personal-loan-4000-payment.html", "personal-loan-6000-payment.html",
    "personal-loan-7000-payment.html", "personal-loan-9000-payment.html", "personal-loan-11000-payment.html",
    "personal-loan-12000-payment.html", "personal-loan-14000-payment.html", "personal-loan-18000-payment.html",
    "personal-loan-25000-payment.html",
    "mortgage-100k-payment.html", "mortgage-125k-payment.html", "mortgage-175k-payment.html",
    "mortgage-225k-payment.html", "mortgage-275k-payment.html", "mortgage-350k-payment.html",
    "mortgage-450k-payment.html", "mortgage-500k-payment.html",
    "auto-loan-calculator-24-months.html", "auto-loan-calculator-36-months.html", "auto-loan-calculator-72-months.html",
    "mortgage-10-year-calculator.html", "mortgage-20-year-calculator.html",
    "used-car-loan-calculator.html", "debt-consolidation-loan-calculator.html",
    "home-improvement-loan-calculator.html", "mortgage-15-year-calculator.html",
    "loan-calculator-india.html", "loan-calculator-singapore.html", "loan-calculator-new-zealand.html",
    "loan-calculator-ireland.html",
    "loan-calculator-comparison.html",
]

def main():
    path = os.path.join(BASE, "sitemap.xml")
    with open(path, "r") as f:
        content = f.read()
    
    existing_urls = set()
    import re
    for m in re.finditer(r'<loc>([^<]+)</loc>', content):
        url = m.group(1)
        existing_urls.add(url.split("/")[-1])
    
    to_add = [p for p in NEW_PAGES if p not in existing_urls]
    if not to_add:
        print("All new pages already in sitemap.")
        return
    
    insert = ""
    for p in to_add:
        insert += f'''
<url>
  <loc>{CANONICAL}/{p}</loc>
  <lastmod>{LASTMOD}</lastmod>
</url>'''
    
    content = content.replace("</urlset>", insert + "\n</urlset>")
    with open(path, "w") as f:
        f.write(content)
    print(f"Added {len(to_add)} URLs to sitemap.xml")

if __name__ == "__main__":
    main()
