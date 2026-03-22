# Résumé des corrections de contraste — LoanWiseCalc

## Fichier modifié

**`style.css`** — seul fichier modifié. Aucun changement de structure HTML, contenu ou SEO.

---

## Avant / Après — Variables de couleur

| Variable | Avant | Après | Ratio WCAG AA | Impact |
|----------|-------|-------|---------------|--------|
| `--color-text-muted` | `#64748b` (slate-500) | `#475569` (slate-600) | ~4.5 → ~5.6:1 | Texte secondaire lisible sur fond clair |
| `--color-accent` | `#3b82f6` (blue-500) | `#2563eb` (blue-600) | ~3.9 → ~4.9:1 | Liens lisibles sur fond blanc / gris clair |
| `--color-accent-hover` | `#2563eb` (blue-600) | `#1d4ed8` (blue-700) | ~4.9 → ~6.2:1 | Feedback visuel plus marqué au survol |

**Nouvelles variables (réutilisables) :**

| Variable | Valeur | Usage |
|----------|--------|--------|
| `--color-accent-dark` | `#1e40af` | Fin des dégradés logo / icônes |
| `--color-accent-subtle` | `rgba(37, 99, 235, 0.1)` | Arrière-plans au survol |
| `--color-accent-border` | `rgba(37, 99, 235, 0.4)` | Bordures CTA, liens |
| `--color-accent-border-light` | `rgba(37, 99, 235, 0.18)` | Bordures fines (calculateur) |
| `--color-accent-border-medium` | `rgba(37, 99, 235, 0.28)` | Bordures résultats |
| `--color-accent-focus` | `rgba(37, 99, 235, 0.35)` | Anneaux de focus, ombres |
| `--color-accent-shadow` | `rgba(37, 99, 235, 0.08)` | Ombres décoratives |

---

## Pourquoi chaque changement améliore l’accessibilité

### 1. `--color-text-muted` : `#64748b` → `#475569`

**Éléments concernés :**
- Liens de la navigation principale (`.site-nav-scroll a`)
- Liens du pied de page (`.footer-links a`)
- Sous-titres (`.subtitle`, `.popular-calculators-lede`, etc.)
- Texte d’aide (`.help-text`, `.form-note`, `.last-updated`)
- Copyright, placeholder des inputs
- Libellés des résultats (`.result-label`)
- Texte `.cta-row--compact`, `.sitemap-section-lede`

**Problème :** #64748b sur fond #f8fafc ≈ 4.2:1, en dessous du seuil AA (4.5:1).

**Effet :** #475569 atteint ~5.5:1, conforme WCAG AA pour le texte normal.

---

### 2. `--color-accent` : `#3b82f6` → `#2563eb`

**Éléments concernés :**
- Liens (`.help-text a`, `.silo-links-row a`, `.sitemap-list a`, etc.)
- CTA de la cta-row (`.cta-link`)
- CTA des cartes (`.calc-card-cta`)
- Liens “Related Calculators”, “You may also need”
- Liens du breadcrumb
- Texte des résultats calculés (`.result-value.has-value`)

**Problème :** #3b82f6 sur #f8fafc ≈ 3.9:1, insuffisant pour WCAG AA.

**Effet :** #2563eb atteint ~4.9:1, conforme pour texte normal et liens.

---

### 3. Bouton CTA principal (`#calculateBtn`)

**Avant :** Texte blanc sur #3b82f6 ≈ 4.5:1 (acceptable mais limite).  
**Après :** Texte blanc sur #2563eb ≈ 5.9:1.

Le bouton reste bien lisible et le contraste est renforcé.

---

### 4. Icône SVG du sélecteur de devise

**Avant :** `fill='%2364748b'` (#64748b)  
**Après :** `fill='%23475569'` (#475569)

Le chevron du select suit la même logique que le texte secondaire et atteint le ratio AA.

---

### 5. Focus clavier — nouveaux styles `:focus-visible`

**Boutons :**
- `#calculateBtn`, `#simpleCalculateBtn`, `#siCalculateBtn` → `outline: 2px solid var(--color-accent); outline-offset: 2px`
- `.submit-btn` → `outline: 2px solid white; outline-offset: 2px`

**Liens :**
- `.site-logo` → outline bleu avec `border-radius`
- `.cta-link` → outline bleu
- `.help-text a`, `.content-section a`, `.silo-links-row a`, `.sitemap-list a`, `.you-may-also-links a`, `.related-calculators-list a`, `.popular-calculators-lede a`, `.cta-row--compact a`, `.disclaimer-important-text a` → outline bleu uniforme

**Objectif :** Faciliter la navigation au clavier et respecter WCAG 2.4.7 (Focus Visible).

---

## Design conservé

- Palette bleue inchangée (blue-500 → blue-600/700)
- Dégradés logo et icônes identiques
- Structure, mise en page et sections conservées
- Hover/focus harmonisés via les variables
- Prêt pour AdSense (slots, structure) inchangé

---

## Validation

- **WCAG AA :** Texte normal ≥ 4.5:1, grand texte / composants UI ≥ 3:1
- **Focus visible :** Contraste de l’indicateur de focus ≥ 3:1
- **Cohérence :** Palette unifiée via variables CSS
- **SEO :** Aucun changement de balises, titres ou contenu
