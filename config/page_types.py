"""
Page type configuration for the template system.

HOW TO ADD NEW PAGES:
--------------------

1. LOAN AMOUNT PAGES - Add to GENERAL_LOAN_AMOUNTS list:
   GENERAL_LOAN_AMOUNTS.append((amount, default_rate, default_term))
   Example: (55000, 6.5, 72)
   Filename auto-generated: loan-55000-monthly-payment.html

2. CAR LOAN PAGES - Add to CAR_LOAN_AMOUNTS:
   CAR_LOAN_AMOUNTS.append((amount, default_rate, default_term))
   Example: (32000, 6.5, 60)
   Filename: car-loan-32000-monthly-payment.html

3. PERSONAL LOAN PAGES - Add to PERSONAL_LOAN_AMOUNTS:
   PERSONAL_LOAN_AMOUNTS.append((amount, default_rate, default_term))

4. MORTGAGE PAGES - Add to MORTGAGE_AMOUNTS (as thousands):
   MORTGAGE_AMOUNTS.append((amount_in_thousands, default_rate, term_months))
   Example: (375, 6.5, 360) -> mortgage-375k-payment.html

5. COUNTRY PAGES - Add to COUNTRIES list:
   COUNTRIES.append({
       "slug": "germany",
       "filename": "loan-calculator-germany.html",
       "title": "Loan Calculator Germany",
       "country": "Germany",
       "amount": 10000,
       "default_rate": 5,
       "default_term": 48,
   })

6. SPECIAL INTENT PAGES - Add to SPECIAL_INTENT_PAGES list (see structure below)
"""

# Format: (amount, default_rate, default_term_months)
# High-priority amounts for SEO: fill gaps, target common search queries
GENERAL_LOAN_AMOUNTS = [
    (2000, 12, 24), (3000, 11, 36), (4000, 10, 36), (5000, 9.5, 36), (6000, 9.5, 48),
    (7000, 9, 36), (7500, 9, 36), (8000, 9, 48), (9000, 9, 36), (10000, 9, 36), (11000, 9, 48),
    (12000, 8.5, 48), (14000, 8.5, 48), (15000, 8.5, 60), (16000, 8.5, 60),
    (17500, 8, 60), (18000, 8, 60), (20000, 8, 60), (22500, 8, 60), (25000, 8, 60),
    (27500, 7.5, 60), (30000, 7.5, 60), (32500, 7.5, 72), (35000, 7.5, 72),
    (37500, 7, 72), (40000, 7, 72), (42500, 7, 72), (45000, 7, 72), (47500, 6.5, 72),
    (50000, 6.5, 72), (55000, 6.5, 72),
]

CAR_LOAN_AMOUNTS = [
    (10000, 7.5, 48), (12000, 7, 48), (14000, 6.5, 48), (15000, 6.5, 60),
    (17500, 6.5, 60), (18000, 6.5, 60), (20000, 6.5, 60), (22000, 6.5, 60),
    (23000, 6.5, 60), (25000, 6.5, 60), (27500, 6.5, 60), (28000, 6.5, 60),
    (30000, 6.5, 60), (33000, 6.5, 60), (35000, 6.5, 60), (40000, 6, 60),
    (45000, 6, 60), (50000, 6, 60), (55000, 6, 72), (60000, 6, 72),
    (65000, 6, 72), (70000, 6, 72), (80000, 5.5, 72),
]

PERSONAL_LOAN_AMOUNTS = [
    (2000, 12, 24), (3000, 11, 36), (4000, 11, 36), (5000, 10, 36),
    (6000, 10, 36), (7000, 9.5, 36), (7500, 9, 48), (8000, 9, 48), (9000, 9, 48),
    (10000, 9, 48), (11000, 9, 48), (12000, 8.5, 48), (13000, 8.5, 48),
    (14000, 8.5, 48), (15000, 8, 60), (17500, 8, 60), (18000, 8, 60),
    (20000, 7.5, 60), (25000, 7.5, 60),
]

