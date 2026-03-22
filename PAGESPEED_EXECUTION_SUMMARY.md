# PageSpeed Full Execution — LoanWiseCalc

## 1. Files audited

| File | Purpose |
|------|---------|
| `index.html` | Homepage structure, critical CSS, LCP elements |
| `style.css` | Colors, contrast, spacing, components |
| `script.js` | Calculator logic, init timing, DOM writes |
| `netlify.toml` | Build, security headers, caching |

---

## 2. Issues identified

### Accessibility (96)
- Liens et CTA avec contraste bleu (#2563eb) limite pour WCAG AA
- Liens des cartes sans soulignement, moins visibles

### Performance (99)
- DOM : divs superflus (ad-placeholder) sur la homepage
- Script : init synchrone pouvant prolonger les long tasks
- LCP : styles critiques incomplets pour le calculateur above-the-fold

### Security
- Headers déjà en place (CSP, HSTS, COOP, frame protection)
- Vérification faite : configuration correcte

---

## 3. Modifications appliquées

### A. Contraste (Accessibility)

| Élément | Avant | Après |
|--------|-------|-------|
| `--color-accent` | #2563eb (~5:1) | #1d4ed8 (~6.2:1) |
| `--color-accent-hover` | #1d4ed8 | #1e40af |
| Variables rgba | rgb(37,99,235) | rgb(29,78,216) |
| `.calc-card-cta` | Pas de soulignement | `text-decoration: underline` |

### B. Réduction du DOM (index.html)

- 3 blocs `ad-slot` : suppression des `<div class="ad-placeholder">` imbriqués
- Texte "Advertisement" directement dans `.ad-slot`
- ~3 nœuds DOM en moins sur la homepage

### C. Script (script.js)

- Remplacement de `requestAnimationFrame` par `requestIdleCallback` avec `timeout: 80`
- Init décalée en idle pour limiter les long tasks
- Fallback `requestAnimationFrame` si `requestIdleCallback` absent

### D. LCP (index.html – critical CSS)

- Ajout de `.calculator`, `.input-group`, `.input-group label` dans le critical CSS inline
- Le shell du calculateur est rendu dès le premier paint

### E. Security headers

- Aucun changement : CSP, HSTS, COOP, X-Frame-Options, Permissions-Policy déjà configurés

---

## 4. Extraits de code modifiés

### style.css
```css
/* Accent plus contrasté */
--color-accent: #1d4ed8;
--color-accent-hover: #1e40af;
--color-accent-subtle: rgba(29, 78, 216, 0.12);
/* ... autres rgba mis à jour */

/* CTA des cartes */
.calc-card-cta {
  text-decoration: underline;
  text-underline-offset: 2px;
}

/* Ad slot : plus de .ad-placeholder */
.ad-slot {
  /* font-size, color déplacés ici */
  font-size: 0.75rem;
  color: var(--color-text-muted);
  letter-spacing: 0.05em;
}
```

### index.html
```html
<!-- Critical CSS élargi -->
.calculator{background:#fff;border-radius:1rem;padding:1.5rem;border:1px solid #e2e8f0}
.input-group{margin-bottom:1.25rem}.input-group label{display:block;font-size:.875rem;font-weight:500;margin-bottom:.5rem}

<!-- Ad slots simplifiés -->
<div class="ad-slot ad-top" aria-label="Advertisement">Advertisement</div>
```

### script.js
```javascript
document.addEventListener('DOMContentLoaded', () => {
  const run = () => requestAnimationFrame(initCalculator);
  if ('requestIdleCallback' in window) {
    requestIdleCallback(run, { timeout: 80 });
  } else {
    requestAnimationFrame(run);
  }
});
```

---

## 5. Checklist de validation

### Local
- [ ] `npx serve .` ou `python -m http.server`
- [ ] Calcul : entrer montant, taux, durée → cliquer "Calculate"
- [ ] Résultats corrects (Monthly Payment, Total Payment, Total Interest)
- [ ] Navigation clavier (Tab, Enter) fonctionne
- [ ] Contraste : vérifier liens et boutons au survol/focus
- [ ] Mobile : layout correct, pas de débordement

### Netlify
- [ ] Déployer (git push ou build manuel)
- [ ] PageSpeed Insights sur l’URL de production
- [ ] Vérifier headers : DevTools → Network → sélectionner la page → Response Headers
  - `Content-Security-Policy`
  - `Strict-Transport-Security`
  - `X-Frame-Options: DENY`
  - `Cross-Origin-Opener-Policy: same-origin`
- [ ] Test du calculateur en production
- [ ] Pas d’erreurs console (CSP, 404, etc.)

### SEO / contenu
- [ ] Meta, canonical, schema JSON-LD inchangés
- [ ] Liens internes et structure du site intacts

---

## 6. Fichiers impactés

| Fichier | Changements |
|---------|-------------|
| `index.html` | Critical CSS, ad slots, accent dans :root |
| `style.css` | Accent, rgba, calc-card-cta, ad-slot |
| `script.js` | Init avec requestIdleCallback |
| `netlify.toml` | Aucun (déjà configuré) |

**Note :** Les autres pages HTML gardent la structure `<div class="ad-placeholder">` ; le CSS reste compatible. Seule la homepage a été simplifiée pour réduire le DOM.
