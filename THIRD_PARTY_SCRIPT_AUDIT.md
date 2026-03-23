# Third-Party Script Audit — LoanWiseCalc

**Last updated:** March 2026  
**Focus:** Reduce desktop performance cost without breaking analytics or monetization

---

## 1. Script Inventory

| Script | Purpose | Load Strategy | Blocking |
|--------|---------|---------------|----------|
| **GTM (GTM-WPRBNP3T)** | Container for GA4, tags | Inline snippet → injects gtm.js with `async` | No — async |
| **GA4** | Analytics (pageviews, events) | Loaded via GTM container | No |
| **AdSense (adsbygoogle.js)** | Ad serving | Deferred: `requestIdleCallback` (2.5s) or `setTimeout(400ms)` | No |
| **Doubleclick / show_ads_impl** | Ad delivery | Loaded by AdSense when needed | No |

---

## 2. Duplicate Analytics Check

- ✅ **No duplicate** — GA4 is loaded only through GTM
- ✅ **No direct gtag.js** — Do not add `<script src="https://www.googletagmanager.com/gtag/js?id=G-...">`; this would duplicate pageviews
- ✅ **Single GTM container** — GTM-WPRBNP3T only

---

## 3. Load Order (All Pages)

1. `<meta charset>`, `<meta viewport>`
2. `preconnect` → googletagmanager.com, pagead2.googlesyndication.com
3. `dns-prefetch` → google-analytics.com (hint for GA4 when GTM loads)
4. GTM inline snippet (injects gtm.js with `fetchPriority='low'`)
5. AdSense deferred loader (loads adsbygoogle.js when idle)
6. Critical CSS / styles
7. Page content
8. `script.js` (defer, end of body)

---

## 4. Optimizations Applied

| Optimization | Status |
|-------------|--------|
| Preconnect to googletagmanager.com | ✅ |
| Preconnect to pagead2.googlesyndication.com | ✅ |
| dns-prefetch to google-analytics.com | ✅ |
| GTM gtm.js: `fetchPriority='low'` | ✅ Reduces priority vs critical resources |
| AdSense: deferred via requestIdleCallback | ✅ Does not block initial render |
| No duplicate analytics | ✅ Verified |
| Meta charset + viewport first | ✅ |

---

## 5. What Not to Change

- **GTM** — Required for GA4 and tag management; do not remove
- **GA4** — Loaded via GTM; do not add a separate gtag.js
- **AdSense** — Required for monetization; keep deferred load

---

## 6. Optional Future Optimizations

- **GTM delayed load** — Load GTM after first interaction or 2s. Improves TBT but may miss fast bounces. Test before enabling.
- **GTM consent mode** — If GDPR/consent applies, configure consent mode in GTM.
- **Partytown** — Offload GTM to a web worker. Higher complexity; evaluate if TBT remains an issue.
