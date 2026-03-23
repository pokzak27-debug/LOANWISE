# Desktop Performance Final Pass — Summary

**Date:** March 2026  
**Goal:** Improve desktop PageSpeed from ~91 toward 95–99

---

## Changes Applied

### 1. Layout Shift (CLS)

| Change | File | Effect |
|--------|------|--------|
| `contain: layout style` + `min-height: 18rem` on `.calculator` (critical CSS) | index.html | Reserves space, prevents calculator from shifting when full CSS loads |
| `min-width: 5em` on `.result-value` | style.css, index critical | Reduces horizontal shift when "—" becomes "$X,XXX.XX" |
| `min-width: 6em` on first-child result-value | style.css | Larger monthly payment value needs more reserve |

### 2. Ad Containers

- Already stable: `contain: layout`, `flex-shrink: 0`, `overflow: hidden`, min-height on all slots
- No changes needed

### 3. CSS Animations

- Already optimized: only `transform` and `opacity` transitions; no `box-shadow`, `border-color`, or `color` on hover
- No changes needed

### 4. Third-Party Scripts

- GTM: `fetchPriority='low'` on gtm.js
- AdSense: deferred via `requestIdleCallback`
- Preconnect + dns-prefetch in place
- No changes needed

### 5. CSP for Google Ad Services

| Addition | netlify.toml | Purpose |
|----------|--------------|---------|
| `https://ep2.adtrafficquality.google` | connect-src | AdSense ad quality checks |
| `https://www.google.com` | connect-src | Broader Google API compatibility |

### 6. Calculator & Result Sections

- Calculator: `contain: layout style` in full CSS (already present)
- Results: `contain: layout style`, `min-height: 8rem` (already present)
- Result values: `min-width` added to reduce CLS when JS updates text

---

## Preserved

- Design, calculator functionality, GTM, GA4, AdSense
- No new frameworks or heavy changes
