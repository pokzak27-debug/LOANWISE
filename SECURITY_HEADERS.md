# Security Headers — LoanWise

Headers are configured in `netlify.toml` and applied to all routes.

---

## Headers and their role

### Content-Security-Policy (CSP)

Limits where resources (scripts, styles, images, etc.) can be loaded from.

| Directive | Value | Why |
|-----------|-------|-----|
| `default-src` | `'self'` | Only same-origin by default |
| `script-src` | `'self'` + AdSense/GTM + `'unsafe-inline'` `'unsafe-eval'` | Own scripts, critical inline, JSON-LD, AdSense |
| `style-src` | `'self'` + `'unsafe-inline'` | External CSS + critical inline CSS |
| `img-src` | `'self'` + `data:` + `https:` | Images, data URIs, ad images |
| `font-src` | `'self'` | Web fonts from same origin |
| `connect-src` | `'self'` + GA/GTM/AdSense | XHR, fetch, analytics/ads |
| `frame-src` | AdSense domains | Ad iframes |
| `frame-ancestors` | `'none'` | Page cannot be framed (modern alternative to X-Frame-Options) |
| `form-action` | `'self'` | Forms submit only to same origin |
| `base-uri` | `'self'` | Prevents base tag hijacking |
| `object-src` | `'none'` | Blocks Flash, plugins, embeds |

---

### Strict-Transport-Security (HSTS)

Forces browsers to use HTTPS only.

- **max-age=31536000** — 1 year
- **includeSubDomains** — applies to all subdomains
- **preload** — eligible for browser HSTS preload lists

**Action:** Submit domain to [hstspreload.org](https://hstspreload.org).

---

### X-Frame-Options

Blocks framing (clickjacking).

- **DENY** — page cannot be put in any iframe

---

### Cross-Origin-Opener-Policy (COOP)

Isolates the document from cross-origin openers.

- **same-origin** — only same-origin windows can be in the same browsing context group (reduces cross-tab attacks like Spectre)

---

### Permissions-Policy

Disables unneeded browser features.

- **camera=(), microphone=(), geolocation=()** — no sensors
- **interest-cohort=()** — FLoC off
- **payment=(), usb=()** — no payment/USB access
- **magnetometer=(), gyroscope=(), accelerometer=()** — no motion sensors

---

### Referrer-Policy

Controls how much referrer info is sent on outbound links.

- **strict-origin-when-cross-origin** — full URL for same-origin; origin only for HTTPS→HTTP; none for downgrade

---

### X-Content-Type-Options

Stops MIME sniffing.

- **nosniff** — browser uses declared Content-Type

---

## Compatibility

- Static site, scripts and styles keep working.
- AdSense/GTM domains are included for ads/analytics.
- SEO not affected (no special requirements for crawlers).
- HSTS needs a valid SSL cert (Netlify provides this).