# Format: (amount_k, default_rate, term_months)  e.g. 200 = $200,000
MORTGAGE_AMOUNTS = [
    (100, 6.5, 360), (125, 6.5, 360), (150, 6.5, 360), (175, 6.5, 360),
    (200, 6.5, 360), (225, 6.5, 360), (250, 6.5, 360), (275, 6.5, 360),
    (300, 6.5, 360), (325, 6.5, 360), (350, 6.5, 360), (375, 6.5, 360),
    (400, 6.5, 360), (450, 6.5, 360), (500, 6.5, 360),
]

# Country pages: include amount, default_rate, default_term, loan_step for calculator defaults
COUNTRIES = [
    {"slug": "usa", "filename": "loan-calculator-usa.html", "title": "Loan Calculator USA", "country": "USA", "amount": 10000, "default_rate": 9, "default_term": 48, "loan_step": 1000},
    {"slug": "uk", "filename": "loan-calculator-uk.html", "title": "Loan Calculator UK", "country": "UK", "amount": 10000, "default_rate": 8, "default_term": 48, "loan_step": 1000},
    {"slug": "canada", "filename": "loan-calculator-canada.html", "title": "Loan Calculator Canada", "country": "Canada", "amount": 10000, "default_rate": 8, "default_term": 48, "loan_step": 1000},
    {"slug": "australia", "filename": "loan-calculator-australia.html", "title": "Loan Calculator Australia", "country": "Australia", "amount": 10000, "default_rate": 9, "default_term": 48, "loan_step": 1000},
    {"slug": "uae", "filename": "loan-calculator-uae.html", "title": "Loan Calculator UAE", "country": "UAE", "amount": 10000, "default_rate": 8, "default_term": 48, "loan_step": 1000},
    {"slug": "morocco", "filename": "loan-calculator-morocco.html", "title": "Loan Calculator Morocco", "country": "Morocco", "amount": 10000, "default_rate": 9, "default_term": 48, "loan_step": 1000},
    {"slug": "india", "filename": "loan-calculator-india.html", "title": "Loan Calculator India", "country": "India", "amount": 100000, "default_rate": 10, "default_term": 48, "loan_step": 5000},
    {"slug": "singapore", "filename": "loan-calculator-singapore.html", "title": "Loan Calculator Singapore", "country": "Singapore", "amount": 10000, "default_rate": 5, "default_term": 48, "loan_step": 1000},
    {"slug": "new-zealand", "filename": "loan-calculator-new-zealand.html", "title": "Loan Calculator New Zealand", "country": "New Zealand", "amount": 10000, "default_rate": 9, "default_term": 48, "loan_step": 1000},
    {"slug": "ireland", "filename": "loan-calculator-ireland.html", "title": "Loan Calculator Ireland", "country": "Ireland", "amount": 10000, "default_rate": 8, "default_term": 48, "loan_step": 1000},
]

