# Internal Linking System

LoanWise uses an automatic internal linking system to improve SEO: no orphan pages, strong topical clusters, better crawlability, and contextual relevance.

## Components

| File | Purpose |
|------|---------|
| `config/internal_linking.py` | Page classification, related links, silo links, breadcrumb logic |
| `apply_internal_links.py` | Applies linking to all HTML pages |

## What Gets Applied

1. **Breadcrumb navigation** — Near the top of every page
   - Home › Parent › Current page
   - Descriptive, crawlable links

2. **Related Calculators** — Section on every page
   - Minimum 5 internal links per page
   - Silo-aware: links stay within cluster first, then cross-silo
   - Descriptive anchor text (no exact-match abuse)

3. **Silo links** — On parent pages (index, car-loan-calculator, personal-loan-calculator, mortgage-calculator, business-loan-calculator)
   - "In this section:" with links to top subpages
   - Example: $15k · $20k · $30k · 48 mo · 60 mo · Trade-in · Affordability

4. **Contextual links** — Already present in content
   - Help text, disclaimer, FAQ answers, and body copy link to relevant calculators

## Cluster Structure

- **General** — index, loan-N-monthly-payment, loan tools (down payment, extra payments, interest)
- **Car** — car-loan-calculator, car-loan-N, auto-loan-*, used-car, trade-in, affordability
- **Personal** — personal-loan-calculator, personal-loan-N, debt-consolidation, home-improvement
- **Mortgage** — mortgage-calculator, mortgage-Nk, 15-year, 30-year
- **Country** — loan-calculator-usa, loan-calculator-uk, etc.
- **Business** — business-loan-calculator, business-loan-N
- **Utility** — about, contact, terms, privacy, sitemap

## Usage

```bash
# Apply to all pages (run after generate_calculator_pages.py)
python3 apply_internal_links.py
```

## Adding New Pages

When you add new HTML pages:

1. Add the page to `config/page_types.py` if it's generated, or ensure the filename matches a pattern in `config/internal_linking.py`
2. Run `apply_internal_links.py` — it discovers all `.html` files and classifies them by filename pattern
3. Unknown patterns fall back to "utility" (Home › Page)

To support a new page type, add a pattern in `classify_page()` and related logic in `get_related_links()` and optionally `get_silo_links()` in `config/internal_linking.py`.

## Technical Rules

- All links are crawlable HTML `<a href="...">` (no JavaScript)
- Descriptive anchor text (e.g. "Car Loan for $20,000" not "click here")
- No repetitive exact-match anchor abuse
- Layout remains clean (existing CSS classes: breadcrumb, related-calculators, silo-links)
