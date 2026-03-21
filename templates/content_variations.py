"""
Content variation pools for unique page generation.

UNIQUENESS RULES:
- Each page type has multiple intro, example, and FAQ variations
- Variations are selected by index (e.g. amount % len(variations)) to ensure
  different pages get different content while remaining deterministic
- Add new variations to expand uniqueness; avoid duplicate wording across pages
"""

# ---------------------------------------------------------------------------
# INTRO VARIATIONS - First paragraph under H1 (keyword-specific, benefit-led)
# ---------------------------------------------------------------------------

INTRO_LOAN_AMOUNT = [
    "Model a {amount} loan in seconds. Free online—no signup required. Start calculating your loan now.",
    "Get your {amount} monthly payment in seconds. Free calculator—adjust rate and term easily. No signup.",
    "Calculate a {amount} loan payment instantly. Free, simple, and fast. Enter your numbers above.",
]

INTRO_CAR_LOAN = [
    "See your {amount} car payment before you finance. Free, online, and fast—no signup. Start calculating your loan now.",
    "Estimate your {amount} auto loan payment in seconds. Free calculator—compare 48, 60, or 72 months. No signup.",
    "Run the numbers on a {amount} car loan instantly. Free and simple. Adjust rate and term to match your quote.",
]

INTRO_PERSONAL_LOAN = [
    "Calculate your {amount} personal loan payment in seconds. Free online—no signup. Start calculating now.",
    "See your {amount} personal loan monthly cost instantly. Free calculator—adjust rate and term. No signup.",
    "Estimate your {amount} personal loan payment before you apply. Free, fast, and simple.",
]

INTRO_MORTGAGE = [
    "See your {amount} mortgage payment in seconds. Free online—no signup. Start calculating your loan now.",
    "Estimate principal and interest on a {amount} mortgage instantly. Free calculator—30-year default. No signup.",
    "Calculate your {amount} home loan payment in seconds. Free tool—adjust rate and term to match your quote.",
]

INTRO_COUNTRY = [
    "Calculate loans for {country} in seconds. Free online—no signup. Start calculating your loan now.",
    "Run {country} loan numbers instantly. Free calculator—select your currency. No signup required.",
]

INTRO_SPECIAL_INTENT = [
    "See your payment in seconds. Free online—no signup. Compare terms before you finance.",
    "Calculate your payment instantly. Free and simple. Adjust amount, rate, or term above.",
]

# ---------------------------------------------------------------------------
# EXAMPLE SCENARIO VARIATIONS - "Real-world example" section
# ---------------------------------------------------------------------------

EXAMPLE_LOAN_AMOUNT = [
    "A {amount} loan at {rate}% for {term} months gives a monthly payment you can calculate above. Typical range: 2–4% of the loan per month depending on rate and term. Use the calculator with your quoted rate.",
    "For a {amount} loan, expect a monthly payment of roughly 2.5–3.5% of the principal at typical rates (8–12%) over 36–60 months. Enter your exact rate and term above for a precise figure.",
]

EXAMPLE_CAR_LOAN = [
    "At 6.5% for 60 months, a {amount} car loan typically runs about 2% of the principal per month. At 72 months the payment drops but total interest rises. Use the calculator with your quoted rate.",
    "Rates for {amount} auto loans often range 5–9% for new cars and 7–12% for used. A 7% rate over 60 months gives roughly a 2% monthly factor—enter your numbers above.",
]

EXAMPLE_MORTGAGE = [
    "At 6.5% for 30 years, expect about $6.32 per $1,000 borrowed—so roughly {approx_monthly} per month for {amount}. A half-point rate drop saves significantly over the life of the loan.",
    "A {amount} mortgage at 7% for 30 years typically runs about $6.65 per $1,000 per month in principal and interest. Use the calculator to compare 6%, 6.5%, and 7%.",
]

# ---------------------------------------------------------------------------
# FAQ VARIATIONS - Question/answer pairs (vary wording, keep intent)
# ---------------------------------------------------------------------------

