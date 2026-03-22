# Phase Security — Production-Grade Headers

## Fichier de configuration : `netlify.toml`

Les en-têtes de sécurité sont déjà configurés dans `netlify.toml`. Récapitulatif :

---

## Headers configurés

| Header | Valeur | Rôle |
|--------|--------|------|
| **Content-Security-Policy** | Voir détail ci‑dessous | Restreint l’origine des scripts, styles, images, formulaires |
| **Strict-Transport-Security** | max-age=31536000; includeSubDomains; preload | Force HTTPS pendant 1 an |
| **X-Frame-Options** | DENY | Empêche l’inclusion en iframe (clickjacking) |
| **Referrer-Policy** | strict-origin-when-cross-origin | Limite les infos dans le Referer |
| **Permissions-Policy** | camera=(), microphone=(), geolocation=(), etc. | Désactive capteurs et APIs non utilisés |
| **Cross-Origin-Opener-Policy** | same-origin | Isole la page des fenêtres cross-origin |
| **X-Content-Type-Options** | nosniff | Empêche le MIME sniffing |

---

## Content-Security-Policy (détail)

| Directive | Valeur | Raison |
|-----------|--------|--------|
| default-src | 'self' | Par défaut, tout vient du même domaine |
| script-src | 'self' + Google (AdSense/GTM) + unsafe-inline unsafe-eval | Scripts du site + inline (onload) + AdSense |
| style-src | 'self' 'unsafe-inline' | CSS du site + critical CSS inline |
| img-src | 'self' data: https: | Images, data URIs, pixels analytics/pub |
| font-src | 'self' | Polices sur le même domaine |
| connect-src | 'self' + Google Analytics, GTM | XHR, fetch, analytics |
| frame-src | Google (AdSense) | Iframes publicitaires |
| frame-ancestors | 'none' | Aucun site ne peut afficher le site en iframe |
| form-action | 'self' | Formulaires uniquement vers le même domaine |
| base-uri | 'self' | Empêche les injections via `<base>` |
| object-src | 'none' | Bloque Flash, plugins, embeds |

---

## Compatibilité site actuel

- **style.css** : chargé depuis 'self' ✓
- **script.js** : chargé depuis 'self' ✓
- **Critical CSS inline** : style-src 'unsafe-inline' ✓
- **onload="this.media='all'"** : script-src 'unsafe-inline' ✓
- **JSON-LD** : type application/ld+json (non exécuté comme script) ✓
- **Formulaires (contact)** : form-action 'self' ✓

Aucun script externe n’est utilisé aujourd’hui. Les domaines Google (AdSense, GTM, Analytics) sont déjà inclus pour une future intégration.

---

## Vérifications après déploiement

1. Ouvrir une page en HTTPS → DevTools → Network → sélectionner la requête HTML → vérifier les Response Headers
2. Tester le calculateur (saisie, bouton, résultats)
3. Tester le formulaire de contact s’il existe
4. Vérifier qu’aucune erreur CSP n’apparaît dans la console

---

## HSTS Preload

Pour figer le site dans les listes de preload des navigateurs, soumettre le domaine sur [hstspreload.org](https://hstspreload.org). À faire uniquement lorsque le site sera définitivement servi en HTTPS sans redirection HTTP.
