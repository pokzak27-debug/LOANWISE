"""
Internal linking configuration for LoanWise.

Provides cluster assignment, breadcrumbs, related links, and silo links
for all page types. Used by apply_internal_links.py and generate_calculator_pages.py.

Cluster structure:
- general: index, loan-N-monthly-payment, loan tools
- car: car-loan-calculator, car-loan-N, auto-loan-*, used-car, trade-in, afford
- personal: personal-loan-calculator, personal-loan-N, debt-consolidation, home-improvement
- mortgage: mortgage-calculator, mortgage-Nk, mortgage-15-year, mortgage-30-year
- country: loan-calculator-{country}
- business: business-loan-calculator, business-loan-N
- utility: about, contact, terms, privacy, sitemap
"""

import re
from typing import List, Tuple, Optional

# ---------------------------------------------------------------------------
# Page classification patterns (filename -> cluster, parent, label)
# ---------------------------------------------------------------------------

def classify_page(fname: str, all_files: set) -> dict:
    """
    Classify a page by filename. Returns:
    - cluster: general | car | personal | mortgage | country | business | utility
    - parent: href of parent page
    - parent_label: label for breadcrumb
    - current_label: label for current page
    - amount or slug: extracted value for related-link logic
    """
    if fname == "index.html":
        return {"cluster": "general", "parent": None, "parent_label": None, "current_label": "Home"}

    # Utility pages
    if fname in ("about.html", "contact.html", "sitemap.html", "terms.html", "privacy-policy.html"):
        return {"cluster": "utility", "parent": "index.html", "parent_label": "Home", "current_label": _util_label(fname)}

    # General loan amount: loan-N-monthly-payment.html
    m = re.match(r"loan-(\d+)-monthly-payment\.html", fname)
    if m:
        amt = int(m.group(1))
        return {"cluster": "general", "parent": "index.html", "parent_label": "Loan Calculator", "current_label": f"Loan for ${amt:,}", "amount": amt}

    # General loan tools
    GENERAL_TOOLS = {
        "loan-calculator-with-down-payment.html": "Loan with Down Payment",
        "loan-calculator-with-extra-payments.html": "Loan with Extra Payments",
        "loan-calculator-with-interest-breakdown.html": "Loan with Interest Breakdown",
        "loan-calculator-comparison.html": "Loan Calculator Comparison",
        "simple-loan-payment-example.html": "Simple Loan Example",
        "how-to-calculate-loan-monthly-payment.html": "How to Calculate Loan Payment",
        "interest-calculator.html": "Interest Calculator",
        "simple-interest-calculator.html": "Simple Interest Calculator",
    }
    if fname in GENERAL_TOOLS:
        return {"cluster": "general", "parent": "index.html", "parent_label": "Loan Calculator", "current_label": GENERAL_TOOLS[fname]}

    # Car loan parent
    if fname == "car-loan-calculator.html":
        return {"cluster": "car", "parent": "index.html", "parent_label": "Home", "current_label": "Car Loan Calculator"}

    # Car loan amount: car-loan-N-monthly-payment.html
    m = re.match(r"car-loan-(\d+)-monthly-payment\.html", fname)
    if m:
        amt = int(m.group(1))
        return {"cluster": "car", "parent": "car-loan-calculator.html", "parent_label": "Car Loan Calculator", "current_label": f"Car Loan for ${amt:,}", "amount": amt}

    # Car special pages
    CAR_SPECIAL = {
        "auto-loan-calculator.html": ("car-loan-calculator.html", "Car Loan Calculator", "Auto Loan Calculator"),
        "auto-loan-calculator-24-months.html": ("car-loan-calculator.html", "Car Loan Calculator", "24 Month Auto Loan"),
        "auto-loan-calculator-36-months.html": ("car-loan-calculator.html", "Car Loan Calculator", "36 Month Auto Loan"),
        "auto-loan-calculator-48-months.html": ("car-loan-calculator.html", "Car Loan Calculator", "48 Month Auto Loan"),
        "auto-loan-calculator-60-months.html": ("car-loan-calculator.html", "Car Loan Calculator", "60 Month Auto Loan"),
        "auto-loan-calculator-72-months.html": ("car-loan-calculator.html", "Car Loan Calculator", "72 Month Auto Loan"),
        "used-car-loan-calculator.html": ("car-loan-calculator.html", "Car Loan Calculator", "Used Car Loan Calculator"),
        "car-loan-with-trade-in-calculator.html": ("car-loan-calculator.html", "Car Loan Calculator", "Car Loan with Trade-In"),
        "how-much-car-loan-can-i-afford.html": ("car-loan-calculator.html", "Car Loan Calculator", "How Much Car Loan Can I Afford"),
        "car-loan-monthly-payment-calculator.html": ("car-loan-calculator.html", "Car Loan Calculator", "Car Loan Monthly Payment"),
        "auto-loan-refinance-calculator.html": ("car-loan-calculator.html", "Car Loan Calculator", "Auto Loan Refinance Calculator"),
    }
    if fname in CAR_SPECIAL:
        p, pl, cl = CAR_SPECIAL[fname]
        return {"cluster": "car", "parent": p, "parent_label": pl, "current_label": cl}

    # Personal loan parent
    if fname == "personal-loan-calculator.html":
        return {"cluster": "personal", "parent": "index.html", "parent_label": "Home", "current_label": "Personal Loan Calculator"}

    # Personal loan amount: personal-loan-N-payment.html
    m = re.match(r"personal-loan-(\d+)-payment\.html", fname)
    if m:
        amt = int(m.group(1))
        return {"cluster": "personal", "parent": "personal-loan-calculator.html", "parent_label": "Personal Loan Calculator", "current_label": f"Personal Loan for ${amt:,}", "amount": amt}

    # Personal special
    PERSONAL_SPECIAL = {
        "debt-consolidation-loan-calculator.html": "Debt Consolidation Loan",
        "home-improvement-loan-calculator.html": "Home Improvement Loan",
        "bad-credit-loan-calculator.html": "Bad Credit Loan Calculator",
    }
    if fname in PERSONAL_SPECIAL:
        return {"cluster": "personal", "parent": "personal-loan-calculator.html", "parent_label": "Personal Loan Calculator", "current_label": PERSONAL_SPECIAL[fname]}

    # Mortgage parent
    if fname == "mortgage-calculator.html":
        return {"cluster": "mortgage", "parent": "index.html", "parent_label": "Home", "current_label": "Mortgage Calculator"}

    # Mortgage amount: mortgage-Nk-payment.html
    m = re.match(r"mortgage-(\d+)k-payment\.html", fname)
    if m:
        k = m.group(1)
        return {"cluster": "mortgage", "parent": "mortgage-calculator.html", "parent_label": "Mortgage Calculator", "current_label": f"Mortgage for ${int(k):,}k", "amount_k": int(k)}

    # Mortgage special
    MORTGAGE_SPECIAL = {
        "mortgage-30-year-calculator.html": "30-Year Mortgage",
        "mortgage-20-year-calculator.html": "20-Year Mortgage",
        "mortgage-15-year-calculator.html": "15-Year Mortgage",
        "mortgage-10-year-calculator.html": "10-Year Mortgage",
    }
    if fname in MORTGAGE_SPECIAL:
        return {"cluster": "mortgage", "parent": "mortgage-calculator.html", "parent_label": "Mortgage Calculator", "current_label": MORTGAGE_SPECIAL[fname]}

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
        return {"cluster": "country", "parent": "index.html", "parent_label": "Home", "current_label": f"Loan Calculator {label}", "slug": slug}

    # Business
    if fname == "business-loan-calculator.html":
        return {"cluster": "business", "parent": "index.html", "parent_label": "Home", "current_label": "Business Loan Calculator"}
    m = re.match(r"business-loan-(\d+)-payment\.html", fname)
    if m:
        amt = int(m.group(1))
        return {"cluster": "business", "parent": "business-loan-calculator.html", "parent_label": "Business Loan Calculator", "current_label": f"Business Loan for ${amt:,}", "amount": amt}

    # Unknown - treat as utility
    return {"cluster": "utility", "parent": "index.html", "parent_label": "Home", "current_label": fname.replace(".html", "").replace("-", " ").title()}