FAQ_LOAN_AMOUNT = [
    ("What is the monthly payment on a {amount} loan at {rate}%?", "Use the calculator above with your exact rate and term. Rates vary by lender and credit. Typical terms are 36, 48, or 60 months."),
    ("How much would I pay per month for {amount}?", "Enter your quoted APR and term in the calculator. At 10% for 48 months, expect roughly 2.5% of the loan per month—adjust for your numbers."),
    ("Is a shorter or longer term better for {amount}?", "Shorter terms cost less total interest but higher monthly payments. Longer terms lower the payment but increase total cost. Compare both in the calculator."),
    ("Does this work for a {amount} car loan?", "Yes—the math is identical. For car-specific context, use our <a href=\"car-loan-calculator.html\">car loan calculator</a>."),
    ("How can I get a lower rate on a {amount} loan?", "Shop multiple lenders, improve your credit score, and consider a secured loan if applicable. See our <a href=\"personal-loan-calculator.html\">personal loan calculator</a> or <a href=\"index.html\">loan calculator</a> for comparisons."),
]

FAQ_CAR_LOAN = [
    ("What is a typical monthly payment for a {amount} car loan?", "At 6.5% for 60 months, use the calculator above for an exact figure. Rates vary—enter your quoted rate and term."),
    ("Should I choose 60 or 72 months for a {amount} loan?", "60 months usually costs less total interest. 72 months lowers the payment but adds interest. Compare both in the calculator."),
    ("Does this include taxes and fees?", "No. The calculator shows principal and interest only. Budget for taxes and fees separately."),
    ("Can I use this for a {amount} used car?", "Yes. The math is identical. Used-car rates are often higher—enter your quoted rate. See <a href=\"used-car-loan-calculator.html\">used car loan calculator</a>."),
    ("How do I compare dealer vs bank rates?", "Get quotes from both. Enter each rate in the calculator to see the difference. Our <a href=\"auto-loan-refinance-calculator.html\">refinance calculator</a> helps too."),
]

FAQ_PERSONAL_LOAN = [
    ("What is the monthly payment on a {amount} personal loan?", "Use the calculator with your quoted rate and term. At 10% for 48 months, expect roughly 2.5% of the loan per month—enter your numbers above."),
    ("Can I use this for a {amount} car loan?", "Yes—the math is identical. For car-specific pages, try our <a href=\"car-loan-calculator.html\">car loan calculator</a>."),
    ("How can I lower my monthly payment?", "Choose a longer term or improve your credit for a lower rate. A longer term increases total interest; a lower rate saves money overall."),
    ("Is a {amount} personal loan hard to get?", "Depends on credit and income. Online lenders and credit unions often have flexible criteria. Compare with our <a href=\"personal-loan-calculator.html\">personal loan calculator</a>."),
    ("What's a good rate for {amount}?", "Rates vary 6–36%. Excellent credit may get 6–10%; fair credit often 15–25%. Shop <a href=\"loan-calculator-usa.html\">USA</a> and <a href=\"loan-calculator-uk.html\">UK</a> calculators for regional context."),
]

FAQ_MORTGAGE = [
    ("What is the monthly payment on a {amount} mortgage at 7%?", "Use the calculator with your quoted rate. At 7% for 30 years, expect roughly $6.65 per $1,000 borrowed per month in P&amp;I."),
    ("How much do I pay in interest on a {amount} mortgage?", "At 6.5% over 30 years, you'll pay roughly 1.2× the principal in interest. A 15-year term cuts total interest significantly."),
    ("Does this include property tax and insurance?", "No. This shows principal and interest only. Your lender will typically escrow taxes and insurance."),
    ("15-year vs 30-year for {amount}?", "30-year lowers the payment; 15-year saves interest. Compare both in the calculator. See <a href=\"mortgage-15-year-calculator.html\">15-year</a> and <a href=\"mortgage-30-year-calculator.html\">30-year</a>."),
    ("How much house can I afford with {amount}?", "This shows the loan payment. Add taxes, insurance, and your down payment. Use our <a href=\"mortgage-calculator.html\">mortgage calculator</a> for any amount."),
]

