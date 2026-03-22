# Résumé de la refactorisation DOM — Homepage LoanWiseCalc

## Fichiers modifiés

- **`index.html`** — structure simplifiée, sections redondantes supprimées
- **`style.css`** — ajustements pour `.trust-point` (grid), `.silo-links-intro` (inline)

---

## Éléments supprimés

| Élément | Nœuds approximatifs | Raison |
|---------|---------------------|--------|
| **CTA row** | ~40 | Doublon des calc-cards : mêmes 13 liens déjà dans les cartes Popular Calculators |
| **Section Popular Calculations** | ~27 | Doublon : liens déjà dans calc-cards, silo-links, help-text et footer |
| **Section Related Calculators** | ~14 | Doublon : tous les liens déjà ailleurs (calc-cards, footer) |
| **Wrappers div dans trust-point** | 4 | Remplacés par une grille CSS sans wrapper |
| **Paragraphe silo-links-intro** | 1 | Fusionné dans `.silo-links-row` en `<strong>` inline |

**Total supprimé :** ~86 nœuds DOM

---

## Conservé pour le SEO

| Composant | Contenu conservé |
|-----------|------------------|
| **Header nav** | 17 liens vers tous les principaux calculateurs et pages |
| **Help-text** | 7 liens inline (car, auto, personal, business, mortgage, interest, simple interest) |
| **Silo-links** | 9 liens ($5k, $10k, $20k, Down payment, Extra payments, Interest breakdown, How to calculate, USA, UK) |
| **Popular Calculators (calc-cards)** | 13 cartes avec h3, description et CTA vers car, auto, personal, business, mortgage, interest, simple interest, USA, UK, Canada, UAE, Morocco, Australia |
| **Popular calculators lede** | 6 liens inline (comparison, how much afford, car monthly, mortgage 30-year, interest breakdown, simple example) |
| **Contenu section** | Liens internes dans "How to use" (car, mortgage, personal, business, USA, UK) |
| **Disclaimer** | Liens car, mortgage, personal |
| **Footer** | 7 colonnes, ~60 liens vers tous les types de calculateurs, pays et pages légales |
| **Schema FAQ** | JSON-LD inchangé |
| **H1, H2, meta, canonical** | Inchangés |

**Crawlabilité :** Toutes les pages principales restent accessibles depuis la homepage (nav, silo, calc-cards, footer, sitemap).

---

## Réduction du DOM

| Métrique | Avant | Après | Gain |
|----------|-------|-------|------|
| Nœuds (start tags) | ~468 | ~382 | **~86 nœuds (~18 %)** |

---

## Structure sémantique conservée

- `<main>` pour le calculateur
- `<section>` pour trust, how-to, disclaimer, popular calculators
- `<nav>` pour breadcrumb, silo-links, footer-map
- `<ul>` / `<li>` pour trust-points
- `<dl>` / `<dt>` / `<dd>` pour FAQ et définitions
- Attributs `aria-labelledby`, `aria-label`, `aria-current` inchangés

---

## Visuel

- Mise en page inchangée
- Trust points : grille CSS à la place des wrappers div, rendu identique
- Silo-links : « In this section: » en inline avec les liens (plus compact)
- Calc-cards, ad slots, footer inchangés