def _util_label(fname: str) -> str:
    labels = {"about.html": "About", "contact.html": "Contact", "sitemap.html": "Sitemap", "terms.html": "Terms", "privacy-policy.html": "Privacy Policy"}
    return labels.get(fname, "Page")


# ---------------------------------------------------------------------------
# Related links builder (silo-aware, min 5 links)
# ---------------------------------------------------------------------------

COUNTRY_FILES = [
    "loan-calculator-usa.html", "loan-calculator-uk.html", "loan-calculator-canada.html",
    "loan-calculator-australia.html", "loan-calculator-uae.html", "loan-calculator-morocco.html",
    "loan-calculator-india.html", "loan-calculator-singapore.html", "loan-calculator-new-zealand.html",
    "loan-calculator-ireland.html",
]

COUNTRY_LABELS = {
    "loan-calculator-usa.html": "Loan Calculator USA",
    "loan-calculator-uk.html": "Loan Calculator UK",
    "loan-calculator-canada.html": "Loan Calculator Canada",
    "loan-calculator-australia.html": "Loan Calculator Australia",
    "loan-calculator-uae.html": "Loan Calculator UAE",
    "loan-calculator-morocco.html": "Loan Calculator Morocco",
    "loan-calculator-india.html": "Loan Calculator India",
    "loan-calculator-singapore.html": "Loan Calculator Singapore",
    "loan-calculator-new-zealand.html": "Loan Calculator New Zealand",
    "loan-calculator-ireland.html": "Loan Calculator Ireland",
}


