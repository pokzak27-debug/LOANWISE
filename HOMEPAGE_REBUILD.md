# Homepage Rebuild — Conversion + SEO

## Structure

### [HERO]
- **H1:** "Loan Calculator — Calculate Your Payment in Seconds"
- **Trust line:** "Free • No signup • Instant results"
- **Primary CTA:** "Calculate now" — scrolls to calculator

### [CALCULATOR]
- Main calculator block immediately below hero
- No distractions (ad moved below internal links)
- Same 4 inputs + CTA button + results (dl/dt/dd)

### [TOP CALCULATORS]
- 8 cards: Car Loan, Auto Loan, Personal, Mortgage, Business, Interest, USA, UK
- Each: title, short description, CTA "Calculate now"

### [TRUST]
- 3 benefits: **Fast**, **Free**, **Accurate**
- Single row on desktop
- No section lede (cleaner)

### [INTERNAL LINKS]
- One section, inline nav
- 6 links: $10,000, $20,000, Down payment, Mortgage $200k, Simple interest, All calculators →

### [FOOTER]
- Full sitemap links unchanged
- All pages preserved for SEO

---

## Removed / Simplified

| Before | After |
|--------|-------|
| Breadcrumb | Removed (hero-first flow) |
| 4 trust points | 3 (Fast, Free, Accurate) |
| Trust section lede | Removed |
| Explore More: 3 groups, 13 links | 1 row, 6 links |
| Section lede on Top Calculators | Removed |
| 6 category cards | 8 cards (added Auto, UK) |

---

## DOM Reduction

- **Trust:** 4 → 3 items (−1 li, −1 span, −1 strong, −1 p)
- **Internal links:** div wrappers + h3 removed → inline nav
- **Breadcrumb:** removed
- **Section ledes:** 2 removed
- **Estimate:** ~25 fewer elements

---

## Design

- **More whitespace:** Section spacing 3rem on desktop
- **Hero CTA:** Prominent button, scrolls to calculator
- **Smooth scroll:** `scroll-behavior: smooth` on html
- **Trust:** 3-column grid on desktop
- **Internal links:** Flex row, wraps on small screens

---

## SEO Preserved

- All important links in footer
- No pages deleted
- Schema.org FAQPage intact
- Content section (How to calculate, FAQ) kept
- Canonical, meta, OG tags unchanged