FAQ_SPECIAL_INTENT = [
    ("Is this estimate accurate?", "This shows principal and interest. Your lender may round differently or charge fees. Use it for planning; confirm with your lender."),
    ("Can I compare different terms?", "Yes—change the term in months to see how 48 vs 60 vs 72 months affects your payment and total interest."),
]

FAQ_COUNTRY = [
    ("Does this work for {country} loans?", "Yes—the math is the same. Select the closest currency and enter your local amount and rate."),
    ("Where can I get a loan in {country}?", "Banks, credit unions, and licensed lenders offer personal, auto, and mortgage products. Compare rates before you apply."),
]

# ---------------------------------------------------------------------------
# HOW TO USE - Step-by-step instructions (vary wording per page type)
# ---------------------------------------------------------------------------

HOW_TO_LOAN_AMOUNT = [
    """<ol>
        <li><strong>Select your currency</strong> — USD is pre-set; change if needed.</li>
        <li><strong>Loan amount</strong> — Pre-filled at {amount}; adjust for a different amount.</li>
        <li><strong>Enter the interest rate</strong> — Use the annual rate (APR) your lender quoted.</li>
        <li><strong>Enter the term in months</strong> — 36, 48, or 60 are common for {amount} loans.</li>
        <li><strong>Click Calculate</strong> — See your monthly payment, total repayment, and total interest.</li>
      </ol>""",
    """<ol>
        <li><strong>Currency</strong> — Defaults to USD; switch to EUR, GBP, or others if needed.</li>
        <li><strong>Amount</strong> — Pre-filled with {amount}; change the field for a different loan size.</li>
        <li><strong>Interest rate</strong> — Enter the annual APR from your quote.</li>
        <li><strong>Term (months)</strong> — Common terms: 24, 36, 48, 60, or 72 months.</li>
        <li><strong>Calculate</strong> — Instant monthly payment, total payment, and total interest.</li>
      </ol>""",
]

HOW_TO_CAR_LOAN = [
    """<ol>
        <li><strong>Loan amount</strong> — Pre-filled at {amount}; adjust for your vehicle price minus down payment.</li>
        <li><strong>Interest rate</strong> — Enter the rate from your dealer or lender.</li>
        <li><strong>Term in months</strong> — 48, 60, or 72 months are common for car loans.</li>
        <li><strong>Click Calculate</strong> — See monthly payment and total interest.</li>
      </ol>""",
]

HOW_TO_PERSONAL_LOAN = [
    """<ol>
        <li><strong>Loan amount</strong> — Pre-filled at {amount}; adjust if needed.</li>
        <li><strong>Enter the interest rate</strong> — Use the APR your lender quoted.</li>
        <li><strong>Enter the term in months</strong> — 24, 36, 48, or 60 are common for personal loans.</li>
        <li><strong>Click Calculate</strong> — See your monthly payment and total interest.</li>
      </ol>""",
]

HOW_TO_MORTGAGE = [
    """<ol>
        <li><strong>Loan amount</strong> — Pre-filled at {amount}; enter your principal after down payment.</li>
        <li><strong>Interest rate</strong> — Use your quoted mortgage rate.</li>
        <li><strong>Term in months</strong> — 360 for 30-year; 180 for 15-year.</li>
        <li><strong>Click Calculate</strong> — See principal and interest (P&I) only; budget taxes and insurance separately.</li>
      </ol>""",
]

HOW_TO_SPECIAL_INTENT = [
    """<ol>
        <li><strong>Enter the loan amount</strong> — The principal you plan to borrow.</li>
        <li><strong>Enter the interest rate</strong> — Use the annual rate your lender quoted.</li>
        <li><strong>Enter the term in months</strong> — Pre-filled for this loan type; adjust if needed.</li>
        <li><strong>Click Calculate</strong> — See your monthly payment and total interest.</li>
      </ol>""",
]

HOW_TO_COUNTRY = [
    """<ol>
        <li><strong>Select currency</strong> — Choose the currency that matches your location (USD, EUR, GBP, etc.).</li>
        <li><strong>Enter the loan amount</strong> — The principal in your local currency.</li>
        <li><strong>Enter the interest rate</strong> — The annual rate from your {country} lender.</li>
        <li><strong>Enter the term in months</strong> — Common terms vary by country and product.</li>
        <li><strong>Click Calculate</strong> — See your monthly payment and total interest.</li>
      </ol>""",
]