def _get_sibling_amounts(fname: str, info: dict, all_files: set) -> List[Tuple[str, str]]:
    """Get adjacent amount pages for loan/car/personal/mortgage amount pages."""
    result = []
    cluster = info.get("cluster", "")
    amt = info.get("amount")
    amt_k = info.get("amount_k")

    if cluster == "general" and amt is not None:
        for delta in [-2000, 2000, -5000, 5000]:
            other = amt + delta
            if other > 0:
                h = f"loan-{other}-monthly-payment.html"
                if h in all_files and h != fname:
                    result.append((h, f"Loan for ${other:,}"))
    elif cluster == "car" and amt is not None:
        for delta in [-5000, 5000, -10000, 10000]:
            other = amt + delta
            if other > 0:
                h = f"car-loan-{other}-monthly-payment.html"
                if h in all_files and h != fname:
                    result.append((h, f"Car Loan for ${other:,}"))
    elif cluster == "personal" and amt is not None:
        for delta in [-1000, 1000, -5000, 5000]:
            other = amt + delta
            if other > 0:
                h = f"personal-loan-{other}-payment.html"
                if h in all_files and h != fname:
                    result.append((h, f"Personal Loan for ${other:,}"))
    elif cluster == "mortgage" and amt_k is not None:
        for delta in [-50, 50, -100, 100]:
            other = amt_k + delta
            if other > 0:
                h = f"mortgage-{other}k-payment.html"
                if h in all_files and h != fname:
                    result.append((h, f"Mortgage for ${other}k"))

    return result[:3]  # max 3 siblings


