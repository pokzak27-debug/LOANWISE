# Homepage Desktop Audit & Optimization Plan — LoanWiseCalc

**Phase:** ANALYZE (DESKTOP FOCUS)  
**Goal:** Conversion, SEO internal linking quality, premium UX perception  
**Focus:** Structure clarity, hierarchy, reducing overload — NOT speed

---

## 1. Audit — Current Layout (Top to Bottom)

### Above the Fold (≈1080px viewport, ~600–700px scroll)

| Section | Content | Links |
|---------|---------|-------|
| **Header** | Logo + nav | **18 links**: Home, Car Loan, Auto Loan, Personal Loan, Business Loan, Mortgage, Interest, Simple Interest, USA, UK, Canada, UAE, Morocco, Australia, About, Contact, Privacy Policy, Sitemap, Terms |
| **Breadcrumb** | "Home" | 0 (current page only) |
| **Hero** | H1, subtitle, intro-lead, last-updated | 0 |
| **Ad top** | Placeholder | 0 |
| **Calculator** | 4 inputs, button, 3 result cards | 0 |
| **Help text** | "Need a specialized tool? Try…" | **5 links**: car, auto, personal, mortgage, interest |

**Above-fold link count: 23 links** (18 nav + 5 help-text)

### Below the Fold

| Section | Content | Links | Notes |
|---------|---------|-------|-------|
| **Trust (Why use LoanWise)** | 4 trust-point cards | 0 | Value props, no links |
| **Popular calculators** | 13 calc-cards | **13 links** | Car, Auto, Personal, Business, Mortgage, Interest, Simple Interest, USA, UK, Canada, UAE, Morocco, Australia |
| **How to use** | 4-step ordered list | 0 | Instructional |
| **Disclaimer** | 2 paragraphs | **3 links**: car, mortgage, personal | Contextual |
| **Explore links** | Single-line nav | **5 links**: $10k, $20k, Down payment, USA, UK | Silo links |
| **Content** | Formula, example, factors, definitions | **6 links**: car, mortgage, personal, business, USA, UK | Inline in prose |
| **Ad middle** | Placeholder | 0 | |
| **Ad bottom** | Placeholder | 0 | |
| **Footer** | 7 columns | **~52 links** | Sitemap-style |

---

## 2. Link Duplication Map

### Core calculator pages — occurrence count

| Page | Header | Help-text | Popular grid | Disclaimer | Explore | Content | Footer |
|------|--------|-----------|--------------|------------|---------|---------|--------|
| car-loan | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ |
| auto-loan | ✓ | ✓ | ✓ | — | — | — | ✓ |
| personal-loan | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ |
| mortgage | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ |
| interest | ✓ | ✓ | ✓ | — | — | — | ✓ |
| business-loan | ✓ | — | ✓ | — | — | ✓ | ✓ |
| simple-interest | ✓ | — | ✓ | — | — | — | ✓ |
| USA | ✓ | — | ✓ | — | ✓ | ✓ | ✓ |
| UK | ✓ | — | ✓ | — | ✓ | ✓ | ✓ |
| Canada | ✓ | — | ✓ | — | — | — | ✓ |
| UAE | ✓ | — | ✓ | — | — | — | ✓ |
| Morocco | ✓ | — | ✓ | — | — | — | ✓ |
| Australia | ✓ | — | ✓ | — | — | — | ✓ |

### Redundancy summary

- **car-loan**: 6 zones
- **personal-loan, mortgage**: 6 zones each
- **USA, UK**: 5 zones each
- **auto-loan, interest**: 4 zones each

---

## 3. Identified Issues

### 3.1 Too many links above the fold

- **18 nav links** on desktop: Calculator types + country pages + legal/company
- **5 help-text links** repeating car, auto, personal, mortgage, interest
- **Total 23 links** before first scroll
- **Impact:** Overload visuel, dilution du focus, aspect "SEO spammy"

### 3.2 Duplicate link zones

- **Help text** et **Popular calculators grid** : mêmes 5 calculateurs (car, auto, personal, mortgage, interest)
- **Disclaimer** : car, mortgage, personal (déjà dans nav + help + grid)
- **Explore** : USA, UK (déjà dans nav + popular grid)
- **Content prose** : car, mortgage, personal, business, USA, UK (déjà présents ailleurs)

### 3.3 Sitemap-style blocks

- **Footer** : 7 colonnes, ~52 liens — structure type sitemap
- **Popular calculators** : 13 cartes — principal bloc de liens
- **Explore links** : mini-sitemap (5 liens)

### 3.4 CTA repetition

- **13× "Calculate free now"** sur chaque calc-card
- Message répétitif, peu différencié

### 3.5 Sections "spammy"

- **Help text** : phrase courte avec 5 liens inline → aspect listicle
- **Explore links** : "Explore: $10k · $20k · Down payment · USA · UK" → liste de liens bruts
- **Footer** : trop de colonnes visibles d’un coup sur desktop

### 3.6 Containers / DOM

- **site-header-inner** > **site-nav** > **site-nav-scroll** : 3 niveaux pour le header
- **footer-map** > **footer-col** (×7) > **footer-links** > **li** > **a** : imbrication profonde
- Containers nécessaires pour la mise en page ; peu de gains possibles sans refonte

