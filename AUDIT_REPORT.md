# LoanWiseCalc — BMAD Audit Report

**Date:** March 2026  
**Scope:** Full project audit, cleanup, optimization, validation

---

## Phase 1 — Findings Classification

### Critical Issues
1. **robots.txt domain mismatch** — References `https://www.loanwise.site/sitemap.xml` but site uses `loanwisecalc.com` in canonicals and sitemap.
2. **Zero-byte temp files** — `index.html.txt`, `script.js.txt`, `style.css.txt` (editor artifacts, safe to remove).

### Medium Issues
1. **Build script clutter** — Multiple one-off Python scripts in root (seo_audit, ctr_optimize, _optimize_ctr, apply_silo_structure, etc.) that could be moved to `scripts/` or documented as dev-only.
2. **sitemap.xml missing mortgage-10-year, mortgage-20-year in alphabetical order** — They appear at end (insert order); not critical but inconsistent.

### Low-Priority Cleanup
1. **__pycache__** — Python cache; add to .gitignore if not already.
2. **_bmad, _bmad-output** — BMAD workflow folders; typically excluded from deployment.
3. **.DS_Store** — macOS metadata; already in .gitignore.
4. **Duplicate script patterns** — loan-calculator-with-down-payment, loan-calculator-with-extra-payments, car-loan-with-trade-in use inline JS (custom calculator logic) instead of script.js; intentional, no change needed.

---

## Phase 2 — File Cleanup (Safe)

### Remove
- `index.html.txt` (0 bytes, temp)
- `script.js.txt` (0 bytes, temp)
- `style.css.txt` (0 bytes, temp)

### Keep (Production)
- All 137 HTML pages
- `style.css`, `script.js`
- `robots.txt`, `sitemap.xml`, `sitemap.html`
- `config/`, `templates/` (for regeneration)

### Dev-Only (Do not deploy as static assets)
- `*.py` (build scripts)
- `_bmad/`, `_bmad-output/`, `docs/`
- `GENERATION_README.md`, `INTERNAL_LINKING.md`
- `__pycache__/`

---

## Phase 3 — HTML + SEO Validation

| Check | Result |
|-------|--------|
| Valid HTML structure | Pass |
| One H1 per page | Pass |
| Heading hierarchy | Pass |
| Unique title | Pass |
| Unique meta description | Pass |
| Canonical tag | Pass (all pages) |
| Viewport meta | Pass (all pages) |

---

## Phase 4 — Internal Linking + Indexability

| Check | Result |
|-------|--------|
| Broken internal links | None (130 targets verified) |
| Related Calculators section | Present on all calculator pages |
| Orphan pages | None |
| Sitemap includes production pages | Pass (138 URLs) |
| robots.txt | Fix domain to loanwisecalc.com |

---

## Phase 5 — Performance + Mobile

- CSS/JS: Single file each, no heavy bloat.
- No images to optimize.
- Responsive layout via media queries.
- Ad slots use minimal placeholder markup.

---

## Phase 6 — JavaScript

- script.js: initCalculator() for standard calculator pages.
- Custom calculators (down-payment, extra-payments, trade-in) use inline JS; no conflicts.
- simple-interest-calculator, interest-calculator: custom logic.
- No console errors observed in structure.

---

## Phase 7 — Final Checks

- No duplicate titles.
- No duplicate meta descriptions.
- Canonical consistency: loanwisecalc.com throughout.
- Navigation consistent across pages.

---

## Fixes Applied

| Fix | Status |
|-----|--------|
| Deleted index.html.txt, script.js.txt, style.css.txt | Done |
| Fixed robots.txt sitemap URL (loanwisecalc.com) | Done |
| Added __pycache__, _bmad-output to .gitignore | Done |
| Fixed stray Unicode chars before related-calculators (136 files) | Done |
| Removed duplicate related-calculators in loan-calculator-uae | Done |
| Added netlify.toml for production deployment | Done |
| Fixed double-encoded &amp;amp; → &amp; in meta/og tags (87 HTML files) | Done |
