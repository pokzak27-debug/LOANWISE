# CTR Boost — Conversion Improvements

Phase **CTR Boost** : maximise les clics vers les pages de calculateurs.

---

## 1. CTA principal

### Changements
- **Texte** : "Calculate now" → **"Calculate Your Loan Now"** (action plus claire)
- **Visibilité above-the-fold** : Hero compact, CTA visible sans scroll
- **Contraste** : Bouton avec gradient bleu foncé (#1d4ed8 → #1e3a8a), texte blanc, ombre accentuée
- **Taille** : `1.125rem` / `1.25rem` padding pour une surface cliquable confortable

### Impact
- Message orienté bénéfice utilisateur
- Contraste WCAG AA (blanc sur bleu foncé)
- Meilleure détectabilité visuelle

---

## 2. Cartes calculateurs

### Changements
- **Carte entière cliquable** : `<a class="category-card">` englobe tout le contenu
- **Hover** : bordure accent, ombre bleutée (`0 12px 32px rgba(29, 78, 216, 0.2)`), `translateY(-4px)`
- **État actif** : `translateY(-2px)` pour feedback tactile
- **CTA dans la carte** : "Calculate Your Loan Now" avec `margin-top: auto` pour rester en bas

### Impact
- Zone cliquable élargie (Fitts's Law)
- Feedback visuel immédiat au survol
- Hiérarchie claire : titre → description → action

---

## 3. Trust

### Changements
- **Phrase trust** : "Free • No signup • Instant results" dans le hero, au-dessus du CTA
- Répétée près du bouton Calculate et dans la section trust
- Style : `hero-trust` / `trust-badges` — couleur accent, gras

### Impact
- Réduction de la friction perçue
- Réassurance avant l’action
- Différenciation vs solutions payantes / inscription

---

## 4. Moins de distractions

### Changements
- **Nav** : 6 liens → 4 (Home, Car Loan, Mortgage, All calculators)
- **Internal links** : section dé-emphasisée — titre plus petit, couleur `--color-text-muted`, espacement réduit
- **Hiérarchie** : hero → calculator → top calculators → trust → internal links

### Impact
- Moins de concurrence avec le CTA
- Un seul parcours dominant : calculer son prêt
- Décision simplifiée (single primary action)

---

## 5. Synthèse technique

| Élément | Avant | Après |
|--------|-------|-------|
| CTA hero | "Calculate now" | "Calculate Your Loan Now" |
| CTA cartes | "Calculate now" | "Calculate Your Loan Now" |
| Nav links | 6 | 4 |
| Hover cartes | translateY(-3px) | translateY(-4px) + ombre accentuée |
| Internal links | Titre standard | Titre réduit, couleur atténuée |

---

## Fichiers modifiés

- `index.html` — hero, cartes, nav, trust
- `style.css` — `.cta-primary`, `.category-card`, `.internal-links-section`
