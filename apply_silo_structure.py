#!/usr/bin/env python3
"""Apply SEO silo structure: breadcrumbs + silo-aware Related Calculators."""

import os
import re

BASE = "/Users/mac/Desktop/LoanWise"

# (file, [(href, label)], current_label)
# Current label = None means it's the last item (current page)
BREADCRUMBS = {
    "index.html": ([], "Home"),
    "about.html": ([("index.html", "Home")], "About"),
    "contact.html": ([("index.html", "Home")], "Contact"),
    "sitemap.html": ([("index.html", "Home")], "Sitemap"),
    "terms.html": ([("index.html", "Home")], "Terms"),
    "privacy-policy.html": ([("index.html", "Home")], "Privacy Policy"),
    # Loan silo
    "loan-2000-monthly-payment.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Loan for $2,000"),
    "loan-3000-monthly-payment.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Loan for $3,000"),
    "loan-5000-monthly-payment.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Loan for $5,000"),
    "loan-7000-monthly-payment.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Loan for $7,000"),
    "loan-8000-monthly-payment.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Loan for $8,000"),
    "loan-10000-monthly-payment.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Loan for $10,000"),
    "loan-12000-monthly-payment.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Loan for $12,000"),
    "loan-15000-monthly-payment.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Loan for $15,000"),
    "loan-20000-monthly-payment.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Loan for $20,000"),
    "loan-4000-monthly-payment.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Loan for $4,000"),
    "loan-6000-monthly-payment.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Loan for $6,000"),
    "loan-9000-monthly-payment.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Loan for $9,000"),
    "loan-11000-monthly-payment.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Loan for $11,000"),
    "loan-14000-monthly-payment.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Loan for $14,000"),
    "loan-16000-monthly-payment.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Loan for $16,000"),
    "loan-18000-monthly-payment.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Loan for $18,000"),
    "loan-25000-monthly-payment.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Loan for $25,000"),
    "loan-30000-monthly-payment.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Loan for $30,000"),
    "loan-35000-monthly-payment.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Loan for $35,000"),
    "loan-40000-monthly-payment.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Loan for $40,000"),
    "loan-45000-monthly-payment.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Loan for $45,000"),
    "loan-50000-monthly-payment.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Loan for $50,000"),
    "loan-calculator-with-down-payment.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Loan with Down Payment"),
    "loan-calculator-with-extra-payments.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Loan with Extra Payments"),
    "loan-calculator-with-interest-breakdown.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Loan with Interest Breakdown"),
    "simple-loan-payment-example.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Simple Loan Example"),
    "how-to-calculate-loan-monthly-payment.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "How to Calculate Loan Payment"),
    "interest-calculator.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Interest Calculator"),
    "simple-interest-calculator.html": ([("index.html", "Home"), ("index.html", "Loan Calculator")], "Simple Interest Calculator"),
    # Car Loan silo
    "car-loan-calculator.html": ([("index.html", "Home")], "Car Loan Calculator"),
    "auto-loan-calculator.html": ([("index.html", "Home"), ("car-loan-calculator.html", "Car Loan Calculator")], "Auto Loan Calculator"),
    "car-loan-15000-monthly-payment.html": ([("index.html", "Home"), ("car-loan-calculator.html", "Car Loan Calculator")], "Car Loan for $15,000"),
    "car-loan-20000-monthly-payment.html": ([("index.html", "Home"), ("car-loan-calculator.html", "Car Loan Calculator")], "Car Loan for $20,000"),
    "car-loan-25000-monthly-payment.html": ([("index.html", "Home"), ("car-loan-calculator.html", "Car Loan Calculator")], "Car Loan for $25,000"),
    "car-loan-30000-monthly-payment.html": ([("index.html", "Home"), ("car-loan-calculator.html", "Car Loan Calculator")], "Car Loan for $30,000"),
    "car-loan-40000-monthly-payment.html": ([("index.html", "Home"), ("car-loan-calculator.html", "Car Loan Calculator")], "Car Loan for $40,000"),
    "car-loan-50000-monthly-payment.html": ([("index.html", "Home"), ("car-loan-calculator.html", "Car Loan Calculator")], "Car Loan for $50,000"),
    "car-loan-60000-monthly-payment.html": ([("index.html", "Home"), ("car-loan-calculator.html", "Car Loan Calculator")], "Car Loan for $60,000"),
    "car-loan-10000-monthly-payment.html": ([("index.html", "Home"), ("car-loan-calculator.html", "Car Loan Calculator")], "Car Loan for $10,000"),
    "car-loan-12000-monthly-payment.html": ([("index.html", "Home"), ("car-loan-calculator.html", "Car Loan Calculator")], "Car Loan for $12,000"),
    "car-loan-14000-monthly-payment.html": ([("index.html", "Home"), ("car-loan-calculator.html", "Car Loan Calculator")], "Car Loan for $14,000"),
    "car-loan-18000-monthly-payment.html": ([("index.html", "Home"), ("car-loan-calculator.html", "Car Loan Calculator")], "Car Loan for $18,000"),
    "car-loan-22000-monthly-payment.html": ([("index.html", "Home"), ("car-loan-calculator.html", "Car Loan Calculator")], "Car Loan for $22,000"),
    "car-loan-28000-monthly-payment.html": ([("index.html", "Home"), ("car-loan-calculator.html", "Car Loan Calculator")], "Car Loan for $28,000"),
    "car-loan-35000-monthly-payment.html": ([("index.html", "Home"), ("car-loan-calculator.html", "Car Loan Calculator")], "Car Loan for $35,000"),
    "car-loan-45000-monthly-payment.html": ([("index.html", "Home"), ("car-loan-calculator.html", "Car Loan Calculator")], "Car Loan for $45,000"),
    "car-loan-55000-monthly-payment.html": ([("index.html", "Home"), ("car-loan-calculator.html", "Car Loan Calculator")], "Car Loan for $55,000"),
    "car-loan-70000-monthly-payment.html": ([("index.html", "Home"), ("car-loan-calculator.html", "Car Loan Calculator")], "Car Loan for $70,000"),
    "car-loan-80000-monthly-payment.html": ([("index.html", "Home"), ("car-loan-calculator.html", "Car Loan Calculator")], "Car Loan for $80,000"),
    "how-much-car-loan-can-i-afford.html": ([("index.html", "Home"), ("car-loan-calculator.html", "Car Loan Calculator")], "How Much Car Loan Can I Afford"),
    "car-loan-monthly-payment-calculator.html": ([("index.html", "Home"), ("car-loan-calculator.html", "Car Loan Calculator")], "Car Loan Monthly Payment"),
    "auto-loan-calculator-48-months.html": ([("index.html", "Home"), ("car-loan-calculator.html", "Car Loan Calculator")], "48 Month Auto Loan"),
    "auto-loan-calculator-60-months.html": ([("index.html", "Home"), ("car-loan-calculator.html", "Car Loan Calculator")], "60 Month Auto Loan"),
    "car-loan-with-trade-in-calculator.html": ([("index.html", "Home"), ("car-loan-calculator.html", "Car Loan Calculator")], "Car Loan with Trade-In"),
    # Personal Loan silo
    "personal-loan-calculator.html": ([("index.html", "Home")], "Personal Loan Calculator"),
    "personal-loan-3000-payment.html": ([("index.html", "Home"), ("personal-loan-calculator.html", "Personal Loan Calculator")], "Personal Loan for $3,000"),
    "personal-loan-5000-payment.html": ([("index.html", "Home"), ("personal-loan-calculator.html", "Personal Loan Calculator")], "Personal Loan for $5,000"),
    "personal-loan-8000-payment.html": ([("index.html", "Home"), ("personal-loan-calculator.html", "Personal Loan Calculator")], "Personal Loan for $8,000"),
    "personal-loan-10000-payment.html": ([("index.html", "Home"), ("personal-loan-calculator.html", "Personal Loan Calculator")], "Personal Loan for $10,000"),
    "personal-loan-15000-payment.html": ([("index.html", "Home"), ("personal-loan-calculator.html", "Personal Loan Calculator")], "Personal Loan for $15,000"),
    "personal-loan-20000-payment.html": ([("index.html", "Home"), ("personal-loan-calculator.html", "Personal Loan Calculator")], "Personal Loan for $20,000"),
    "personal-loan-2000-payment.html": ([("index.html", "Home"), ("personal-loan-calculator.html", "Personal Loan Calculator")], "Personal Loan for $2,000"),
    "personal-loan-4000-payment.html": ([("index.html", "Home"), ("personal-loan-calculator.html", "Personal Loan Calculator")], "Personal Loan for $4,000"),
    "personal-loan-6000-payment.html": ([("index.html", "Home"), ("personal-loan-calculator.html", "Personal Loan Calculator")], "Personal Loan for $6,000"),
    "personal-loan-7000-payment.html": ([("index.html", "Home"), ("personal-loan-calculator.html", "Personal Loan Calculator")], "Personal Loan for $7,000"),
    "personal-loan-9000-payment.html": ([("index.html", "Home"), ("personal-loan-calculator.html", "Personal Loan Calculator")], "Personal Loan for $9,000"),
    "personal-loan-11000-payment.html": ([("index.html", "Home"), ("personal-loan-calculator.html", "Personal Loan Calculator")], "Personal Loan for $11,000"),
    "personal-loan-12000-payment.html": ([("index.html", "Home"), ("personal-loan-calculator.html", "Personal Loan Calculator")], "Personal Loan for $12,000"),
    "personal-loan-14000-payment.html": ([("index.html", "Home"), ("personal-loan-calculator.html", "Personal Loan Calculator")], "Personal Loan for $14,000"),
    "personal-loan-18000-payment.html": ([("index.html", "Home"), ("personal-loan-calculator.html", "Personal Loan Calculator")], "Personal Loan for $18,000"),
    "personal-loan-25000-payment.html": ([("index.html", "Home"), ("personal-loan-calculator.html", "Personal Loan Calculator")], "Personal Loan for $25,000"),
    # Mortgage silo
    "mortgage-calculator.html": ([("index.html", "Home")], "Mortgage Calculator"),
    "mortgage-30-year-calculator.html": ([("index.html", "Home"), ("mortgage-calculator.html", "Mortgage Calculator")], "30-Year Mortgage"),
    "mortgage-150k-payment.html": ([("index.html", "Home"), ("mortgage-calculator.html", "Mortgage Calculator")], "Mortgage for $150k"),
    "mortgage-200k-payment.html": ([("index.html", "Home"), ("mortgage-calculator.html", "Mortgage Calculator")], "Mortgage for $200k"),
    "mortgage-250k-payment.html": ([("index.html", "Home"), ("mortgage-calculator.html", "Mortgage Calculator")], "Mortgage for $250k"),
    "mortgage-300k-payment.html": ([("index.html", "Home"), ("mortgage-calculator.html", "Mortgage Calculator")], "Mortgage for $300k"),
    "mortgage-400k-payment.html": ([("index.html", "Home"), ("mortgage-calculator.html", "Mortgage Calculator")], "Mortgage for $400k"),
    "mortgage-100k-payment.html": ([("index.html", "Home"), ("mortgage-calculator.html", "Mortgage Calculator")], "Mortgage for $100k"),
    "mortgage-125k-payment.html": ([("index.html", "Home"), ("mortgage-calculator.html", "Mortgage Calculator")], "Mortgage for $125k"),
    "mortgage-175k-payment.html": ([("index.html", "Home"), ("mortgage-calculator.html", "Mortgage Calculator")], "Mortgage for $175k"),
    "mortgage-225k-payment.html": ([("index.html", "Home"), ("mortgage-calculator.html", "Mortgage Calculator")], "Mortgage for $225k"),
    "mortgage-275k-payment.html": ([("index.html", "Home"), ("mortgage-calculator.html", "Mortgage Calculator")], "Mortgage for $275k"),
    "mortgage-350k-payment.html": ([("index.html", "Home"), ("mortgage-calculator.html", "Mortgage Calculator")], "Mortgage for $350k"),
    "mortgage-450k-payment.html": ([("index.html", "Home"), ("mortgage-calculator.html", "Mortgage Calculator")], "Mortgage for $450k"),
    "mortgage-500k-payment.html": ([("index.html", "Home"), ("mortgage-calculator.html", "Mortgage Calculator")], "Mortgage for $500k"),
    # Country silo
    "loan-calculator-usa.html": ([("index.html", "Home")], "Loan Calculator USA"),
    "loan-calculator-uk.html": ([("index.html", "Home")], "Loan Calculator UK"),
    "loan-calculator-canada.html": ([("index.html", "Home")], "Loan Calculator Canada"),
    "loan-calculator-uae.html": ([("index.html", "Home")], "Loan Calculator UAE"),
    "loan-calculator-morocco.html": ([("index.html", "Home")], "Loan Calculator Morocco"),
    "loan-calculator-australia.html": ([("index.html", "Home")], "Loan Calculator Australia"),
    "loan-calculator-india.html": ([("index.html", "Home")], "Loan Calculator India"),
    "loan-calculator-singapore.html": ([("index.html", "Home")], "Loan Calculator Singapore"),
    "loan-calculator-new-zealand.html": ([("index.html", "Home")], "Loan Calculator New Zealand"),
    "loan-calculator-ireland.html": ([("index.html", "Home")], "Loan Calculator Ireland"),
    # Business Loan silo
    "business-loan-calculator.html": ([("index.html", "Home")], "Business Loan Calculator"),
    "business-loan-10000-payment.html": ([("index.html", "Home"), ("business-loan-calculator.html", "Business Loan Calculator")], "Business Loan for $10,000"),
    "business-loan-20000-payment.html": ([("index.html", "Home"), ("business-loan-calculator.html", "Business Loan Calculator")], "Business Loan for $20,000"),
    "business-loan-50000-payment.html": ([("index.html", "Home"), ("business-loan-calculator.html", "Business Loan Calculator")], "Business Loan for $50,000"),
}

