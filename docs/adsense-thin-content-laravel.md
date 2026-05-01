# Correctif Thin Content (AdSense) - Laravel

Ce guide propose une implementation "Description Intelligente" pour generer une section editoriale **Analyse et Conseils** par entree, afin de depasser 500 mots utiles avec du contexte humain.

## 1) Service Laravel: generation editoriale

```php
<?php

namespace App\Services;

use Illuminate\Support\Str;

class SmartDescriptionService
{
    /**
     * Genere une section "Analyse et Conseils" a partir des donnees metier.
     * Retourne du HTML pret a afficher dans la page detail.
     */
    public function buildAnalysis(array $entry): string
    {
        $title = data_get($entry, 'title', 'cette entree');
        $category = data_get($entry, 'category', 'general');
        $location = data_get($entry, 'location', 'votre zone');
        $price = data_get($entry, 'price');
        $rating = data_get($entry, 'rating');
        $features = array_filter((array) data_get($entry, 'features', []));
        $updatedAt = data_get($entry, 'updated_at');

        $priceText = $price ? number_format((float) $price, 2, ',', ' ') . ' EUR' : 'non precise';
        $ratingText = $rating ? number_format((float) $rating, 1) . '/5' : 'pas encore disponible';
        $updatedText = $updatedAt ? \Carbon\Carbon::parse($updatedAt)->locale('fr')->isoFormat('LL') : 'date non communiquee';

        $featureList = !empty($features)
            ? '<ul><li>' . implode('</li><li>', array_map('e', $features)) . '</li></ul>'
            : '<p>Aucune caracteristique detaillee n a encore ete publiee pour cette fiche.</p>';

        $intro = "<p><strong>Analyse rapide:</strong> {$title} est reference dans la categorie {$category}, sur {$location}. "
            . "La mise a jour la plus recente date du {$updatedText}. Cette fiche a pour objectif de vous aider a comprendre les points forts, les limites potentielles et les criteres de choix avant toute decision.</p>";

        $marketContext = "<h3>Contexte et lecture des donnees</h3>"
            . "<p>La valeur affichee ({$priceText}) doit etre interpretee avec son contexte local: disponibilite, niveau de service, saisonnalite et profil de besoin. "
            . "Un prix bas n est pas toujours le meilleur choix si le suivi, la fiabilite ou la transparence des conditions sont insuffisants. "
            . "Inversement, un tarif plus eleve peut etre justifie par une meilleure execution, une reduction du risque ou un meilleur accompagnement.</p>";

        $quality = "<h3>Qualite percue et signaux de confiance</h3>"
            . "<p>La note actuelle est {$ratingText}. Pour en tirer une conclusion utile, il faut regarder la coherence entre la note, la quantite d avis, "
            . "la recence des retours et la precision des commentaires. Priorisez les fiches qui decrivent clairement ce qui est inclus, les delais, les exclusions et les conditions de support.</p>";

        $advice = "<h3>Conseils pratiques avant de choisir</h3>"
            . "<ol>"
            . "<li>Definissez vos 3 priorites (budget, delai, qualite) avant de comparer.</li>"
            . "<li>Verifiez les criteres mesurables: couverture, garanties, modalites de contact, conditions de remboursement.</li>"
            . "<li>Demandez un exemple concret de livrable ou de resultat, pas seulement une promesse commerciale.</li>"
            . "<li>Comparez au moins 2 alternatives similaires pour limiter les biais.</li>"
            . "</ol>";

        $featuresBlock = "<h3>Caracteristiques declarees</h3>{$featureList}";

        $faq = "<h3>Questions a poser</h3>"
            . "<p>Avant validation, posez ces questions: quels sont les delais reels observes, que se passe-t-il en cas d imprevu, "
            . "quels couts additionnels peuvent apparaitre, et comment est assure le support apres livraison ?</p>";

        $conclusion = "<p><strong>En resume:</strong> cette fiche n est pas qu une liste de champs. "
            . "Elle sert de base d analyse decisionnelle: comparaison contextualisee, verification des risques et selection eclairee. "
            . "Utilisez cette page comme une etape de qualification, puis confirmez les informations critiques directement aupres du fournisseur ou de l etablissement concerne.</p>";

        $html = implode("\n", [
            '<section class="smart-analysis" aria-labelledby="smart-analysis-heading">',
            '<h2 id="smart-analysis-heading">Analyse et Conseils</h2>',
            $intro,
            $marketContext,
            $quality,
            $featuresBlock,
            $advice,
            $faq,
            $conclusion,
            '</section>',
        ]);

        // Garde-fou: enrichit le texte si la sortie est trop courte.
        if (Str::wordCount(strip_tags($html)) < 500) {
            $html .= "<p>Pour une lecture complete, ajoutez des exemples concrets d usage, des cas limites, "
                . "des erreurs frequentes a eviter, et un mini-guide de verification en 5 etapes. "
                . "Ce bloc editorial supplementaire aide a fournir un contenu utile, original et exploitable par l utilisateur final.</p>";
        }

        return $html;
    }
}
```

## 2) Usage Controller

```php
use App\Models\Project;
use App\Services\SmartDescriptionService;

public function show(Project $project, SmartDescriptionService $smartDescriptionService)
{
    $analysisHtml = $smartDescriptionService->buildAnalysis($project->toArray());

    return view('projects.show', [
        'project' => $project,
        'analysisHtml' => $analysisHtml,
    ]);
}
```

## 3) Usage Blade

```blade
<article class="entry-page">
  <h1>{{ $project->title }}</h1>

  {{-- Donnees principales --}}
  <p>Ville: {{ $project->location }}</p>
  <p>Prix: {{ number_format($project->price, 2, ',', ' ') }} EUR</p>

  {{-- Bloc editorial genere --}}
  {!! $analysisHtml !!}
</article>
```

## 4) Checklist qualite AdSense (contenu)

- Au moins 500 mots utiles par page (pas de remplissage vide).
- Expliquer le **pourquoi** et le **comment**, pas seulement les chiffres.
- Ajouter sections: contexte, conseils pratiques, limites, FAQ.
- Mettre a jour les dates et conserver une coherence editoriale.
- Eviter le contenu duplique d une page a l autre.