def get_related_links(fname: str, info: dict, all_files: set) -> List[Tuple[str, str]]:
    """Build silo-aware related links (href, label). Excludes self. Min 5 links."""
    links = []
    cluster = info.get("cluster", "general")
    parent = info.get("parent")

    def add(href: str, label: str):
        if href in all_files and href != fname and (href, label) not in links:
            links.append((href, label))

    # 1. Parent link
    if parent and parent in all_files:
        parent_label = info.get("parent_label", "Parent")
        add(parent, parent_label)

    # 2. Sibling amount pages (for amount-driven pages)
    for href, label in _get_sibling_amounts(fname, info, all_files):
        add(href, label)

    # 3. Sibling / cluster links
    if cluster == "general":
        # Top general subpages
        for h in ["loan-10000-monthly-payment.html", "loan-20000-monthly-payment.html", "personal-loan-calculator.html", "car-loan-calculator.html", "mortgage-calculator.html"]:
            if h in all_files and h != fname:
                lbl = {"loan-10000-monthly-payment.html": "Loan for $10,000", "loan-20000-monthly-payment.html": "Loan for $20,000"}.get(h, _short_label(h))
                add(h, lbl)
    elif cluster == "car":
        for h in ["car-loan-20000-monthly-payment.html", "car-loan-30000-monthly-payment.html", "auto-loan-calculator-60-months.html", "car-loan-with-trade-in-calculator.html", "how-much-car-loan-can-i-afford.html"]:
            add(h, _short_label(h))
    elif cluster == "personal":
        for h in ["personal-loan-10000-payment.html", "personal-loan-5000-payment.html", "loan-10000-monthly-payment.html"]:
            add(h, _short_label(h))
    elif cluster == "mortgage":
        for h in ["mortgage-200k-payment.html", "mortgage-300k-payment.html", "mortgage-30-year-calculator.html"]:
            add(h, _short_label(h))
    elif cluster == "country":
        for h in ["loan-calculator-usa.html", "loan-calculator-uk.html", "loan-calculator-australia.html"]:
            add(h, COUNTRY_LABELS.get(h, h))
    elif cluster == "business":
        for h in ["business-loan-10000-payment.html", "business-loan-50000-payment.html", "personal-loan-calculator.html"]:
            add(h, _short_label(h))

    # 3. Cross-silo: index (once only), main calculators
    add("index.html", "Loan Calculator")
    if fname != "car-loan-calculator.html":
        add("car-loan-calculator.html", "Car Loan Calculator")
    if fname != "auto-loan-calculator.html":
        add("auto-loan-calculator.html", "Auto Loan Calculator")
    if cluster != "personal":
        add("personal-loan-calculator.html", "Personal Loan Calculator")
    if cluster != "mortgage":
        add("mortgage-calculator.html", "Mortgage Calculator")
    if cluster != "business":
        add("business-loan-calculator.html", "Business Loan Calculator")

    # 4. Country links for crawlability (cross-link country pages)
    if cluster in ("general", "car", "personal", "mortgage", "business", "utility") and len(links) < 14:
        for h in ["loan-calculator-usa.html", "loan-calculator-uk.html", "loan-calculator-canada.html"]:
            add(h, COUNTRY_LABELS.get(h, "Country"))

    # 5. Utility: add sitemap for thin pages
    if cluster == "utility" and len(links) < 10:
        add("sitemap.html", "Full Sitemap")

    # Deduplicate by href (keep first occurrence)
    seen = set()
    deduped = []
    for h, l in links:
        if h in all_files and h != fname and h not in seen:
            seen.add(h)
            deduped.append((h, l))

    return deduped[:12]