def build_breadcrumb(trail, current):
    parts = []
    for href, label in trail:
        parts.append(f'<a href="{href}">{label}</a>')
        parts.append('<span class="breadcrumb-sep" aria-hidden="true">›</span>')
    parts.append(f'<span aria-current="page">{current}</span>')
    return '<nav class="breadcrumb" aria-label="Breadcrumb">\n      ' + "\n      ".join(parts) + "\n    </nav>"

def build_breadcrumb_home_only():
    return '<nav class="breadcrumb" aria-label="Breadcrumb">\n      <span aria-current="page">Home</span>\n    </nav>'

# Full related links per page (main first, then siblings, then cross-silo). Exclude self.
def get_related_links(fname):
    ALL_RELATED = {
        "index.html": [("loan-10000-monthly-payment.html","Loan for $10,000"),("loan-20000-monthly-payment.html","Loan for $20,000"),("loan-calculator-with-down-payment.html","Loan with Down Payment"),("car-loan-calculator.html","Car Loan Calculator"),("personal-loan-calculator.html","Personal Loan Calculator"),("mortgage-calculator.html","Mortgage Calculator"),("loan-calculator-usa.html","Loan Calculator USA")],
        "car-loan-calculator.html": [("auto-loan-calculator.html","Auto Loan Calculator"),("car-loan-20000-monthly-payment.html","Car Loan for $20,000"),("car-loan-30000-monthly-payment.html","Car Loan for $30,000"),("auto-loan-calculator-60-months.html","60 Month Auto Loan"),("car-loan-with-trade-in-calculator.html","Car Loan with Trade-In"),("how-much-car-loan-can-i-afford.html","How Much Car Loan Can I Afford?"),("index.html","Loan Calculator"),("personal-loan-calculator.html","Personal Loan Calculator")],
        "auto-loan-calculator.html": [("car-loan-calculator.html","Car Loan Calculator"),("car-loan-20000-monthly-payment.html","Car Loan for $20,000"),("auto-loan-calculator-60-months.html","60 Month Auto Loan"),("car-loan-with-trade-in-calculator.html","Car Loan with Trade-In"),("index.html","Loan Calculator"),("personal-loan-calculator.html","Personal Loan Calculator")],
        "personal-loan-calculator.html": [("personal-loan-10000-payment.html","Personal Loan for $10,000"),("personal-loan-5000-payment.html","Personal Loan for $5,000"),("loan-10000-monthly-payment.html","Loan for $10,000"),("car-loan-calculator.html","Car Loan Calculator"),("mortgage-calculator.html","Mortgage Calculator"),("index.html","Loan Calculator")],
        "mortgage-calculator.html": [("mortgage-200k-payment.html","Mortgage for $200k"),("mortgage-300k-payment.html","Mortgage for $300k"),("mortgage-30-year-calculator.html","30-Year Mortgage"),("car-loan-calculator.html","Car Loan Calculator"),("personal-loan-calculator.html","Personal Loan Calculator"),("index.html","Loan Calculator")],
        "loan-calculator-usa.html": [("index.html","Loan Calculator"),("car-loan-calculator.html","Car Loan Calculator"),("loan-calculator-uk.html","Loan Calculator UK"),("loan-10000-monthly-payment.html","Loan for $10,000"),("personal-loan-calculator.html","Personal Loan Calculator"),("mortgage-calculator.html","Mortgage Calculator")],
        "loan-calculator-uk.html": [("index.html","Loan Calculator"),("car-loan-calculator.html","Car Loan Calculator"),("loan-calculator-usa.html","Loan Calculator USA"),("personal-loan-calculator.html","Personal Loan Calculator")],
        "loan-calculator-canada.html": [("index.html","Loan Calculator"),("car-loan-calculator.html","Car Loan Calculator"),("loan-calculator-usa.html","Loan Calculator USA")],
        "loan-calculator-uae.html": [("index.html","Loan Calculator"),("car-loan-calculator.html","Car Loan Calculator"),("loan-calculator-usa.html","Loan Calculator USA")],
        "loan-calculator-morocco.html": [("index.html","Loan Calculator"),("car-loan-calculator.html","Car Loan Calculator")],
        "loan-calculator-australia.html": [("index.html","Loan Calculator"),("car-loan-calculator.html","Car Loan Calculator"),("loan-calculator-uk.html","Loan Calculator UK")],
        "business-loan-calculator.html": [("business-loan-10000-payment.html","Business Loan for $10,000"),("business-loan-50000-payment.html","Business Loan for $50,000"),("personal-loan-calculator.html","Personal Loan Calculator"),("car-loan-calculator.html","Car Loan Calculator"),("index.html","Loan Calculator")],
    }
    # Car loan amount pages
    car_amounts = ["10000","12000","14000","15000","18000","20000","22000","25000","28000","30000","35000","40000","45000","50000","55000","60000","70000","80000"]
    for amt in car_amounts:
        p = f"car-loan-{amt}-monthly-payment.html"
        if p not in ALL_RELATED:
            sibs = [f"car-loan-{a}-monthly-payment.html" for a in car_amounts if a!=amt][:3]
            ALL_RELATED[p] = [("car-loan-calculator.html","Car Loan Calculator")] + [(f, f"Car Loan for ${int(a):,}") for f,a in zip(sibs,[a for a in car_amounts if a!=amt][:3])] + [("auto-loan-calculator.html","Auto Loan Calculator"),("index.html","Loan Calculator"),("personal-loan-calculator.html","Personal Loan Calculator")]
    # Loan amount pages
    loan_amounts = ["2000","3000","5000","7000","8000","10000","12000","15000","20000"]
    for amt in loan_amounts:
        p = f"loan-{amt}-monthly-payment.html"
        if p not in ALL_RELATED:
            ALL_RELATED[p] = [("index.html","Loan Calculator"),("personal-loan-calculator.html","Personal Loan Calculator"),("loan-10000-monthly-payment.html","Loan for $10,000") if amt!="10000" else ("loan-20000-monthly-payment.html","Loan for $20,000"),("car-loan-calculator.html","Car Loan Calculator"),("mortgage-calculator.html","Mortgage Calculator"),("loan-calculator-usa.html","Loan Calculator USA")]
    # Personal loan amount pages
    for amt in ["2000","3000","4000","5000","6000","7000","8000","9000","10000","11000","12000","14000","15000","18000","20000","25000"]:
        p = f"personal-loan-{amt}-payment.html"
        if p not in ALL_RELATED:
            ALL_RELATED[p] = [("personal-loan-calculator.html","Personal Loan Calculator"),("loan-10000-monthly-payment.html","Loan for $10,000"),("car-loan-calculator.html","Car Loan Calculator"),("mortgage-calculator.html","Mortgage Calculator"),("index.html","Loan Calculator")]
    # Mortgage amount pages
    for k in ["100k","125k","150k","175k","200k","225k","250k","275k","300k","350k","400k","450k","500k"]:
        p = f"mortgage-{k}-payment.html"
        if p not in ALL_RELATED:
            ALL_RELATED[p] = [("mortgage-calculator.html","Mortgage Calculator"),("mortgage-30-year-calculator.html","30-Year Mortgage"),("car-loan-calculator.html","Car Loan Calculator"),("personal-loan-calculator.html","Personal Loan Calculator"),("index.html","Loan Calculator")]
    # Business loan amount pages
    for amt in ["10000","20000","50000"]:
        p = f"business-loan-{amt}-payment.html"
        if p not in ALL_RELATED:
            ALL_RELATED[p] = [("business-loan-calculator.html","Business Loan Calculator"),("personal-loan-calculator.html","Personal Loan Calculator"),("index.html","Loan Calculator"),("car-loan-calculator.html","Car Loan Calculator")]
    # Other loan tools
    for p, links in [
        ("loan-calculator-with-down-payment.html", [("car-loan-with-trade-in-calculator.html","Car Loan with Trade-In"),("loan-calculator-with-extra-payments.html","Loan with Extra Payments"),("car-loan-calculator.html","Car Loan Calculator"),("mortgage-calculator.html","Mortgage Calculator"),("index.html","Loan Calculator")]),
        ("loan-calculator-with-extra-payments.html", [("loan-calculator-with-down-payment.html","Loan with Down Payment"),("loan-calculator-with-interest-breakdown.html","Loan with Interest Breakdown"),("car-loan-calculator.html","Car Loan Calculator"),("mortgage-calculator.html","Mortgage Calculator"),("index.html","Loan Calculator")]),
        ("loan-calculator-with-interest-breakdown.html", [("interest-calculator.html","Interest Calculator"),("simple-interest-calculator.html","Simple Interest Calculator"),("index.html","Loan Calculator"),("car-loan-calculator.html","Car Loan Calculator"),("mortgage-calculator.html","Mortgage Calculator")]),
        ("simple-loan-payment-example.html", [("loan-calculator-with-interest-breakdown.html","Loan with Interest Breakdown"),("interest-calculator.html","Interest Calculator"),("index.html","Loan Calculator"),("car-loan-calculator.html","Car Loan Calculator")]),
        ("how-to-calculate-loan-monthly-payment.html", [("index.html","Loan Calculator"),("car-loan-calculator.html","Car Loan Calculator"),("personal-loan-calculator.html","Personal Loan Calculator"),("mortgage-calculator.html","Mortgage Calculator")]),
        ("interest-calculator.html", [("simple-interest-calculator.html","Simple Interest Calculator"),("loan-calculator-with-interest-breakdown.html","Loan with Interest Breakdown"),("index.html","Loan Calculator"),("car-loan-calculator.html","Car Loan Calculator"),("mortgage-calculator.html","Mortgage Calculator")]),
        ("simple-interest-calculator.html", [("interest-calculator.html","Interest Calculator"),("index.html","Loan Calculator"),("car-loan-calculator.html","Car Loan Calculator"),("personal-loan-calculator.html","Personal Loan Calculator")]),
        ("how-much-car-loan-can-i-afford.html", [("car-loan-calculator.html","Car Loan Calculator"),("car-loan-20000-monthly-payment.html","Car Loan for $20,000"),("auto-loan-calculator.html","Auto Loan Calculator"),("personal-loan-calculator.html","Personal Loan Calculator"),("index.html","Loan Calculator")]),
        ("car-loan-monthly-payment-calculator.html", [("car-loan-calculator.html","Car Loan Calculator"),("car-loan-20000-monthly-payment.html","Car Loan for $20,000"),("auto-loan-calculator-60-months.html","60 Month Auto Loan"),("index.html","Loan Calculator")]),
        ("auto-loan-calculator-48-months.html", [("auto-loan-calculator-60-months.html","60 Month Auto Loan"),("car-loan-calculator.html","Car Loan Calculator"),("car-loan-with-trade-in-calculator.html","Car Loan with Trade-In"),("car-loan-20000-monthly-payment.html","Car Loan for $20,000"),("how-much-car-loan-can-i-afford.html","How Much Car Loan Can I Afford?"),("index.html","Loan Calculator")]),
        ("auto-loan-calculator-60-months.html", [("auto-loan-calculator-48-months.html","48 Month Auto Loan"),("car-loan-calculator.html","Car Loan Calculator"),("car-loan-with-trade-in-calculator.html","Car Loan with Trade-In"),("car-loan-30000-monthly-payment.html","Car Loan for $30,000"),("index.html","Loan Calculator")]),
        ("car-loan-with-trade-in-calculator.html", [("loan-calculator-with-down-payment.html","Loan with Down Payment"),("car-loan-calculator.html","Car Loan Calculator"),("auto-loan-calculator-60-months.html","60 Month Auto Loan"),("how-much-car-loan-can-i-afford.html","How Much Car Loan Can I Afford?"),("index.html","Loan Calculator")]),
        ("mortgage-30-year-calculator.html", [("mortgage-calculator.html","Mortgage Calculator"),("mortgage-200k-payment.html","Mortgage for $200k"),("mortgage-300k-payment.html","Mortgage for $300k"),("car-loan-calculator.html","Car Loan Calculator"),("personal-loan-calculator.html","Personal Loan Calculator"),("index.html","Loan Calculator")]),
    ("auto-loan-calculator-36-months.html", [("car-loan-calculator.html","Car Loan Calculator"),("auto-loan-calculator-48-months.html","48 Month Auto Loan"),("auto-loan-calculator-60-months.html","60 Month Auto Loan"),("car-loan-20000-monthly-payment.html","Car Loan for $20,000"),("index.html","Loan Calculator")]),
    ("auto-loan-calculator-72-months.html", [("car-loan-calculator.html","Car Loan Calculator"),("auto-loan-calculator-60-months.html","60 Month Auto Loan"),("auto-loan-calculator-48-months.html","48 Month Auto Loan"),("car-loan-30000-monthly-payment.html","Car Loan for $30,000"),("index.html","Loan Calculator")]),
    ("used-car-loan-calculator.html", [("car-loan-calculator.html","Car Loan Calculator"),("car-loan-with-trade-in-calculator.html","Car Loan with Trade-In"),("how-much-car-loan-can-i-afford.html","How Much Car Loan Can I Afford"),("auto-loan-calculator-60-months.html","60 Month Auto Loan"),("index.html","Loan Calculator")]),
    ("debt-consolidation-loan-calculator.html", [("personal-loan-calculator.html","Personal Loan Calculator"),("index.html","Loan Calculator"),("loan-10000-monthly-payment.html","Loan for $10,000"),("loan-20000-monthly-payment.html","Loan for $20,000"),("car-loan-calculator.html","Car Loan Calculator")]),
    ("home-improvement-loan-calculator.html", [("personal-loan-calculator.html","Personal Loan Calculator"),("mortgage-calculator.html","Mortgage Calculator"),("index.html","Loan Calculator"),("loan-20000-monthly-payment.html","Loan for $20,000"),("loan-calculator-with-down-payment.html","Loan with Down Payment")]),
    ("mortgage-15-year-calculator.html", [("mortgage-calculator.html","Mortgage Calculator"),("mortgage-30-year-calculator.html","30-Year Mortgage"),("mortgage-200k-payment.html","Mortgage for $200k"),("mortgage-300k-payment.html","Mortgage for $300k"),("index.html","Loan Calculator")]),
    ("loan-calculator-india.html", [("index.html","Loan Calculator"),("loan-calculator-usa.html","Loan Calculator USA"),("loan-calculator-uk.html","Loan Calculator UK"),("car-loan-calculator.html","Car Loan Calculator"),("personal-loan-calculator.html","Personal Loan Calculator")]),
    ("loan-calculator-singapore.html", [("index.html","Loan Calculator"),("loan-calculator-usa.html","Loan Calculator USA"),("loan-calculator-australia.html","Loan Calculator Australia"),("car-loan-calculator.html","Car Loan Calculator"),("personal-loan-calculator.html","Personal Loan Calculator")]),
    ("loan-calculator-new-zealand.html", [("index.html","Loan Calculator"),("loan-calculator-australia.html","Loan Calculator Australia"),("loan-calculator-uk.html","Loan Calculator UK"),("car-loan-calculator.html","Car Loan Calculator"),("personal-loan-calculator.html","Personal Loan Calculator")]),
    ("loan-calculator-ireland.html", [("index.html","Loan Calculator"),("loan-calculator-uk.html","Loan Calculator UK"),("loan-calculator-usa.html","Loan Calculator USA"),("car-loan-calculator.html","Car Loan Calculator"),("personal-loan-calculator.html","Personal Loan Calculator")]),
    ]:
        ALL_RELATED[p] = links
    out = ALL_RELATED.get(fname)
    if out:
        return [(h,t) for h,t in out if h != fname][:8]
    return None

