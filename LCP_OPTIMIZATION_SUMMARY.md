# Résumé des optimisations LCP — Homepage Hero

## Contexte

- **LCP candidate :** `.intro-lead` (texte principal sous le H1)
- **Objectif :** Réduire le délai d’affichage du hero (header + titre + intro)

---

## Audit — sources de retard

| Cause | Détail |
|-------|--------|
| **CSS bloquant** | `style.css` bloquait le rendu tant qu’il n’était pas chargé et parsé |
| **JSON-LD dans le head** | ~2 KB de script inline avant le body, ralentissant l’accès au contenu |
| **Ordre de parsing** | Head volumineux avant le body, report du premier rendu |
| **Pas de police web** | Utilisation de `system-ui` uniquement → pas de FOIT/FOUT |
| **Pas d’animations** | Aucune transition/animation sur le hero → pas de retards liés |

---

## Modifications effectuées

### 1. Critical CSS inline

Un bloc `<style>` dans le `<head>` contient les règles minimales pour le hero :
- Reset (*, :root, variables)
- `body`, `.container`, `.site-header`, nav, logo
- `.breadcrumb`, `.page-header`, `h1`, `.subtitle`, `.intro-lead`, `.last-updated`
- Media queries (480px, 520px, 640px) pour le hero

**Effet :** Le navigateur peut afficher le hero dès la fin du parsing du HTML, sans attendre `style.css`.

### 2. Chargement non bloquant de `style.css`

```html
<link rel="preload" href="style.css" as="style" fetchpriority="high">
<link rel="stylesheet" href="style.css" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="style.css"></noscript>
```

- **preload + fetchpriority="high"** : priorité de téléchargement du CSS
- **media="print" puis onload → media="all"** : chargement asynchrone, sans blocage du rendu
- **noscript** : fallback pour les visiteurs sans JavaScript

**Effet :** La page n’est plus bloquée par le CSS pour le premier rendu.

### 3. JSON-LD déplacé en fin de body

Le script FAQ Schema est déplacé juste avant `script.js`, en bas de page.

**Effet :** Head plus léger, parsing du body plus tôt.

---

## Impact sur le LCP

- **Avant :** Le rendu attendait le chargement complet de `style.css`.
- **Après :** Le hero s’affiche dès que le HTML est parsé, grâce au critical CSS inline.
- **CLS :** Aucun changement de mise en page, le critical CSS reprend les mêmes dimensions et espacements que le CSS complet.

---

## Fichier modifié

**`index.html`** — uniquement la homepage (les autres pages restent inchangées).

---

## Comportement conservé

- Même rendu visuel du hero
- Texte et structure inchangés
- Schema FAQ JSON-LD toujours présent et exploitable
- Fallback pour navigateurs sans JavaScript
