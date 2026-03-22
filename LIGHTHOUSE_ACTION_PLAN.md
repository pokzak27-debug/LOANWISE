# LoanWiseCalc — Plan d’action Lighthouse / PageSpeed

**Objectif :** Corriger les problèmes Lighthouse sans impacter le design, le SEO ou la préparation AdSense.

**Audit actuel :** Performance 99 · Accessibilité 96 · Best Practices 100 · SEO 100

---

## 1. Cartographie des fichiers

| Composant | Fichiers principaux | Notes |
|-----------|---------------------|-------|
| **CTA / boutons / liens homepage** | `style.css` (lignes 768–778, 1127–1153), `index.html` (lignes 340–387) | `.cta-link`, `.cta-row`, `.calc-card-cta` |
| **Cartes calculateur** | `style.css` (lignes 623–676), `index.html` (lignes 278–337) | `.calc-card`, `.popular-calculators-grid` |
| **Sitemap-list / grandes sections de liens** | `style.css` (lignes 921–936), `index.html` (lignes 203–224), `sitemap.html` (entier) | `.sitemap-list`, `ul.sitemap-list` |
| **Script de calcul** | `script.js` (entier) | `initCalculator()`, `handleCalculate()`, `setResults()` |
| **Headers de déploiement** | `netlify.toml` (lignes 6–22) | `[[headers]]` pour HTML, CSS, JS |

**Fichiers à modifier en priorité :**
1. `style.css` — contraste, variables CSS
2. `script.js` — tâche principale, éventuel layout thrashing
3. `netlify.toml` — en-têtes de sécurité
4. `index.html` — structure DOM, sections dupliquées
5. `templates/page_template.html` — pour les pages générées (si applicable)

---

## 2. QUICK WINS

### 2.1 Contraste des liens et CTA (Accessibilité 96 → 100)

**Problème :** Lighthouse signale un contraste insuffisant sur plusieurs liens/CTA.

**Sélecteurs concernés (à ajuster dans `style.css`) :**