def _short_label(href: str) -> str:
    """Short descriptive label from href."""
    m = re.match(r"car-loan-(\d+)-monthly-payment\.html", href)
    if m:
        return f"Car Loan for ${int(m.group(1)):,}"
    m = re.match(r"personal-loan-(\d+)-payment\.html", href)
    if m:
        return f"Personal Loan for ${int(m.group(1)):,}"
    m = re.match(r"loan-(\d+)-monthly-payment\.html", href)
    if m:
        return f"Loan for ${int(m.group(1)):,}"
    m = re.match(r"mortgage-(\d+)k-payment\.html", href)
    if m:
        return f"Mortgage for ${m.group(1)}k"
    m = re.match(r"business-loan-(\d+)-payment\.html", href)
    if m:
        return f"Business Loan for ${int(m.group(1)):,}"
    labels = {
        "index.html": "Loan Calculator",
        "car-loan-calculator.html": "Car Loan Calculator",
        "auto-loan-calculator.html": "Auto Loan Calculator",
        "personal-loan-calculator.html": "Personal Loan Calculator",
        "mortgage-calculator.html": "Mortgage Calculator",
        "business-loan-calculator.html": "Business Loan Calculator",
        "auto-loan-calculator-36-months.html": "36 Month Auto Loan",
        "auto-loan-calculator-48-months.html": "48 Month Auto Loan",
        "auto-loan-calculator-60-months.html": "60 Month Auto Loan",
        "auto-loan-calculator-72-months.html": "72 Month Auto Loan",
        "used-car-loan-calculator.html": "Used Car Loan Calculator",
        "car-loan-with-trade-in-calculator.html": "Car Loan with Trade-In",
        "how-much-car-loan-can-i-afford.html": "How Much Car Loan Can I Afford",
        "car-loan-monthly-payment-calculator.html": "Car Loan Monthly Payment",
        "debt-consolidation-loan-calculator.html": "Debt Consolidation Loan",
        "home-improvement-loan-calculator.html": "Home Improvement Loan",
        "mortgage-30-year-calculator.html": "30-Year Mortgage",
        "mortgage-15-year-calculator.html": "15-Year Mortgage",
        "loan-calculator-with-down-payment.html": "Loan with Down Payment",
        "loan-calculator-with-extra-payments.html": "Loan with Extra Payments",
        "how-to-calculate-loan-monthly-payment.html": "How to Calculate Loan Payment",
        "loan-calculator-comparison.html": "Loan Calculator Comparison",
    }
    return labels.get(href, href.replace(".html", "").replace("-", " ").title())


# ---------------------------------------------------------------------------
# Silo links for parent pages (In this section: ...)
# ---------------------------------------------------------------------------

def get_silo_links_for_amount_page(fname: str, info: dict, all_files: set) -> Optional[str]:
    """Return compact silo links for amount/subpages (links to parent + siblings)."""
    cluster = info.get("cluster", "")
    parent = info.get("parent")
    amt = info.get("amount")
    amt_k = info.get("amount_k")
    if not parent or parent not in all_files:
        return None
    items = [(parent, "Main calculator")]
    if cluster == "car" and amt is not None:
        for delta in [-5000, 5000, -10000, 10000]:
            other = amt + delta
            if other > 0:
                h = f"car-loan-{other}-monthly-payment.html"
                if h in all_files and h != fname:
                    items.append((h, f"${other:,}"))
                    if len(items) >= 5:
                        break
        items.extend([
            ("auto-loan-calculator-60-months.html", "60 mo"),
            ("car-loan-with-trade-in-calculator.html", "Trade-in"),
        ])
    elif cluster == "personal" and amt is not None:
        for delta in [-5000, 5000]:
            other = amt + delta
            if other > 0:
                h = f"personal-loan-{other}-payment.html"
                if h in all_files and h != fname:
                    items.append((h, f"${other:,}"))
                    if len(items) >= 5:
                        break
        items.extend([
            ("debt-consolidation-loan-calculator.html", "Debt Consolidation"),
        ])
    elif cluster == "mortgage" and amt_k is not None:
        for delta in [-50, 50, -100, 100]:
            other = amt_k + delta
            if other > 0:
                h = f"mortgage-{other}k-payment.html"
                if h in all_files and h != fname:
                    items.append((h, f"${other}k"))
                    if len(items) >= 5:
                        break
        items.append(("mortgage-30-year-calculator.html", "30-Year"))
    elif cluster == "general" and amt is not None:
        for delta in [-5000, 5000]:
            other = amt + delta
            if other > 0:
                h = f"loan-{other}-monthly-payment.html"
                if h in all_files and h != fname:
                    items.append((h, f"${other:,}"))
                    if len(items) >= 5:
                        break
    else:
        return None
    parts = []
    seen = set()
    for href, label in items:
        if href in all_files and href not in seen:
            seen.add(href)
            parts.append(f'<a href="{href}">{label}</a>')
    if len(parts) < 3:
        return None
    return f'''    <nav class="silo-links silo-links--compact" aria-label="Calculators in this section">
      <p class="silo-links-intro">In this section:</p>
      <p class="silo-links-row">
        {" · ".join(parts[:8])}
      </p>
    </nav>'''