def main():
    for fname in sorted(os.listdir(BASE)):
        if not fname.endswith(".html"):
            continue
        path = os.path.join(BASE, fname)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. Add breadcrumb
        if fname in BREADCRUMBS:
            trail, current = BREADCRUMBS[fname]
            if fname == "index.html":
                bc_html = build_breadcrumb_home_only()
            else:
                bc_html = build_breadcrumb(trail, current)

            # Insert after <div class="container"> and newline
            pattern = r'(<div class="container">)\n(\s*)(<header class="page-header|<main class="page-content)'
            replacement = r'\1\n\2' + bc_html + r'\n\2\3'
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content, count=1)

        # 2. Update Related Calculators with silo-aware links
        links = get_related_links(fname)
        if links and "related-calculators" in content:
            # Build new related section
            items = "\n        ".join(f'<li><a href="{h}">{t}</a></li>' for h, t in links)
            new_section = f'''    <section class="related-calculators" aria-labelledby="related-calculators-heading">
      <h2 id="related-calculators-heading">Related Calculators</h2>
      <ul class="related-calculators-list">
        {items}
      </ul>
    </section>'''
            content = re.sub(
                r'<section class="related-calculators" aria-labelledby="related-calculators-heading">.*?</section>',
                new_section,
                content,
                flags=re.DOTALL,
                count=1,
            )

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {fname}")

if __name__ == "__main__":
    main()