| Sélecteur | Variable actuelle | Problème | Lignes |
|-----------|-------------------|----------|--------|
| `.site-nav-scroll a` | `--color-text-muted` (#64748b) | Gris sur fond clair, ratio ~4.5 | 130–139 |
| `.footer-links a` | `--color-text-muted` (#64748b) | Idem | 231–246 |
| `.cta-link` | `--color-accent` (#3b82f6) | Bleu sur fond gris clair, ~3.9 | 768–778 |
| `.calc-card-cta` | `--color-accent` (#3b82f6) | Idem | 663–671 |
| `.silo-links-row a` | `--color-accent` | Idem | 880–887 |
| `.sitemap-list a` | `--color-accent` | Idem | 920–927 |
| `.help-text a`, `.content-section a` | `--color-accent` | Idem | 800–811 |

**Action recommandée :** Assombrir `--color-text-muted` et `--color-accent` pour atteindre ≥4.5:1 (texte normal) et ≥3:1 (grand texte/CTA).

- `--color-text-muted` : passer de `#64748b` à `#475569` (slate-600) ou `#334155` (slate-700)
- `--color-accent` : passer de `#3b82f6` à `#2563eb` (blue-600) ou `#1d4ed8` (blue-700)
- Ou utiliser des `border`/`background` plus foncés pour les CTA

**Fichier :** `style.css` — lignes 7–19 (variables `:root`) et les règles ci-dessus.

---

### 2.2 En-têtes de sécurité (Best Practices)

**Problème :** Manque de CSP, HSTS, COOP, protection anti-frame renforcée.

**Action :** Étendre `netlify.toml` (voir section 4 ci-dessous).

---

### 2.3 Chargement inutile de `script.js`

**Problème :** Les pages sans calculateur (about, contact, privacy-policy, terms, sitemap) chargent `script.js` alors qu’elles n’ont pas `#currency`.

**Action :** Supprimer `<script src="script.js" defer></script>` des pages statiques qui n’utilisent pas le calculateur, ou implémenter un chargement conditionnel.

**Fichiers :** `about.html`, `contact.html`, `privacy-policy.html`, `terms.html`, `sitemap.html` (+ pages similaires générées par template).

---

## 3. SAFE REFACTORS

### 3.1 Réduction de la taille du DOM

**Problème :** DOM trop volumineux (cible Lighthouse : <1500 nœuds).

**Sources principales sur `index.html` :**

1. **Sections redondantes**
   - `.popular-calculations` (l.203–224) et `.popular-calculators` (l.276–337) se chevauchent fortement.
   - Fusionner ou limiter à une seule section “Popular Calculators”.

2. **CTA row dupliqué**
   - `.cta-row` (l.340–387) : 13 blocs CTA répétitifs, déjà couverts par les calc-cards.
   - Réduire à 3–5 liens principaux ou remplacer par une grille compacte.

3. **Footer**
   - 7 colonnes × nombreux liens.
   - Réduire les liens par colonne ou regrouper certaines catégories.

4. **Sitemap-list homepage**
   - 21 liens dans “Popular Calculations”.
   - Réduire à 10–12 liens les plus stratégiques.

**Fichiers :** `index.html` principalement ; vérifier les templates si régénération.

---

### 3.2 Longue tâche JS et layout thrashing

**Problème :** Une longue tâche sur le main thread et/ou layout thrashing dans `script.js`.

**Comportement actuel :**
- `initCalculator()` s’exécute entièrement au `DOMContentLoaded`.
- `setResults()` fait 6 accès au DOM (3 `textContent` + 3 `classList.add`).
- `clearResults()` fait un `forEach` avec `classList.remove`.

**Actions recommandées :**
1. Découper le travail avec `scheduler.yield()` ou `setTimeout(0)` si supporté, ou `requestIdleCallback` pour les mises à jour non critiques.
2. Regrouper les mises à jour DOM : utiliser un `DocumentFragment` ou faire toutes les lectures d’abord, puis toutes les écritures.
3. Utiliser `requestAnimationFrame` pour les mises à jour visuelles si besoin.

**Fichier :** `script.js` — fonctions `setResults`, `clearResults`, `handleCalculate`.

---

### 3.3 Sitemap HTML

**Problème :** `sitemap.html` contient ~150+ liens sur une seule page, ce qui alourdit le DOM.

**Action :** Garder la structure actuelle pour l’indexation, mais envisager une pagination ou une mise en avant progressive (ex. “load more”) pour les sections moins prioritaires — uniquement si cela ne nuit pas au SEO. Optionnel et à valider en A/B.

**Fichier :** `sitemap.html`.

---

## 4. SECURITY HEADERS

**Fichier :** `netlify.toml`

**État actuel :** `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy` sur HTML.

**À ajouter :**

```toml
# Exemple — à adapter selon besoins AdSense/CSP
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Permissions-Policy = "camera=(), microphone=(), geolocation=()"
    # HSTS — activer uniquement en HTTPS
    Strict-Transport-Security = "max-age=31536000; includeSubDomains; preload"
    # COOP — isolement du document
    Cross-Origin-Opener-Policy = "same-origin"
    # CSP — permettre scripts inline si AdSense en a besoin
    Content-Security-Policy = "default-src 'self'; script-src 'self' https://pagead2.googlesyndication.com https://google.com https://www.google.com 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; frame-src https://googleads.g.doubleclick.net;"
```

**Points importants :**
- Adapter CSP pour AdSense (`pagead2.googlesyndication.com`, `doubleclick.net`, etc.).
- Tester après déploiement pour vérifier que les pubs s’affichent.
- Trusted Types : optionnel pour l’instant, peut compliquer l’intégration AdSense.

---

## 5. VALIDATION CHECKLIST

Après chaque modification :

- [ ] **Performance** : Lighthouse Performance ≥99
- [ ] **Accessibilité** : Lighthouse Accessibility = 100 (contraste)
- [ ] **SEO** : Titres, meta, canonicals, structure inchangés
- [ ] **Design** : Aucune régression visuelle notable
- [ ] **AdSense** : Placeholders et structure prêts ; CSP compatible si AdSense actif
- [ ] **Mobile** : Test sur viewport 375px
- [ ] **Scripts** : Calculateur fonctionnel sur index et pages outils
- [ ] **Liens internes** : Aucun lien cassé après réduction du DOM

---

## 6. Ordre d’exécution recommandé

| Étape | Action | Fichiers | Risque |
|-------|--------|----------|--------|
| 1 | Ajuster les variables de contraste | `style.css` | Faible |
| 2 | Ajouter les security headers | `netlify.toml` | Moyen (CSP/AdSense) |
| 3 | Retirer `script.js` des pages statiques | 5+ HTML | Faible |
| 4 | Découper/yield dans `script.js` | `script.js` | Faible |
| 5 | Regrouper mises à jour DOM dans `script.js` | `script.js` | Faible |
| 6 | Fusionner Popular Calculations / Popular Calculators | `index.html` | Moyen |
| 7 | Réduire `.cta-row` | `index.html` | Moyen |
| 8 | Réduire sitemap-list homepage | `index.html` | Faible |
| 9 | Alléger footer (optionnel) | `index.html` + templates | Moyen |

---

*Document généré le 22 mars 2026 — Phase ANALYZE + PLAN (aucun code modifié).*
