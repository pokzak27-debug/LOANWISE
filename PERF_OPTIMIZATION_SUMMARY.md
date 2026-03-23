# Mobile Performance Optimization — Core Web Vitals

**Date:** March 2026  
**Focus:** CLS, TBT, LCP, unused JavaScript, third-party script cost

---

## 1. Layout Stability (CLS)

| Change | Impact |
|--------|--------|
| `contain: layout` on `.ad-container` | Prevents ad injection from shifting surrounding content |
| `contain: layout` in index critical CSS | Same benefit before full stylesheet loads |
| Existing `min-height` on results, ad slots | Reserved space prevents collapse/shift |

---

## 2. Ad Slot Stability

| Change | Impact |
|--------|--------|
| `.ad-container` already has `min-height: 100px`, `overflow: hidden` | No layout collapse when ads load |
| `contain: layout` added | Isolates ad layout from page layout |

---

## 3. Third-Party Script Overhead (TBT)

| Change | Impact |
|--------|--------|
| **AdSense deferred load** | Script loads via `requestIdleCallback` (or `setTimeout` fallback). Reduces main-thread blocking during initial parse. Ads still render within ~400ms–2.5s. |
| Preconnect to GTM and AdSense | Already present; improves connection setup |
| GTM | Unchanged (required for GA4; user asked to keep compatible) |

---

## 4. TBT / LCP — Critical Resources

| Change | Impact |
|--------|--------|
| `preload` for `style.css` on 133+ pages | Earlier CSS fetch; improves LCP on calculator pages |
| `script.js` removed from static pages | about, contact, privacy-policy, terms no longer load unused calculator logic |
| Index: critical CSS + non-blocking stylesheet | Inline critical CSS, `media="print" onload` for main CSS |

---

## 5. Unused JavaScript

| Change | Impact |
|--------|--------|
| `script.js` removed from: about, contact, privacy-policy, terms | ~4KB saved per page; no calculator init on pages without `#currency` |

---

## 6. Template Updates

- **templates/page_template.html**: meta charset/viewport first, preconnect, preload for style.css, AdSense defer
- **generate_calculator_pages.py**: Output uses template; regenerated pages inherit optimizations

---

## Compatibility

- **Google Tag Manager / GA4:** Unchanged; tracking works as before
- **AdSense:** Deferred load is compatible; ads still fill reserved slots; no policy violation
- **Calculator:** Behavior unchanged; `script.js` still uses `requestIdleCallback` for init
