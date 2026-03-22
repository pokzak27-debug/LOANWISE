# Résumé des optimisations script.js

## Audit — causes potentielles de reflow / tâche longue

### 1. Pas de géométrie lue explicitement

Aucun appel à `offsetWidth`, `offsetHeight`, `getBoundingClientRect`, `clientWidth`, `scrollHeight` ou autre lecture de layout.

### 2. Écritures DOM entrelacées (risque de layout thrashing)

**Problème :** Dans `setResults` et `clearResults`, les écritures DOM (textContent, classList) étaient enchaînées de façon alternée (écriture 1 → écriture 2 → …). Chaque mutation peut déclencher un style recalc ; en enchaînant plusieurs types de mutations, le navigateur peut être contraint à recalculer le layout plus souvent.

**Pattern à risque :**

```
textContent (write) → classList.add (write, peut déclencher style recalc) → textContent (write) → …
```

### 3. Tâche longue à l’init

**Problème :** `initCalculator()` s’exécutait entièrement dans le callback `DOMContentLoaded`. Tout le travail (lectures DOM, création de fonctions, attachement d’événements) restait dans une seule tâche, bloquant le rendu initial.

### 4. Travail superflu sur les pages sans calculateur

**Problème :** Sur les pages sans calculateur (about, contact, terms, etc.), le script faisait 7 `getElementById` avant de tester `currencySelect` et sortir.

### 5. `forEach` avec callback pour peu d’éléments

**Problème :** Dans `clearResults`, `forEach` créait une nouvelle closure à chaque appel pour 3 éléments.

---

## Modifications effectuées

| Changement | Fichier | Effet |
|------------|---------|-------|
| Init différée avec `requestAnimationFrame` | L.9–12 | Réduit la longueur de la tâche à l’init et ne bloque pas le premier paint |
| Early bailout avant les autres `getElementById` | L.15–17 | Sur les pages sans calculateur, économise 6 appels DOM |
| Batches d’écritures DOM : d’abord tous les `textContent`, puis tous les `classList` | L.57–78 | Limite le style recalc et le layout thrashing |
| Pré-calcul des chaînes avant les écritures DOM | L.69–72 | Isole les calculs (formatCurrency) des mutations DOM |
| Callback `onEnterKey` partagé au lieu de 4 closures | L.108–120 | Moins de créations de fonctions |
| Boucle `for` au lieu de `forEach` pour les inputs | L.117–121 | Légère réduction des allocations |

---

## Risques de reflow identifiés et traités

1. **Écritures DOM entrelacées**  
   - Avant : `textContent` et `classList` alternés pour chaque élément.  
   - Après : toutes les mises à jour de `textContent` en premier, puis toutes les `classList`.

2. **Calculs mélangés aux écritures DOM**  
   - Avant : `formatCurrency` appelé au moment des écritures.  
   - Après : toutes les chaînes calculées avant toute mutation DOM.

3. **Init bloquante**  
   - Avant : `initCalculator` exécuté directement dans `DOMContentLoaded`.  
   - Après : exécution reportée à la prochaine frame avec `requestAnimationFrame`.

---

## Impact sur les performances (résumé)

- **First Paint / First Contentful Paint :** L’init est décalée au prochain frame, ce qui évite de bloquer le rendu initial.
- **Long tasks :** La tâche du `DOMContentLoaded` est plus courte ; le reste du travail se fait dans une tâche séparée.
- **Layout thrashing :** Réduction des recalculs de style grâce au regroupement des écritures DOM.
- **Pages sans calculateur :** Moins de lectures DOM inutiles grâce à l’early bailout.

---

## Comportement conservé

- Logique du calculateur et formules inchangées  
- Même rendu des résultats  
- Validation des champs inchangée  
- Comportement Enter et clic conservé  
- Compatibilité avec les pages sans calculateur (early return)
