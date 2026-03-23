# Third-Party Tracking Audit — LoanWiseCalc

**Last updated:** March 2026

## Current Setup

### 1. Google Tag Manager (GTM-WPRBNP3T)
- **Placement:** Inline script in `<head>`, loads gtm.js asynchronously
- **Purpose:** Container for GA4 and other tags (configured in GTM)
- **Blocking:** No — gtm.js loads with `async`
- **Duplicate:** None — single GTM container

### 2. Google AdSense (ca-pub-7502486843743422)
- **Placement:** Deferred loader in `<head>` — loads via `requestIdleCallback` (2.5s) or `setTimeout(400ms)`
- **Purpose:** Ad serving and site verification
- **Blocking:** No — script injected when browser idle
- **Duplicate:** None — single script

### 3. First-Party (script.js)
- **Placement:** End of `<body>`, `defer`
- **Purpose:** Calculator logic
- **Blocking:** No — `defer` ensures non-blocking

## Optimizations Applied

| Optimization | Status |
|-------------|--------|
| Preconnect to googletagmanager.com | ✅ All pages |
| Preconnect to pagead2.googlesyndication.com | ✅ All pages |
| Meta charset + viewport first in head | ✅ Index, key pages |
| AdSense deferred load (requestIdleCallback) | ✅ All pages |
| GTM gtm.js fetchPriority=low | ✅ All pages |
| dns-prefetch google-analytics.com | ✅ All pages |
| script.js defer | ✅ All pages |
| No duplicate analytics | ✅ Verified |

## Script Load Order (Recommended)

1. `<meta charset>`, `<meta viewport>`
2. `<link rel="preconnect">` (GTM, AdSense)
3. GTM inline snippet
4. AdSense script (async)
5. Preload/CSS
6. Page content
7. script.js (defer, end of body)

## GTM + GA4

GA4 is loaded via GTM. Do not add a separate gtag.js or analytics.js — this would duplicate tracking.

## Future Recommendations

- **GTM:** Audit tags in GTM; remove unused triggers; use consent mode if required
- **AdSense:** Keep reserved ad slot heights to minimize CLS
- **LCP:** Critical CSS inline on index; preload key assets