### 3.7 Hiérarchie

- Hero → Calculator → Help text (liens) → Trust → Popular calculators
- La zone **Trust** pourrait être mieux mise en avant avant les liens
- **How to use** (4 étapes) redondant avec l’interface évidente du calculateur

---

## 4. Optimization Plan

### KEEP (important for SEO and conversion)

| Element | Reason |
|---------|--------|
| **Calculator block** | Cœur produit, conversion |
| **Popular calculators grid** | Bloc principal de liens internes, silo, conversion |
| **Trust section** | Crédibilité, réduction du bounce |
| **Footer** | Sitemap SEO, crawl, UX classique |
| **Content section** (formula, example, FAQ) | Contenu long-form SEO, E-E-A-T |
| **Breadcrumb** | Navigation, SEO |
| **Schema FAQ** | Rich results, SEO |
| **Disclaimer** | Conformité, transparence |

### SIMPLIFY (réduire la répétition)

| Element | Action | Impact SEO |
|---------|--------|------------|
| **Header nav** | Réduire à 6–8 liens prioritaires : Home, Car Loan, Personal Loan, Mortgage, USA, About, Sitemap. Déplacer le reste dans un menu "More" ou dans le footer | Faible — footer conserve les liens |
| **Help text** | Remplacer par une phrase sans liens, ou 1–2 liens max. Ex: "Need a car or mortgage calculator? Browse our tools below." | Faible — popular grid conserve les liens |
| **Disclaimer links** | Garder 1 lien (ex. car loan calculator) au lieu de 3 | Faible |
| **Content prose links** | Réduire à 2–3 liens contextuels au lieu de 6 | Faible |
| **Explore links** | Garder uniquement les silo amount/category ($10k, $20k, Down payment). Retirer USA, UK (déjà dans popular grid) | Neutre |
| **CTA "Calculate free now"** | Varier : "Get estimate" / "Try now" / "Calculate" selon le type de calculatrice | Aucun |
| **Popular calculators** | Regrouper en 2 sous-sections : "By type" (car, auto, personal, business, mortgage, interest, simple interest) et "By region" (USA, UK, Canada, UAE, Morocco, Australia). Ou afficher 6–8 cartes principales + "View all" vers sitemap | Faible — liens conservés sur sitemap |

### REMOVE (duplication inutile)

| Element | Action | Impact SEO |
|---------|--------|------------|
| **Help-text links (5)** | Supprimer ou remplacer par texte non lié. Les mêmes pages sont dans popular grid et footer | Aucun — liens présents ailleurs |
| **How to use (4 steps)** | Supprimer si la maquette est jugée suffisamment évidente. Ou condenser en 1 paragraphe court | Aucun |
| **Explore: USA, UK** | Retirer — déjà dans popular grid + footer | Aucun |
| **Redundant content links** | Supprimer 3–4 des 6 liens dans "How to use this for real decisions" | Faible |

### RESTRUCTURE (meilleure hiérarchie)

| Change | Rationale |
|--------|-----------|
| **Hero → Calculator → Trust → Popular calculators** | Mettre Trust juste après le calculateur pour renforcer la crédibilité avant la découverte d’outils |
| **Help text** : déplacer ou fusionner | Si conservé, le placer après Trust, ou l’intégrer au lede de Popular calculators |
| **Popular calculators** : 2 blocs visuels | "Top tools" (6 cartes) + "More calculators" (7 cartes en grille plus compacte) pour clarifier la hiérarchie |
| **Footer** : collapse sur desktop | Sur desktop, afficher 3–4 colonnes principales. Les autres dans un bloc "More calculators" repliable (accordion) ou lien vers Sitemap |
| **Nav** : groupement | Grouper visuellement : [Home] [Car Loan] [Personal] [Mortgage] | [USA] [UK] | [About] [Sitemap] pour réduire la perception de "mur de liens" |

---

## 5. Recommended Priority Order

### Phase 1 — Quick wins (faible risque SEO)
1. **Simplify help text** : remplacer les 5 liens par une phrase sans liens ou 1 lien
2. **Simplify explore links** : retirer USA, UK
3. **Simplify disclaimer** : 1 lien au lieu de 3
4. **Simplify content prose** : 2–3 liens au lieu de 6

### Phase 2 — Restructure
5. **Reorder** : Hero → Calculator → Trust → Popular calculators
6. **Popular calculators** : subdivision "Top tools" vs "More" (optionnel)

### Phase 3 — Nav & footer (plus impactant)
7. **Header nav** : réduire à 8–10 liens prioritaires
8. **Footer** : simplifier ou regrouper les colonnes sur desktop

---

## 6. Summary

| Metric | Current | Target (perception) |
|--------|---------|---------------------|
| Above-fold links | 23 | 10–14 |
| Link zones for car-loan | 6 | 3–4 |
| CTA repetition | 13× identical | 3–4 variants |
| Sections before calculator | 2 (hero, ad) | 2 (unchanged) |
| Trust placement | After help-text | After calculator |

**Principle:** Garder la valeur SEO (liens dans popular grid, footer, content) tout en réduisant la répétition et la surcharge visuelle pour une UX plus premium et conversion-oriented.
