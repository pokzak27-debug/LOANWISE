# LoanWise Page Generation Guide

This document explains how to generate and add new long-tail calculator pages using the template system.

## Overview

The system consists of:

| Component | Purpose |
|-----------|---------|
| `config/page_types.py` | Page definitions: amounts, countries, special-intent pages |
| `templates/page_template.html` | Base HTML structure with `{{ placeholders }}` |
| `templates/content_variations.py` | Intro, example, FAQ, and how-to wording variations for uniqueness |
| `generate_calculator_pages.py` | Main script that assembles pages and writes static HTML |

## Quick Start

```bash
python3 generate_calculator_pages.py
```

- **Skips** pages that already exist (no overwrites by default)
- **Creates** only new pages defined in `config/page_types.py`
- After generation, run `apply_internal_links.py` then `update_indexing.py` for sitemap, footer, and internal links

---

## How to Add New Pages

### 1. Loan Amount Pages (e.g. loan-7500-monthly-payment.html)

Edit `config/page_types.py`:

```python
GENERAL_LOAN_AMOUNTS.append((7500, 9, 36))
```

Format: `(amount, default_rate, default_term_months)`

Filename is auto-generated: `loan-{amount}-monthly-payment.html`

---

### 2. Car Loan Amount Pages

```python
CAR_LOAN_AMOUNTS.append((32000, 6.5, 60))
```

Filename: `car-loan-{amount}-monthly-payment.html`

---

### 3. Personal Loan Amount Pages

```python
PERSONAL_LOAN_AMOUNTS.append((13000, 8.5, 48))
```

Filename: `personal-loan-{amount}-payment.html`

---

### 4. Mortgage Amount Pages (in thousands)

```python
MORTGAGE_AMOUNTS.append((375, 6.5, 360))
```

- `375` = $375,000
- Filename: `mortgage-375k-payment.html`

---

### 5. Country Pages

```python
COUNTRIES.append({
    "slug": "germany",
    "filename": "loan-calculator-germany.html",
    "title": "Loan Calculator Germany",
    "country": "Germany",
    "amount": 10000,
    "default_rate": 5,
    "default_term": 48,
    "loan_step": 1000,
})
```

---

### 6. Special Intent Pages (e.g. medical loan, wedding loan)

Add a full definition to `SPECIAL_INTENT_PAGES` in `config/page_types.py`:

```python
{
    "filename": "medical-loan-calculator.html",
    "cluster": "personal",
    "amount": 15000,
    "default_rate": 10,
    "default_term": 48,
    "loan_step": 500,
    "breadcrumb_parent": "personal-loan-calculator.html",
    "breadcrumb_parent_label": "Personal Loan Calculator",
    "breadcrumb_current": "Medical Loan Calculator",
    "title": "Medical Loan Calculator – Free Payment Tool",
    "meta": "Medical loan payment in seconds. Free calculator. Compare terms. No signup.",
    "h1": "Medical Loan Calculator — Free Estimate",
    "subtitle": "Typical medical loan terms—adjust to your procedure",
    "related": [
        ("personal-loan-calculator.html", "Personal Loan Calculator"),
        ("index.html", "Loan Calculator"),
        # ... more related links
    ],
}
```

Required fields: `filename`, `cluster`, `amount`, `default_rate`, `default_term`, `loan_step`, breadcrumb fields, `title`, `meta`, `h1`, `subtitle`, `related`.

---

## Uniqueness System

Content variations ensure each page feels unique:

- **Intros** — Multiple phrasings per page type (e.g. "Model a $X loan..." vs "Get your $X monthly payment...")
- **Examples** — Different real-world scenario wordings
- **FAQs** — Rotating questions/answers; order varies by page index
- **How-to** — Slight wording variations in step-by-step instructions

Variations are selected by **index** (e.g. amount position in list), so output is deterministic. Add more entries to the pools in `templates/content_variations.py` to increase variety.

---

## Template Placeholders

`templates/page_template.html` uses these placeholders:

| Placeholder | Source |
|-------------|--------|
| `{{ title }}` | Page title (from config or auto-generated) |
| `{{ meta_description }}` | Meta description |
| `{{ canonical_url }}` | Full canonical URL |
| `{{ h1 }}` | Main heading |
| `{{ subtitle }}` | Subtitle under H1 |
| `{{ intro }}` | First paragraph (from content variations) |
| `{{ nav_html }}` | Site navigation (shared) |
| `{{ breadcrumb_html }}` | Breadcrumb nav (from config) |
| `{{ calculator_html }}` | Calculator form (shared, values from config) |
| `{{ help_links }}` | Help text with adjacent amounts/links |
| `{{ disclaimer }}` | Estimate disclaimer |
| `{{ content_section }}` | How-to, examples, FAQs (from content variations) |
| `{{ related_calculators_html }}` | Related links section |
| `{{ footer_html }}` | Footer + script (shared) |
| `{{ last_updated }}` | Last updated date |

---

## Post-Generation Steps

1. **Silo structure** — Run `apply_silo_structure.py` to set breadcrumbs and related links
2. **Sitemap** — Run `update_for_new_pages.py` to add new URLs to `sitemap.xml`
3. **CTR titles** (optional) — Run `apply_ctr_titles.py` for title/meta optimization

---

## Adding New Content Variations

To vary intros, examples, or FAQs more:

1. Edit `templates/content_variations.py`
2. Add new strings to the relevant pool (e.g. `INTRO_LOAN_AMOUNT.append("...")`)
3. Re-run the generator (you may need to delete existing pages or add a `--force` flag to overwrite)
