#!/usr/bin/env python3
"""Apply CTR-optimized titles and meta descriptions across all pages."""

import os
import re

BASE = "/Users/mac/Desktop/LoanWise"

# (title, meta_description) - max 60 chars title, max 155 chars meta
# Title: keyword + emotional trigger (Free, Fast, Easy, Instant)
# Meta: keyword + benefit + CTA
PAGES = {
    "index.html": (
        "Free Loan Calculator – Instant Monthly Payment",
        "Calculate your monthly payment, total interest, and loan cost in seconds. Free and easy—no signup. Try it now.",
    ),
    "about.html": (
        "About LoanWise – Free Loan Calculators Made Easy",
        "Meet LoanWise: free loan, car, and mortgage calculators. Fast, simple estimates. No signup. Start calculating.",
    ),
    "contact.html": (
        "Contact LoanWise – Free Calculator Support",
        "Questions about our free calculators? Get help fast. No signup required. Contact us—we reply when we can.",
    ),
    "terms.html": (
        "Terms of Use – Free Loan Calculators | LoanWise",
        "LoanWise terms: free calculators for estimates only. Simple rules. Always verify with your lender. Read more.",
    ),
    "privacy-policy.html": (
        "Privacy Policy – Free Online Calculators | LoanWise",
        "How we handle data: plain English privacy policy. No account needed. Simple and transparent. Read here.",
    ),
    "sitemap.html": (
        "Sitemap – All Loan Calculators | LoanWise",
        "Complete sitemap of all free loan calculators. Find any tool fast. No signup. Browse all pages.",
    ),
    # Loan silo
    "loan-2000-monthly-payment.html": (
        "Loan for $2,000 – Monthly Payment Free & Instant",
        "Get your $2,000 loan monthly payment in seconds. Free calculator. See total interest and cost. Calculate now.",
    ),
    "loan-3000-monthly-payment.html": (
        "Loan for $3,000 – Monthly Payment Free & Instant",
        "Get your $3,000 loan monthly payment in seconds. Free calculator. See total interest and cost. Calculate now.",
    ),
    "loan-5000-monthly-payment.html": (
        "Loan for $5,000 – Monthly Payment Free & Instant",
        "Get your $5,000 loan monthly payment in seconds. Free calculator. See total interest and cost. Calculate now.",
    ),
    "loan-7000-monthly-payment.html": (
        "Loan for $7,000 – Monthly Payment Free & Instant",
        "Get your $7,000 loan monthly payment in seconds. Free calculator. See total interest and cost. Calculate now.",
    ),
    "loan-8000-monthly-payment.html": (
        "Loan for $8,000 – Monthly Payment Free & Instant",
        "Get your $8,000 loan monthly payment in seconds. Free calculator. See total interest and cost. Calculate now.",
    ),
    "loan-10000-monthly-payment.html": (
        "Loan for $10,000 – Monthly Payment Instantly",
        "Calculate your monthly payment, total interest, and loan cost in seconds. Free and easy loan calculator.",
    ),
    "loan-12000-monthly-payment.html": (
        "Loan for $12,000 – Monthly Payment Free & Instant",
        "Get your $12,000 loan monthly payment in seconds. Free calculator. See total interest and cost. Calculate now.",
    ),
    "loan-15000-monthly-payment.html": (
        "Loan for $15,000 – Monthly Payment Free & Instant",
        "Get your $15,000 loan monthly payment in seconds. Free calculator. See total interest and cost. Calculate now.",
    ),
    "loan-20000-monthly-payment.html": (
        "Loan for $20,000 – Monthly Payment Instantly",
        "Calculate your $20k loan payment in seconds. Free tool. See monthly cost and total interest. Try it now.",
    ),
    "loan-calculator-with-down-payment.html": (
        "Loan Calculator with Down Payment – Free & Easy",
        "Enter price and down payment—see your real monthly payment instantly. Free tool. No signup. Calculate now.",
    ),
    "loan-calculator-with-extra-payments.html": (
        "Loan Calculator with Extra Payments – Free Tool",
        "See how extra payments cut interest and shorten your loan. Free instant calculator. No signup. Try it now.",
    ),
    "loan-calculator-with-interest-breakdown.html": (
        "Loan Calculator with Interest Breakdown – Free",
        "Year-by-year principal vs interest breakdown. Free instant calculator. See where your money goes. Try now.",
    ),
    "simple-loan-payment-example.html": (
        "Simple Loan Example – $10k Walkthrough Free",
        "Learn loan math with a $10k example. Free calculator included. Understand payments in minutes. Start here.",
    ),
    "how-to-calculate-loan-monthly-payment.html": (
        "How to Calculate Loan Payment – Free Guide",
        "Step-by-step loan payment formula. Free examples and calculators. Easy to follow. Master it in minutes.",
    ),
    "interest-calculator.html": (
        "Interest Calculator – Free & Instant Results",
        "Calculate loan and simple interest in seconds. Free online tool. No signup. Get your numbers now.",
    ),
    "simple-interest-calculator.html": (
        "Simple Interest Calculator – Free I=P×R×T Tool",
        "Calculate simple interest with I=P×R×T. Free and instant. Compare to compound. No signup. Try now.",
    ),
    # Car Loan silo
    "car-loan-calculator.html": (
        "Car Loan Calculator – Free Monthly Payment Now",
        "See your car loan payment instantly. Free easy calculator. Compare rates before the dealer. Calculate now.",
    ),
    "auto-loan-calculator.html": (
        "Auto Loan Calculator – Free Payment Instantly",
        "Get your auto loan monthly payment in seconds. Free tool. See total interest. No signup. Calculate now.",
    ),
    "car-loan-15000-monthly-payment.html": (
        "Car Loan for $15,000 – Monthly Payment Free",
        "$15k car loan payment in seconds. Free calculator. Compare terms. Dealer-ready numbers. Try it now.",
    ),
    "car-loan-20000-monthly-payment.html": (
        "Car Loan for $20,000 – Monthly Payment Free",
        "$20k car loan payment in seconds. Free calculator. Compare terms. Dealer-ready numbers. Try it now.",
    ),
    "car-loan-25000-monthly-payment.html": (
        "Car Loan for $25,000 – Monthly Payment Free",
        "$25k car loan payment in seconds. Free calculator. Compare terms. Dealer-ready numbers. Try it now.",
    ),
    "car-loan-30000-monthly-payment.html": (
        "Car Loan for $30,000 – Monthly Payment Free",
        "$30k car loan payment in seconds. Free calculator. Compare terms. Dealer-ready numbers. Try it now.",
    ),
    "car-loan-40000-monthly-payment.html": (
        "Car Loan for $40,000 – Monthly Payment Free",
        "$40k car loan payment in seconds. Free calculator. Compare terms. Dealer-ready numbers. Try it now.",
    ),
    "car-loan-50000-monthly-payment.html": (
        "Car Loan for $50,000 – Monthly Payment Free",
        "$50k car loan payment in seconds. Free calculator. Compare terms. Dealer-ready numbers. Try it now.",
    ),
    "car-loan-60000-monthly-payment.html": (
        "Car Loan for $60,000 – Monthly Payment Free",
        "$60k car loan payment in seconds. Free calculator. Compare terms. Dealer-ready numbers. Try it now.",
    ),
    "how-much-car-loan-can-i-afford.html": (
        "How Much Car Loan Can I Afford? – Free Tool",
        "Find your max car loan based on income and debt. Free instant calculator. Adjust rates fast. Try now.",
    ),
    "car-loan-monthly-payment-calculator.html": (
        "Car Loan Monthly Payment Calculator – Free",
        "Car payment in seconds. Free easy calculator. No signup. Dealer-ready numbers. Calculate your payment now.",
    ),
    "auto-loan-calculator-48-months.html": (
        "48 Month Auto Loan – Free Payment Calculator",
        "4-year car loan payment instantly. Free calculator. Compare 48 vs 60 months. No signup. Try now.",
    ),
    "auto-loan-calculator-60-months.html": (
        "60 Month Auto Loan – Free Payment Calculator",
        "5-year car loan payment instantly. Free calculator. Most popular term. Compare rates. Try now.",
    ),
    "car-loan-with-trade-in-calculator.html": (
        "Car Loan with Trade-In – Free Payment Tool",
        "Enter price, trade-in, and down payment—see real monthly cost. Free instant. No signup. Calculate now.",
    ),
    # Personal Loan silo
    "personal-loan-calculator.html": (
        "Personal Loan Calculator – Free Payment Instantly",
        "Calculate your personal loan payment in seconds. Free easy tool. See monthly cost before you apply. Try now.",
    ),
    "personal-loan-3000-payment.html": (
        "Personal Loan for $3,000 – Free Payment Tool",
        "$3k personal loan payment in seconds. Free calculator. See cost before you apply. No signup. Try now.",
    ),
    "personal-loan-5000-payment.html": (
        "Personal Loan for $5,000 – Free Payment Tool",
        "$5k personal loan payment in seconds. Free calculator. See cost before you apply. No signup. Try now.",
    ),
    "personal-loan-8000-payment.html": (
        "Personal Loan for $8,000 – Free Payment Tool",
        "$8k personal loan payment in seconds. Free calculator. See cost before you apply. No signup. Try now.",
    ),
    "personal-loan-10000-payment.html": (
        "Personal Loan for $10,000 – Free Payment Tool",
        "$10k personal loan payment in seconds. Free calculator. See cost before you apply. No signup. Try now.",
    ),
    "personal-loan-15000-payment.html": (
        "Personal Loan for $15,000 – Free Payment Tool",
        "$15k personal loan payment in seconds. Free calculator. See cost before you apply. No signup. Try now.",
    ),
    "personal-loan-20000-payment.html": (
        "Personal Loan for $20,000 – Free Payment Tool",
        "$20k personal loan payment in seconds. Free calculator. See cost before you apply. No signup. Try now.",
    ),
    # Mortgage silo
    "mortgage-calculator.html": (
        "Mortgage Calculator – Free Monthly Payment Now",
        "Principal & interest in seconds. Free mortgage calculator. Compare rates. No signup. Calculate your payment now.",
    ),
    "mortgage-30-year-calculator.html": (
        "30-Year Mortgage Calculator – Free & Instant",
        "30-year mortgage payment in seconds. Free calculator. See P&I and total interest. No signup. Try now.",
    ),
    "mortgage-150k-payment.html": (
        "Mortgage for $150k – Free Payment Calculator",
        "$150k mortgage payment instantly. Free tool. Adjust rate and term. See P&I. No signup. Calculate now.",
    ),
    "mortgage-200k-payment.html": (
        "Mortgage for $200k – Free Payment Calculator",
        "$200k mortgage payment instantly. Free tool. Adjust rate and term. See P&I. No signup. Calculate now.",
    ),
    "mortgage-250k-payment.html": (
        "Mortgage for $250k – Free Payment Calculator",
        "$250k mortgage payment instantly. Free tool. Adjust rate and term. See P&I. No signup. Calculate now.",
    ),
    "mortgage-300k-payment.html": (
        "Mortgage for $300k – Free Payment Calculator",
        "$300k mortgage payment instantly. Free tool. Adjust rate and term. See P&I. No signup. Calculate now.",
    ),
    "mortgage-400k-payment.html": (
        "Mortgage for $400k – Free Payment Calculator",
        "$400k mortgage payment instantly. Free tool. Adjust rate and term. See P&I. No signup. Calculate now.",
    ),
    # Country silo
    "loan-calculator-usa.html": (
        "USA Loan Calculator – Free USD Payment Instantly",
        "US loan payment in seconds. Free USD calculator. Personal, auto, or mortgage. No signup. Calculate now.",
    ),
    "loan-calculator-uk.html": (
        "UK Loan Calculator – Free GBP Payment Instantly",
        "UK loan payment in seconds. Free GBP calculator. Personal, car, or mortgage. No signup. Calculate now.",
    ),
    "loan-calculator-canada.html": (
        "Canada Loan Calculator – Free CAD Payment Instantly",
        "Canada loan payment in seconds. Free CAD calculator. Personal, auto, or mortgage. No signup. Try now.",
    ),
    "loan-calculator-australia.html": (
        "Australia Loan Calculator – Free AUD Payment",
        "Australia loan payment in seconds. Free AUD calculator. Personal, car, or mortgage. No signup. Try now.",
    ),
    "loan-calculator-uae.html": (
        "UAE Loan Calculator – Free AED Payment Instantly",
        "UAE loan payment in seconds. Free AED calculator. Personal, auto, or mortgage. No signup. Calculate now.",
    ),
    "loan-calculator-morocco.html": (
        "Morocco Loan Calculator – Free MAD Payment",
        "Morocco loan payment in seconds. Free MAD calculator. Personal, car, or mortgage. No signup. Try now.",
    ),
    # Business Loan silo
    "business-loan-calculator.html": (
        "Business Loan Calculator – Free Payment Instantly",
        "Business loan payment in seconds. Free calculator. Model cash flow before you sign. No signup. Try now.",
    ),
    "business-loan-10000-payment.html": (
        "Business Loan for $10,000 – Free Payment Tool",
        "$10k business loan payment in seconds. Free tool. Plan cash flow. No signup. Calculate your payment now.",
    ),
    "business-loan-20000-payment.html": (
        "Business Loan for $20,000 – Free Payment Tool",
        "$20k business loan payment in seconds. Free tool. Plan cash flow. No signup. Calculate your payment now.",
    ),
    "business-loan-50000-payment.html": (
        "Business Loan for $50,000 – Free Payment Tool",
        "$50k business loan payment in seconds. Free tool. Plan cash flow. No signup. Calculate your payment now.",
    ),
}


def escape_meta(s):
    return s.replace("&", "&amp;").replace('"', "&quot;")


def update_file(filepath, title, meta):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace title
    content = re.sub(r"<title>.*?</title>", f"<title>{escape_meta(title)}</title>", content)

    # Replace meta description
    content = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{escape_meta(meta)}">',
        content,
    )

    # Replace og:title if present
    content = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{escape_meta(title)}">',
        content,
    )

    # Replace og:description if present
    content = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{escape_meta(meta)}">',
        content,
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    for filename, (title, meta) in PAGES.items():
        filepath = os.path.join(BASE, filename)
        if os.path.exists(filepath):
            update_file(filepath, title, meta)
            print(f"Updated {filename}")
        else:
            print(f"SKIP (not found): {filename}")

    # Verify lengths
    for fn, (t, m) in PAGES.items():
        if len(t) > 60:
            print(f"WARN: {fn} title {len(t)} chars (max 60)")
        if len(m) > 155:
            print(f"WARN: {fn} meta {len(m)} chars (max 155)")


if __name__ == "__main__":
    main()
