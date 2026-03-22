# Security headers — Netlify config

## Fichier mis à jour

**`netlify.toml`** — headers de sécurité pour la prod.

---

## Détection du projet

| Élément | Résultat |
|---------|----------|
| `netlify.toml` | ✓ Présent, utilisé |
| `_headers` | ✗ Absent |
| Autre config | Aucune |

---

## Headers utilisés (résumé)

| Header | Rôle |
|--------|------|
| **X-Frame-Options: DENY** | Empêche l’inclusion en iframe (clickjacking) |
| **X-Content-Type-Options: nosniff** | Empêche le navigateur de deviner le type MIME |
| **Referrer-Policy: strict-origin-when-cross-origin** | Limite les infos envoyées dans le Referer vers d’autres sites |
| **Strict-Transport-Security** | Force HTTPS, avec subdomains et preload |
| **Cross-Origin-Opener-Policy: same-origin** | Isole la page des autres fenêtres cross-origin |
| **Permissions-Policy** | Désactive caméra, micro, géolocalisation, FLoC |
| **Content-Security-Policy** | Restreint l’origine des scripts, styles, images, formulaires, etc. |

---

## Contenu exact du fichier

```toml
# Netlify config for LoanWiseCalc static site
[build]
  publish = "."
  command = ""

# Security headers for all HTML pages
[[headers]]
  for = "/*.html"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Strict-Transport-Security = "max-age=31536000; includeSubDomains; preload"
    Cross-Origin-Opener-Policy = "same-origin"
    Permissions-Policy = "camera=(), microphone=(), geolocation=(), interest-cohort=()"
    Content-Security-Policy = "default-src 'self'; script-src 'self' https://pagead2.googlesyndication.com https://partner.googleadservices.com https://www.googletagmanager.com 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self' https://www.google-analytics.com https://www.googletagmanager.com https://googleads.g.doubleclick.net; frame-src https://googleads.g.doubleclick.net https://tpc.googlesyndication.com https://fundingchoicesmessages.google.com; frame-ancestors 'none'; form-action 'self'; base-uri 'self'"

# Security headers for root/index
[[headers]]
  for = "/"
  [headers.values]
    # (mêmes valeurs que ci-dessus)

# Cache static assets
[[headers]]
  for = "/*.css"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/*.js"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
```

---

## CSP en détail

| Directive | Valeur | Raison |
|-----------|--------|--------|
| default-src | 'self' | Par défaut, tout vient du même domaine |
| script-src | 'self' + Google (AdSense, GTM) + 'unsafe-inline' 'unsafe-eval' | Scripts du site + AdSense/analytics, inline requis par AdSense |
| style-src | 'self' 'unsafe-inline' | CSS du site + critical CSS inline |
| img-src | 'self' data: https: | Images du site, data: pour icônes, https: pour pixels pub/analytics |
| font-src | 'self' | Polices éventuelles sur le même domaine |
| connect-src | 'self' + Google Analytics, GTM, DoubleClick | Requêtes AJAX / analytics / ads |
| frame-src | DoubleClick, Google syndication, Funding Choices | Iframes des pubs AdSense |
| frame-ancestors | 'none' | Aucune page ne peut afficher le site en iframe |
| form-action | 'self' | Formulaires uniquement vers le même domaine |
| base-uri | 'self' | Évite les injections via `<base>` |

---

## Ce qui reste autorisé

- CSS, JS, favicon, canonicals, schema JSON-LD
- Formulaires (contact) vers le même domaine
- Emplacements AdSense futurs (scripts et frames)
- Google Analytics / GTM si ajoutés plus tard

---

## Trusted Types

Non activés : ils imposent des changements importants (notamment `innerHTML` et équivalents) et peuvent entrer en conflit avec AdSense. À envisager plus tard si le site n’utilise plus de scripts tiers.

---

## Vérifications après déploiement

1. Ouvrir une page en HTTPS et contrôler les headers (DevTools → Network → Headers).
2. Tester le calculateur (clic, entrée, résultats).
3. Tester le formulaire de contact si utilisé.
4. Vérifier que les annonces s’affichent correctement après l’activation d’AdSense.