def get_silo_links(fname: str, all_files: set) -> Optional[str]:
    """Return HTML for silo-links nav if this is a parent page that should have one."""
    if fname == "index.html":
        items = [
            ("loan-5000-monthly-payment.html", "$5k"),
            ("loan-10000-monthly-payment.html", "$10k"),
            ("loan-20000-monthly-payment.html", "$20k"),
            ("loan-50000-monthly-payment.html", "$50k"),
            ("car-loan-calculator.html", "Car Loan"),
            ("personal-loan-calculator.html", "Personal"),
            ("mortgage-calculator.html", "Mortgage"),
            ("loan-calculator-usa.html", "USA"),
            ("loan-calculator-uk.html", "UK"),
        ]
    elif fname in ("car-loan-calculator.html", "auto-loan-calculator.html"):
        items = [
            ("car-loan-15000-monthly-payment.html", "$15k"),
            ("car-loan-20000-monthly-payment.html", "$20k"),
            ("car-loan-25000-monthly-payment.html", "$25k"),
            ("car-loan-30000-monthly-payment.html", "$30k"),
            ("car-loan-40000-monthly-payment.html", "$40k"),
            ("car-loan-50000-monthly-payment.html", "$50k"),
            ("auto-loan-calculator-24-months.html", "24 mo"),
            ("auto-loan-calculator-36-months.html", "36 mo"),
            ("auto-loan-calculator-48-months.html", "48 mo"),
            ("auto-loan-calculator-60-months.html", "60 mo"),
            ("auto-loan-calculator-72-months.html", "72 mo"),
            ("used-car-loan-calculator.html", "Used Car"),
            ("auto-loan-refinance-calculator.html", "Refinance"),
            ("car-loan-with-trade-in-calculator.html", "Trade-in"),
            ("how-much-car-loan-can-i-afford.html", "Affordability"),
        ]
    elif fname == "personal-loan-calculator.html":
        items = [
            ("personal-loan-5000-payment.html", "$5k"),
            ("personal-loan-10000-payment.html", "$10k"),
            ("personal-loan-15000-payment.html", "$15k"),
            ("personal-loan-20000-payment.html", "$20k"),
            ("personal-loan-25000-payment.html", "$25k"),
            ("bad-credit-loan-calculator.html", "Bad Credit"),
            ("debt-consolidation-loan-calculator.html", "Debt Consolidation"),
            ("home-improvement-loan-calculator.html", "Home Improvement"),
        ]
    elif fname == "mortgage-calculator.html":
        items = [
            ("mortgage-150k-payment.html", "$150k"),
            ("mortgage-200k-payment.html", "$200k"),
            ("mortgage-250k-payment.html", "$250k"),
            ("mortgage-300k-payment.html", "$300k"),
            ("mortgage-400k-payment.html", "$400k"),
            ("mortgage-10-year-calculator.html", "10-Year"),
            ("mortgage-15-year-calculator.html", "15-Year"),
            ("mortgage-20-year-calculator.html", "20-Year"),
            ("mortgage-30-year-calculator.html", "30-Year"),
        ]
    elif fname == "business-loan-calculator.html":
        items = [
            ("business-loan-10000-payment.html", "$10k"),
            ("business-loan-20000-payment.html", "$20k"),
            ("business-loan-50000-payment.html", "$50k"),
        ]
    else:
        return None

    parts = []
    for href, label in items:
        if href in all_files:
            parts.append(f'<a href="{href}">{label}</a>')
    if not parts:
        return None
    return f'''    <nav class="silo-links" aria-label="Calculators in this section">
      <p class="silo-links-intro">In this section:</p>
      <p class="silo-links-row">
        {" · ".join(parts)}
      </p>
    </nav>'''
