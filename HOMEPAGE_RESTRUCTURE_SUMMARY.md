# Homepage Restructure — Premium, Conversion-Focused Layout

## New Structure (Top to Bottom)

1. **HERO** — Clear title, subtitle, intro, last-updated
2. **CALCULATOR** — Main focus (unchanged)
3. **TOP CATEGORIES** — 6 cards (Car, Personal, Mortgage, Business, Interest, USA)
4. **TRUST / BENEFITS** — "Why use LoanWise?" (4 points)
5. **INTERNAL LINKS** — Grouped: By amount, By region, Specialized + sitemap
6. **DISCLAIMER** — Compact single paragraph
7. **CONTENT** — Formula, example, FAQ (SEO long-form)
8. **ADS** — Middle, bottom
9. **FOOTER** — Complete links (unchanged)

---

## Changes Implemented

### Removed
- **Help text** (5 inline links) — duplicated popular calculators
- **Popular calculators** (13 cards) — replaced by 6 top categories + internal links
- **How to use** (4-step list) — redundant with obvious UI
- **Explore links** (5 links) — merged into internal links section
- **Disclaimer** (3 links) — reduced to 1 link

### Replaced
- **13 calc-cards** → **6 category-cards** (curated top tools)
- **Wall of links** → **Grouped link-groups** (By amount, By region, Specialized)
- **Repeated CTAs** → Single "Get estimate" per card

### Added
- **Internal links section** — Clean 3-column layout with sitemap CTA
- **Section titles/ledes** — Consistent `.section-title`, `.section-lede`
- **Visually hidden** — Disclaimer h2 for accessibility

---

## SEO Preservation

| Page Type | Before | After |
|-----------|--------|-------|
| Car Loan | 6 zones | Top categories + footer |
| Personal, Mortgage, Business, Interest | 6 zones | Top categories + internal links + footer |
| USA | 5 zones | Top categories + By region + footer |
| UK, Canada, UAE, Morocco, Australia | 4 zones | By region + footer |
| Auto, Simple Interest | 4 zones | Specialized + footer |
| $10k, $20k, Down payment | 3 zones | By amount + footer |
| Used Car, Mortgage $200k | 2 zones | Specialized + footer |

**All pages remain linked.** Footer unchanged. Sitemap linked from internal links CTA.

---

## Visual Improvements

- **More white space** — Section borders, padding (2rem, 2.25rem)
- **Fewer sections** — 8 → 6 main blocks before content
- **Clean cards** — Category cards with hover, consistent CTA
- **Grouped links** — Clear hierarchy (By amount | By region | Specialized)
- **Single CTA** — "View full sitemap" instead of scattered links

---

## Files Modified

- **index.html** — Structure, sections, content prose (1 link instead of 6)
- **style.css** — New: `.top-categories`, `.category-card`, `.link-groups`, `.disclaimer-section`, `.visually-hidden`; updated section spacing