# ---------------------------------------------------------------------------
# WHAT AFFECTS - Bullet list of factors (for loan amount, car, personal, mortgage)
# ---------------------------------------------------------------------------

WHAT_AFFECTS_LOAN_AMOUNT = """<ul>
        <li><strong>Interest rate</strong> — Rates for personal loans often range from 6% to 36% depending on credit. A lower rate reduces both the payment and total interest.</li>
        <li><strong>Loan term</strong> — Shorter terms mean higher monthly payments but less total interest. Longer terms spread the cost but cost more overall.</li>
        <li><strong>Origination fees</strong> — If your lender charges fees and finances them, add the fee to the loan amount for a more accurate estimate.</li>
      </ul>
      <p>Compare with our <a href="personal-loan-calculator.html">personal loan calculator</a>, <a href="car-loan-calculator.html">car loan calculator</a>, or <a href="loan-calculator-usa.html">USA loan calculator</a> for other amounts and contexts.</p>"""

WHAT_AFFECTS_CAR_LOAN = """<p>A {amount} car loan is a common size for used vehicles or a new car with a down payment. Your monthly payment depends on the interest rate and loan term. Rates vary by lender and credit score. New-car borrowers often see 5–7%; used cars and lower credit can mean 8–12%. Use the calculator above to compare 48, 60, and 72 months.</p>
      <p>Many buyers overlook total interest. Run the numbers before you sign—the same car can cost hundreds more or less depending on rate and term. Our <a href="car-loan-calculator.html">car loan calculator</a> works for any amount.</p>"""

WHAT_AFFECTS_PERSONAL_LOAN = """<ul>
        <li><strong>Interest rate</strong> — Personal loan rates typically range from 6% to 36% depending on credit.</li>
        <li><strong>Loan term</strong> — Shorter terms save interest; longer terms lower the monthly payment.</li>
        <li><strong>Credit score</strong> — Better credit usually means lower rates. Shop multiple lenders.</li>
      </ul>"""

WHAT_AFFECTS_MORTGAGE = """<p>This calculator shows principal and interest only. Your real monthly housing cost usually includes property taxes, insurance, and sometimes PMI. Budget for those separately. See our <a href="mortgage-calculator.html">mortgage calculator</a> for any amount.</p>"""

WHAT_AFFECTS_SPECIAL_INTENT = """<ul>
        <li><strong>Interest rate</strong> — Your rate depends on credit, lender, and loan type. Shop multiple offers.</li>
        <li><strong>Loan term</strong> — Shorter terms mean higher payments but less total interest. Longer terms spread the cost.</li>
        <li><strong>Loan amount</strong> — The principal directly affects both monthly payment and total interest.</li>
      </ul>"""

WHAT_AFFECTS_COUNTRY = """<p>Loan structures and rates vary by country. This calculator uses standard amortization—equal monthly payments of principal and interest. Check with local lenders for product-specific terms. Use our <a href="loan-calculator-usa.html">USA</a>, <a href="loan-calculator-uk.html">UK</a>, or <a href="loan-calculator-australia.html">Australia</a> calculators for region-specific pages.</p>"""


def pick_variation(pool, index):
    """Select a variation by index for deterministic uniqueness."""
    return pool[index % len(pool)]


def pick_faqs(pool, count, index, **fmt_kwargs):
    """Pick up to `count` FAQ items from pool, formatted with kwargs."""
    items = []
    for i in range(min(count, len(pool))):
        q, a = pool[(index + i) % len(pool)]
        try:
            q = q.format(**fmt_kwargs)
            a = a.format(**fmt_kwargs)
        except KeyError:
            pass
        items.append((q, a))
    return items


def format_faqs_html(faq_items):
    """Render FAQ items as <dl class='faq-list'> HTML."""
    lines = []
    for q, a in faq_items:
        lines.append(f"        <dt>{q}</dt>")
        lines.append(f"        <dd>{a}</dd>")
    return '<dl class="faq-list">\n' + "\n".join(lines) + "\n      </dl>"