# Full definition for special intent pages (not amount-driven)
SPECIAL_INTENT_PAGES = [
    {
        "filename": "auto-loan-calculator-24-months.html",
        "cluster": "car",
        "amount": 20000, "default_rate": 6.5, "default_term": 24, "loan_step": 100,
        "breadcrumb_parent": "car-loan-calculator.html", "breadcrumb_parent_label": "Car Loan Calculator",
        "breadcrumb_current": "24 Month Auto Loan",
        "title": "24 Month Auto Loan – Free Payment Calculator",
        "meta": "2-year car loan payment instantly. Free calculator. Shorter term, less interest. Compare with 36 and 48 months. No signup.",
        "h1": "24 Month Auto Loan Calculator — Free, Fast Estimate",
        "subtitle": "2-year term pre-filled—pay off faster, save on interest",
        "related": [
            ("car-loan-calculator.html", "Car Loan Calculator"),
            ("auto-loan-calculator-36-months.html", "36 Month Auto Loan"),
            ("auto-loan-calculator-48-months.html", "48 Month Auto Loan"),
            ("car-loan-20000-monthly-payment.html", "Car Loan for $20,000"),
            ("index.html", "Loan Calculator"),
        ],
    },
    {
        "filename": "auto-loan-calculator-36-months.html",
        "cluster": "car",
        "amount": 25000, "default_rate": 6.5, "default_term": 36, "loan_step": 100,
        "breadcrumb_parent": "car-loan-calculator.html", "breadcrumb_parent_label": "Car Loan Calculator",
        "breadcrumb_current": "36 Month Auto Loan",
        "title": "36 Month Auto Loan – Free Payment Calculator",
        "meta": "3-year car loan payment instantly. Free calculator. Compare with 48 and 60 months. No signup. Try now.",
        "h1": "36 Month Auto Loan Calculator — Free, Fast Estimate",
        "subtitle": "3-year term pre-filled—change amount or rate in seconds",
        "related": [
            ("car-loan-calculator.html", "Car Loan Calculator"),
            ("auto-loan-calculator-48-months.html", "48 Month Auto Loan"),
            ("auto-loan-calculator-60-months.html", "60 Month Auto Loan"),
            ("car-loan-20000-monthly-payment.html", "Car Loan for $20,000"),
            ("index.html", "Loan Calculator"),
        ],
    },
    {
        "filename": "auto-loan-calculator-72-months.html",
        "cluster": "car",
        "amount": 30000, "default_rate": 7, "default_term": 72, "loan_step": 100,
        "breadcrumb_parent": "car-loan-calculator.html", "breadcrumb_parent_label": "Car Loan Calculator",
        "breadcrumb_current": "72 Month Auto Loan",
        "title": "72 Month Auto Loan – Free Payment Calculator",
        "meta": "6-year car loan payment instantly. Free calculator. Lower payments, more interest. No signup. Compare now.",
        "h1": "72 Month Auto Loan Calculator — Free, Fast Estimate",
        "subtitle": "6-year term pre-filled—see payment vs total interest",
        "related": [
            ("car-loan-calculator.html", "Car Loan Calculator"),
            ("auto-loan-calculator-60-months.html", "60 Month Auto Loan"),
            ("auto-loan-calculator-48-months.html", "48 Month Auto Loan"),
            ("car-loan-30000-monthly-payment.html", "Car Loan for $30,000"),
            ("index.html", "Loan Calculator"),
        ],
    },
    {
        "filename": "used-car-loan-calculator.html",
        "cluster": "car",
        "amount": 18000, "default_rate": 8.5, "default_term": 60, "loan_step": 100,
        "breadcrumb_parent": "car-loan-calculator.html", "breadcrumb_parent_label": "Car Loan Calculator",
        "breadcrumb_current": "Used Car Loan Calculator",
        "title": "Used Car Loan Calculator – Free Payment Tool",
        "meta": "Used car loan payment in seconds. Higher rates typical. Free calculator. Compare before you buy. No signup.",
        "h1": "Used Car Loan Calculator — Free, Fast Estimate",
        "subtitle": "Typical used-car rates—adjust for your quote",
        "related": [
            ("car-loan-calculator.html", "Car Loan Calculator"),
            ("car-loan-with-trade-in-calculator.html", "Car Loan with Trade-In"),
            ("how-much-car-loan-can-i-afford.html", "How Much Car Loan Can I Afford"),
            ("auto-loan-calculator-60-months.html", "60 Month Auto Loan"),
            ("index.html", "Loan Calculator"),
        ],
    },
    {
        "filename": "debt-consolidation-loan-calculator.html",
        "cluster": "personal",
        "amount": 15000, "default_rate": 10, "default_term": 48, "loan_step": 500,
        "breadcrumb_parent": "personal-loan-calculator.html", "breadcrumb_parent_label": "Personal Loan Calculator",
        "breadcrumb_current": "Debt Consolidation Loan",
        "title": "Debt Consolidation Loan Calculator – Free Tool",
        "meta": "Debt consolidation loan payment in seconds. Compare single payment vs multiple debts. Free. No signup. Calculate now.",
        "h1": "Debt Consolidation Loan Calculator — Free Estimate",
        "subtitle": "See one payment to replace multiple debts",
        "related": [
            ("personal-loan-calculator.html", "Personal Loan Calculator"),
            ("index.html", "Loan Calculator"),
            ("loan-10000-monthly-payment.html", "Loan for $10,000"),
            ("loan-20000-monthly-payment.html", "Loan for $20,000"),
            ("car-loan-calculator.html", "Car Loan Calculator"),
        ],
    },
    {
        "filename": "home-improvement-loan-calculator.html",
        "cluster": "personal",
        "amount": 25000, "default_rate": 9, "default_term": 60, "loan_step": 1000,
        "breadcrumb_parent": "personal-loan-calculator.html", "breadcrumb_parent_label": "Personal Loan Calculator",
        "breadcrumb_current": "Home Improvement Loan",
        "title": "Home Improvement Loan Calculator – Free Tool",
        "meta": "Home improvement loan payment in seconds. Renovation funding. Free calculator. Compare terms. No signup. Calculate now.",
        "h1": "Home Improvement Loan Calculator — Free Estimate",
        "subtitle": "Typical renovation loan terms—adjust to your project",
        "related": [
            ("personal-loan-calculator.html", "Personal Loan Calculator"),
            ("mortgage-calculator.html", "Mortgage Calculator"),
            ("index.html", "Loan Calculator"),
            ("loan-20000-monthly-payment.html", "Loan for $20,000"),
            ("loan-calculator-with-down-payment.html", "Loan with Down Payment"),
        ],
    },
    {
        "filename": "mortgage-10-year-calculator.html",
        "cluster": "mortgage",
        "amount": 300000, "default_rate": 5.5, "default_term": 120, "loan_step": 10000,
        "breadcrumb_parent": "mortgage-calculator.html", "breadcrumb_parent_label": "Mortgage Calculator",
        "breadcrumb_current": "10-Year Mortgage",
        "title": "10-Year Mortgage Calculator – Free Payment Tool",
        "meta": "10-year mortgage payment instantly. Pay off fastest, lowest interest. Free calculator. Compare with 15- and 30-year. No signup.",
        "h1": "10-Year Mortgage Calculator — Free, Fast P&amp;I Estimate",
        "subtitle": "120-month term—highest payment, least total interest",
        "related": [
            ("mortgage-calculator.html", "Mortgage Calculator"),
            ("mortgage-15-year-calculator.html", "15-Year Mortgage"),
            ("mortgage-30-year-calculator.html", "30-Year Mortgage"),
            ("mortgage-300k-payment.html", "Mortgage for $300k"),
            ("index.html", "Loan Calculator"),
        ],
    },
    {
        "filename": "mortgage-20-year-calculator.html",
        "cluster": "mortgage",
        "amount": 250000, "default_rate": 6, "default_term": 240, "loan_step": 10000,
        "breadcrumb_parent": "mortgage-calculator.html", "breadcrumb_parent_label": "Mortgage Calculator",
        "breadcrumb_current": "20-Year Mortgage",
        "title": "20-Year Mortgage Calculator – Free Payment Tool",
        "meta": "20-year mortgage payment instantly. Balance of payment and interest savings. Free calculator. Compare 15 vs 20 vs 30 years. No signup.",
        "h1": "20-Year Mortgage Calculator — Free, Fast P&amp;I Estimate",
        "subtitle": "240-month term—between 15- and 30-year options",
        "related": [
            ("mortgage-calculator.html", "Mortgage Calculator"),
            ("mortgage-15-year-calculator.html", "15-Year Mortgage"),
            ("mortgage-30-year-calculator.html", "30-Year Mortgage"),
            ("mortgage-250k-payment.html", "Mortgage for $250k"),
            ("index.html", "Loan Calculator"),
        ],
    },
    {
        "filename": "mortgage-15-year-calculator.html",
        "cluster": "mortgage",
        "amount": 250000, "default_rate": 6, "default_term": 180, "loan_step": 10000,
        "breadcrumb_parent": "mortgage-calculator.html", "breadcrumb_parent_label": "Mortgage Calculator",
        "breadcrumb_current": "15-Year Mortgage",
        "title": "15-Year Mortgage Calculator – Free Payment Tool",
        "meta": "15-year mortgage payment instantly. Pay off faster, save interest. Free calculator. No signup. Compare with 30-year.",
        "h1": "15-Year Mortgage Calculator — Free, Fast P&amp;I Estimate",
        "subtitle": "180-month term—higher payment, less total interest",
        "related": [
            ("mortgage-calculator.html", "Mortgage Calculator"),
            ("mortgage-30-year-calculator.html", "30-Year Mortgage"),
            ("mortgage-200k-payment.html", "Mortgage for $200k"),
            ("mortgage-300k-payment.html", "Mortgage for $300k"),
            ("index.html", "Loan Calculator"),
        ],
    },
    # High-intent modifier pages (batch 1)
    {
        "filename": "auto-loan-refinance-calculator.html",
        "cluster": "car",
        "amount": 25000, "default_rate": 7, "default_term": 48, "loan_step": 100,
        "breadcrumb_parent": "car-loan-calculator.html", "breadcrumb_parent_label": "Car Loan Calculator",
        "breadcrumb_current": "Auto Loan Refinance Calculator",
        "title": "Auto Loan Refinance Calculator – See If You Save",
        "meta": "Should you refinance your car loan? Compare current payment vs lower rate. Free calculator. See savings in seconds. No signup.",
        "h1": "Auto Loan Refinance Calculator — Free Comparison",
        "subtitle": "Enter your loan, try a lower rate—see potential savings",
        "intro_override": "Should you refinance your car loan? Enter your current balance, rate, and remaining term below. Then try a lower rate to see how much you could save. Refinancing often makes sense if rates dropped or your credit improved.",
        "help_links": '<a href="car-loan-calculator.html">car loan calculator</a> · <a href="auto-loan-calculator-48-months.html">48 month</a> · <a href="auto-loan-calculator-60-months.html">60 month</a> · <a href="loan-calculator-with-extra-payments.html">payoff calculator</a>',
        "related": [
            ("car-loan-calculator.html", "Car Loan Calculator"),
            ("car-loan-25000-monthly-payment.html", "Car Loan for $25,000"),
            ("auto-loan-calculator-48-months.html", "48 Month Auto Loan"),
            ("loan-calculator-with-extra-payments.html", "Loan with Extra Payments"),
            ("index.html", "Loan Calculator"),
        ],
    },
    {
        "filename": "bad-credit-loan-calculator.html",
        "cluster": "personal",
        "amount": 10000, "default_rate": 15, "default_term": 48, "loan_step": 500,
        "breadcrumb_parent": "personal-loan-calculator.html", "breadcrumb_parent_label": "Personal Loan Calculator",
        "breadcrumb_current": "Bad Credit Loan Calculator",
        "title": "Bad Credit Loan Calculator – Estimate Your Payment",
        "meta": "Calculate loan payments with lower credit. Higher rates typical. Free calculator. See realistic numbers before you apply. No signup.",
        "h1": "Bad Credit Loan Calculator — Estimate Your Payment",
        "subtitle": "Rates for lower credit—adjust to your situation",
        "intro_override": "Rates for borrowers with lower credit are often 12–25% or higher. Use this calculator to see realistic monthly payments before you apply. Improving your score or shopping multiple lenders can help lower your rate.",
        "help_links": '<a href="personal-loan-calculator.html">personal loan calculator</a> · <a href="loan-10000-monthly-payment.html">$10k loan</a> · <a href="debt-consolidation-loan-calculator.html">debt consolidation</a> · <a href="index.html">loan calculator</a>',
        "related": [
            ("personal-loan-calculator.html", "Personal Loan Calculator"),
            ("loan-10000-monthly-payment.html", "Loan for $10,000"),
            ("debt-consolidation-loan-calculator.html", "Debt Consolidation Loan"),
            ("index.html", "Loan Calculator"),
            ("car-loan-calculator.html", "Car Loan Calculator"),
        ],
    },
]
