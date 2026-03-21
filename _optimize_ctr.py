#!/usr/bin/env python3
"""CTR/SEO pass for LoanWise HTML. Run: python3 _optimize_ctr.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

INTRO_CTA = (
    "Get a clear payment in seconds—free, online, and simple. No signup required. "
    "Start calculating your loan now using the form below."
)


def money(n: int) -> str:
    return f"${n:,}"


def esc_attr(s: str) -> str:
    """Escape for HTML attribute / title text (avoid double-encoding entities)."""
    s = s.replace("&amp;", "&")  # normalize if re-running
    s = s.replace("&", "&amp;")
    return s.replace('"', "&quot;")


def set_head(text: str, title: str, desc: str) -> str:
    title_e = esc_attr(title)
    desc_e = esc_attr(desc)
    text = re.sub(r"<title>.*?</title>", f"<title>{title_e}</title>", text, count=1)
    text = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{desc_e}">',
        text,
        count=1,
    )
    text = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{title_e}">',
        text,
        count=1,
    )
    text = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{desc_e}">',
        text,
        count=1,
    )
    return text


def insert_intro_compact_header(text: str, intro: str) -> str:
    if "intro-lead" in text:
        return text
    pat = r'(</p>\s*)(</header>\s*\n\s*<main class="calculator">)'
    rep = r'\1      <p class="intro-lead">' + intro + r"</p>\n    \2"
    new, n = re.subn(pat, rep, text, count=1)
    if n:
        return new
    pat2 = r"(<p class=\"subtitle subtitle--benefit\">[^<]*</p>\s*)</header>"
    rep2 = r'\1      <p class="intro-lead">' + intro + r"</p>\n    </header>"
    new2, n2 = re.subn(pat2, rep2, text, count=1)
    return new2 if n2 else text


def replace_h1_subtitle(text: str, h1: str, subtitle: str) -> str:
    h1_e = esc_attr(h1)
    sub_e = esc_attr(subtitle)
    text = re.sub(r"<h1[^>]*>.*?</h1>", f"<h1>{h1_e}</h1>", text, count=1)
    text = re.sub(
        r'<p class="subtitle subtitle--benefit">.*?</p>',
        f'<p class="subtitle subtitle--benefit">{sub_e}</p>',
        text,
        count=1,
    )
    return text


def replace_page_title_h1(text: str, h1_inner: str) -> str:
    return re.sub(
        r'<h1 class="page-title">.*?</h1>',
        f'<h1 class="page-title">{esc_attr(h1_inner)}</h1>',
        text,
        count=1,
    )


def insert_first_p_content_page(text: str, first_p: str) -> str:
    if re.search(
        r"<main class=\"page-content\">[\s\S]{0,4000}?<p class=\"intro-lead\">",
        text,
    ):
        return text
    pat = r'(<main class="page-content">\s*<h1 class="page-title">.*?</h1>\s*<section class="content-section">\s*)'
    m = re.search(pat, text, re.DOTALL)
    if not m:
        return text
    insert = (
        m.group(1)
        + f'        <p class="intro-lead">{esc_attr(first_p)}</p>\n\n        '
    )
    return text.replace(m.group(1), insert, 1)


SPECIFIC = {
    "index.html": {
        "title": "Loan Calculator — Monthly Payment Estimate (Free, Online & Fast, 2026) | LoanWise",
        "desc": "Calculate your loan payment instantly—free online calculator, simple and fast. No signup required. See monthly payment, total interest, and 9 currencies in one click. LoanWise 2026.",
        "h1": "Loan Calculator — Your Payment in Seconds (Free & Online)",
        "subtitle": "9 currencies · monthly payment + total interest—fast, simple, no signup",
        "intro": INTRO_CTA,
    },
    "car-loan-calculator.html": {
        "title": "Car Loan Calculator — Monthly Payment (Free, Online & Fast, 2026) | LoanWise",
        "desc": "Car loan calculator online: see your monthly payment instantly. Free, fast, simple—no signup. Compare rate and term before the dealer. LoanWise 2026.",
        "h1": "Car Loan Calculator — Payment Estimate Free & Fast",
        "subtitle": "3 quick fields → monthly payment + total interest before you buy",
        "intro": "Plan your car budget with confidence. This free online tool is fast and simple—no signup required. Start calculating your loan now.",
    },
    "auto-loan-calculator.html": {
        "title": "Auto Loan Calculator — Monthly Payment (Free, Online & Fast, 2026) | LoanWise",
        "desc": "Auto loan payment calculator: instant results, free online. Simple inputs—no signup. See payment and total interest in seconds. LoanWise 2026.",
        "h1": "Auto Loan Calculator — See Your Payment Free & Online",
        "subtitle": "Same math as banks—enter amount, APR, and term for a fast estimate",
        "intro": "Get a clear auto payment in seconds. Free, online, and simple—no signup. Start calculating your loan now.",
    },
    "personal-loan-calculator.html": {
        "title": "Personal Loan Calculator — Monthly Payment (Free, Online & Fast, 2026) | LoanWise",
        "desc": "Personal loan calculator: calculate your payment instantly online. Free, fast, simple—no signup. See monthly cost and total interest before you apply. LoanWise 2026.",
        "h1": "Personal Loan Calculator — Fast, Free Payment Estimate",
        "subtitle": "Unsecured loan math—adjust rate and term to match your offer",
        "intro": "Know what you’ll owe each month. Free online calculator—no signup. Start calculating your loan now.",
    },
    "business-loan-calculator.html": {
        "title": "Business Loan Calculator — Monthly Payment (Free, Online & Fast, 2026) | LoanWise",
        "desc": "Business loan payment calculator online: instant, free estimates. Simple and fast—no signup. Model cash flow before you sign. LoanWise 2026.",
        "h1": "Business Loan Calculator — Simple, Fast Payment Planning",
        "subtitle": "Term-loan style payments—enter amount, rate, and months",
        "intro": "Stress-test your business payment in seconds. Free and online—no signup required. Start calculating your loan now.",
    },
    "mortgage-calculator.html": {
        "title": "Mortgage Calculator — Monthly P&I Payment (Free, Online & Fast, 2026) | LoanWise",
        "desc": "Mortgage calculator online: principal & interest in seconds. Free, simple, fast—no signup. Calculate your payment instantly and compare rates. LoanWise 2026.",
        "h1": "Mortgage Calculator — P&I Payment, Free & Fast",
        "subtitle": "360 months = 30 years · P&I only—add taxes/insurance in your budget",
        "intro": "See your mortgage payment instantly. Free online tool—simple and fast, no signup. Start calculating your loan now.",
    },
    "interest-calculator.html": {
        "title": "Interest Calculator — Loan & Simple Interest (Free, Online & Fast, 2026) | LoanWise",
        "desc": "Free online interest calculator: amortizing loan plus simple I = P×R×T. Fast, simple—no signup. Calculate interest and payments instantly. LoanWise 2026.",
        "h1": "Interest Calculator — Loan + Simple Interest, Free Online",
        "subtitle": "Loan tool below; scroll for simple interest—both fast and free",
        "intro": "Run loan or simple-interest numbers in seconds. Free, online, no signup—start calculating now.",
    },
    "simple-interest-calculator.html": {
        "title": "Simple Interest Calculator — I = P×R×T (Free, Online & Fast, 2026) | LoanWise",
        "desc": "Simple interest calculator online: free, fast formula math plus compound compare. No signup—calculate instantly. LoanWise 2026.",
        "h1": "Simple Interest Calculator — Free, Fast & Easy Online",
        "subtitle": "I = P×R×T in one click—optional compound comparison",
        "intro": "Solve simple interest in seconds. Free online calculator—no signup. Start calculating now.",
    },
    "how-much-car-loan-can-i-afford.html": {
        "title": "How Much Car Loan Can I Afford? — Free Online Calculator (Fast, 2026) | LoanWise",
        "desc": "See how much car loan you can afford—instant, free online. Simple payment math—no signup. Adjust income, debt, and rate fast. LoanWise 2026.",
        "h1": "How Much Car Loan Can I Afford? — Free & Fast",
        "subtitle": "Payment-first check—tweak income, debts, and rate in seconds",
        "intro": "Get a reality check on car payments in seconds. Free, online, simple—no signup. Start calculating now.",
    },
    "mortgage-30-year-calculator.html": {
        "title": "30-Year Mortgage Calculator — Monthly Payment (Free, Online & Fast, 2026) | LoanWise",
        "desc": "30-year mortgage payment calculator: free, online, instant P&I. Simple and fast—no signup. Calculate your payment in seconds. LoanWise 2026.",
        "h1": "30-Year Mortgage Calculator — Free, Fast Payment Estimate",
        "subtitle": "30-year term pre-set—change rate or loan size anytime",
        "intro": "Model a 30-year payment instantly. Free online—no signup. Start calculating your mortgage now.",
    },
    "loan-calculator-with-interest-breakdown.html": {
        "title": "Loan Calculator with Interest Breakdown — Free Online (Fast, 2026) | LoanWise",
        "desc": "Loan calculator with year-by-year interest breakdown—free online. Fast, simple—no signup. See principal vs. interest each year instantly. LoanWise 2026.",
        "h1": "Loan Calculator with Interest Breakdown — Free & Fast",
        "subtitle": "Full amortization schedule—see every year’s split in one run",
        "intro": "Understand where your money goes—free, online, instant. No signup. Start calculating your loan now.",
    },
    "car-loan-monthly-payment-calculator.html": {
        "title": "Car Loan Monthly Payment Calculator — Free Online (Fast & Simple, 2026) | LoanWise",
        "desc": "Car loan monthly payment calculator: instant results, free online. Simple and fast—no signup. Dealer-ready numbers in seconds. LoanWise 2026.",
        "h1": "Car Loan Monthly Payment — Free, Fast Estimate Online",
        "subtitle": "3 fields → payment + total cost before you negotiate",
        "intro": "Walk into the dealership prepared. Free online tool—no signup. Start calculating your car loan now.",
    },
    "simple-loan-payment-example.html": {
        "title": "Simple Loan Payment Example — $10k Walkthrough (Free Online, 2026) | LoanWise",
        "desc": "Simple loan payment example with live calculator—free online. Learn the math fast; no signup. Calculate your own scenario instantly. LoanWise 2026.",
        "h1": "Loan Payment Example — Free, Simple Step-by-Step",
        "subtitle": "$10,000 at 6% for 36 months explained + try your numbers",
        "intro": "See how a real payment breaks down—free, online, easy. Start calculating your loan now.",
    },
    "loan-calculator-usa.html": {
        "title": "USA Loan Calculator — USD Payment (Free, Online & Fast, 2026) | LoanWise",
        "desc": "USA loan calculator online: instant USD monthly payments. Free, simple, fast—no signup. Personal, auto, or mortgage-style terms in seconds. LoanWise 2026.",
        "h1": "USA Loan Calculator — Free, Fast USD Payments Online",
        "subtitle": "USD default · typical US terms for personal, auto, and home-style loans",
        "intro": "Run US-dollar loan numbers instantly. Free online—no signup. Start calculating your loan now.",
    },
    "loan-calculator-uk.html": {
        "title": "UK Loan Calculator — GBP Payment (Free, Online & Fast, 2026) | LoanWise",
        "desc": "UK loan calculator online: fast GBP payment estimates. Free, simple—no signup. Calculate your loan instantly in pounds. LoanWise 2026.",
        "h1": "UK Loan Calculator — Free, Fast Online (GBP)",
        "subtitle": "GBP default · quick monthly payment + total interest",
        "intro": "See your UK loan payment in seconds. Free online calculator—no signup. Start calculating now.",
    },
    "loan-calculator-canada.html": {
        "title": "Canada Loan Calculator — CAD Payment (Free, Online & Fast, 2026) | LoanWise",
        "desc": "Canada loan calculator: instant CAD monthly payments online. Free, fast, simple—no signup. LoanWise 2026.",
        "h1": "Canada Loan Calculator — Free, Fast CAD Estimate",
        "subtitle": "CAD default · simple payment math for any term",
        "intro": "Plan loans in Canadian dollars—instantly. Free online—no signup. Start calculating your loan now.",
    },
    "loan-calculator-uae.html": {
        "title": "UAE Loan Calculator — AED Payment (Free, Online & Fast, 2026) | LoanWise",
        "desc": "UAE loan calculator online: fast AED payment estimates. Free, simple—no signup. Calculate instantly. LoanWise 2026.",
        "h1": "UAE Loan Calculator — Free, Fast Online (AED)",
        "subtitle": "AED default · monthly payment + total interest in seconds",
        "intro": "Model dirham loans in seconds. Free online—no signup. Start calculating your loan now.",
    },
    "loan-calculator-morocco.html": {
        "title": "Morocco Loan Calculator — MAD Payment (Free, Online & Fast, 2026) | LoanWise",
        "desc": "Morocco loan calculator: instant MAD monthly payments online. Free, fast, simple—no signup. LoanWise 2026.",
        "h1": "Morocco Loan Calculator — Free, Fast MAD Estimate",
        "subtitle": "MAD default · simple, clear payment results",
        "intro": "Calculate in Moroccan dirhams—instantly. Free online—no signup. Start calculating your loan now.",
    },
    "loan-calculator-australia.html": {
        "title": "Australia Loan Calculator — AUD Payment (Free, Online & Fast, 2026) | LoanWise",
        "desc": "Australia loan calculator online: fast AUD payment estimates. Free, simple—no signup. Calculate your loan instantly. LoanWise 2026.",
        "h1": "Australia Loan Calculator — Free, Fast Online (AUD)",
        "subtitle": "AUD default · quick monthly payment + total interest",
        "intro": "See your Australian dollar payment in seconds. Free online—no signup. Start calculating now.",
    },
    "about.html": {
        "title": "About LoanWise — Free Online Calculators (Simple & Fast, 2026) | LoanWise",
        "desc": "About LoanWise: free online loan, car, and mortgage calculators—fast and simple. No signup. Built for clear payment estimates in 2026.",
        "page_h1": "About LoanWise — Free, Fast Payment Tools Online",
        "first_p": "LoanWise gives you clear loan estimates in seconds—free, online, and simple. No signup required. Start calculating on the home page or pick a specialized calculator below.",
    },
    "contact.html": {
        "title": "Contact LoanWise — Calculator Help (Free Support, Online, 2026) | LoanWise",
        "desc": "Contact LoanWise online—questions about our free calculators welcome. Simple, fast replies when we can. No signup to use the tools. LoanWise 2026.",
        "page_h1": "Contact LoanWise — We’re Here to Help",
        "first_p": "Have a question about our free online calculators? Send a message—we read everything. No signup is ever required to use LoanWise. Use the form below when you’re ready.",
    },
    "terms.html": {
        "title": "Terms of Use — LoanWise (Free Tools, Online, 2026) | LoanWise",
        "desc": "LoanWise terms of use: free online calculators for estimates only—not lending advice. Simple rules; always verify with your lender. LoanWise 2026.",
        "page_h1": "Terms of Use — Simple Rules for Free Online Tools",
        "first_p": "LoanWise offers free, online calculators for planning only. Read these simple terms, then use our tools with confidence—no signup required.",
    },
    "privacy-policy.html": {
        "title": "Privacy Policy — LoanWise (Free Online Calculators, 2026) | LoanWise",
        "desc": "LoanWise privacy policy in plain English: how our free online site may use cookies and analytics. Simple, transparent—no account required. LoanWise 2026.",
        "page_h1": "Privacy Policy — Clear & Simple (2026)",
        "first_p": "We keep this policy straightforward. LoanWise is a free online calculator site—no signup—and here’s how visits may be measured.",
    },
}


def long_tail_payload(name: str):
    m = re.match(r"car-loan-(\d+)-monthly-payment\.html$", name)
    if m:
        a = int(m.group(1))
        lab = money(a)
        kw = f"Car Loan {lab} Monthly Payment"
        return {
            "title": f"{kw} — Free Online Calculator (Fast & Simple, 2026) | LoanWise",
            "desc": f"{kw}: calculate instantly—free online, no signup. Simple tool for monthly payment and total interest. Compare terms fast. LoanWise 2026.",
            "h1": f"{kw} — Free, Fast Estimate",
            "subtitle": f"Pre-filled for {lab}—change rate or term in seconds",
            "intro": f"See your {lab} car payment before you finance. Free, online, and fast—no signup. Start calculating your loan now.",
        }
    m = re.match(r"loan-(\d+)-monthly-payment\.html$", name)
    if m:
        a = int(m.group(1))
        lab = money(a)
        kw = f"Loan {lab} Monthly Payment"
        return {
            "title": f"{kw} — Free Online Calculator (Fast & Simple, 2026) | LoanWise",
            "desc": f"{kw}: instant results—free online calculator, no signup. Simple payment and interest totals. LoanWise 2026.",
            "h1": f"{kw} — Fast, Free Online",
            "subtitle": f"Pre-filled for {lab}—adjust rate and term easily",
            "intro": f"Model a {lab} loan in seconds. Free online—no signup required. Start calculating your loan now.",
        }
    m = re.match(r"personal-loan-(\d+)-payment\.html$", name)
    if m:
        a = int(m.group(1))
        lab = money(a)
        kw = f"Personal Loan {lab} Payment"
        return {
            "title": f"{kw} — Free Online Calculator (Fast & Simple, 2026) | LoanWise",
            "desc": f"{kw}: calculate your monthly cost instantly. Free, online, simple—no signup. See payment and interest before you apply. LoanWise 2026.",
            "h1": f"{kw} — Free & Fast Estimate",
            "subtitle": f"Pre-filled for {lab} unsecured—tune rate and term",
            "intro": f"Plan a {lab} personal loan payment in seconds. Free online—no signup. Start calculating now.",
        }
    m = re.match(r"business-loan-(\d+)-payment\.html$", name)
    if m:
        a = int(m.group(1))
        lab = money(a)
        kw = f"Business Loan {lab} Payment"
        return {
            "title": f"{kw} — Free Online Calculator (Fast & Simple, 2026) | LoanWise",
            "desc": f"{kw}: instant monthly estimate—free online, no signup. Simple cash-flow planning for your business. LoanWise 2026.",
            "h1": f"{kw} — Fast, Free Online",
            "subtitle": f"Pre-filled for {lab}—adjust rate and term for your term loan",
            "intro": f"Stress-test a {lab} business payment in seconds. Free online—no signup. Start calculating your loan now.",
        }
    m = re.match(r"mortgage-(\d+)k-payment\.html$", name)
    if m:
        k = int(m.group(1))
        lab = money(k * 1000)
        kw = f"Mortgage {lab} Payment"
        return {
            "title": f"{kw} — Free Online P&I Calculator (Fast & Simple, 2026) | LoanWise",
            "desc": f"{kw}: principal & interest instantly—free online, no signup. Simple 30-year default; change rate anytime. LoanWise 2026.",
            "h1": f"{kw} — Free, Fast P&I Estimate",
            "subtitle": "30-year term pre-filled—adjust rate to match your quote",
            "intro": f"See your {lab} mortgage payment in seconds. Free online—no signup. Start calculating your loan now.",
        }
    return None


def process_file(path: Path) -> bool:
    name = path.name
    text = path.read_text(encoding="utf-8")
    orig = text

    if name in SPECIFIC:
        d = SPECIFIC[name]
        text = set_head(text, d["title"], d["desc"])
        if d.get("h1") and d.get("subtitle"):
            text = replace_h1_subtitle(text, d["h1"], d["subtitle"])
            text = insert_intro_compact_header(text, d.get("intro", INTRO_CTA))
        if d.get("page_h1"):
            text = replace_page_title_h1(text, d["page_h1"])
        if d.get("first_p"):
            text = insert_first_p_content_page(text, d["first_p"])
    else:
        payload = long_tail_payload(name)
        if payload:
            text = set_head(text, payload["title"], payload["desc"])
            text = replace_h1_subtitle(text, payload["h1"], payload["subtitle"])
            text = insert_intro_compact_header(text, payload["intro"])

    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    n = 0
    for path in sorted(ROOT.glob("*.html")):
        if path.name.startswith("_"):
            continue
        if process_file(path):
            n += 1
    print(f"Updated {n} files.")


if __name__ == "__main__":
    main()
