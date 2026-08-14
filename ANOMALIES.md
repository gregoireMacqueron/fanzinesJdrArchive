# Manquants, erreurs et anomalies de migration

État établi le 14 août 2026 à partir du dump MediaWiki et du dossier d’images
disponibles dans `sources/`.

Les rapports exhaustifs et lisibles par une machine sont disponibles dans :

- `reports/image-manifest.json` pour les images ;
- `reports/content-migration.json` pour les pages et les redirections.

## Synthèse

| Élément | Résultat |
| --- | ---: |
| Pages de l’espace principal analysées | 278 |
| Pages Markdown produites | 254 |
| Redirections identifiées | 21 |
| Pages techniques explicitement exclues | 3 |
| Pages vides | 7 |
| Fichiers image sources | 1 495 |
| Images classées par publication | 1 378 |
| Images partagées | 10 |
| Images restant à classer | 107 |
| Références d'images réécrites | 2 875 |
| Références d’images manquantes | 3 occurrences, 2 fichiers |
| Groupes de doublons binaires | 6 |
| Tableaux MediaWiki convertis en Markdown | 1 543 |
| Fermetures de tableau orphelines supprimées | 1 |

## Fichiers image manquants

Deux fichiers référencés par le contenu n’ont pas été retrouvés dans les
sources :

| Article | Fichier attendu | Occurrences |
| --- | --- | ---: |
| Ars Mag | `TheTribunalOfLochLegleanMap(300ppp-Portrait).png` | 2 |
| Antre du Dragon (L') | `AntreDuDragon10.jpg` | 1 |

Les liens d’origine sont volontairement conservés dans les fichiers Markdown
concernés, afin que l’anomalie reste visible et puisse être réparée plus tard.

## Pages vides

Ces pages existent dans MediaWiki, mais leur dernière révision ne contient
aucun contenu exploitable :

- APA Rôle
- Aphaia
- Chimère
- Krystal
- Ludochronik
- Miroir des Terres Médianes (Le)
- Salamandre (La)

Elles ont été conservées sous forme de fichiers Markdown avec leurs
métadonnées historiques.

## Pages techniques de l'ancien wiki

L'inventaire éditorial a identifié **35 pages techniques ou administratives**
dans l'espace principal du MediaWiki. Elles ne décrivent pas des fanzines et
ne devraient donc pas apparaître dans le catalogue, la recherche, la
navigation séquentielle ou le sitemap.

Trois pages de code obsolète ont été supprimées du site et explicitement
exclues de `scripts/extract_mediawiki.py`, afin qu'une nouvelle migration ne
les recrée pas :

- `Code HTML à récupérer` ;
- `Code d'une Fiche de Numéro de Fanzine` ;
- `Code d'une Fiche de Fanzine`.

Les **32 pages techniques restantes** sont encore publiées en attendant une
décision éditoriale. Inventaire complet par fonction :

### Modèle de fiche restant

- `Code Alternatif d'une Fiche de Numéro de Fanzine`

### Aide à la saisie des champs

- `Auteur`
- `Code ISSN`
- `Date de parution`
- `Début parution`
- `Fin parution`
- `Format`
- `Impression`
- `Jeu`
- `Langue`
- `Nombre total de numéros`
- `Numéro`
- `Page`
- `Pages`
- `Périodicité`
- `Prix (Détails)`
- `Prix (Généralités)`
- `Série`
- `Site web (Détails)`
- `Thème / Jeu(x)`
- `Titre de l'article`
- `Titre (Détails)`
- `Titre (Généralités)`
- `Type d'article`
- `Type de numéro`

### Documentation d'édition et éléments d'interface

- `Couverture (Détails)`
- `Couverture (Généralités)`
- `Logos`
- `Prérequis (Détails)`
- `Prérequis (Généralités)`
- `Prévisualisation des Fiches et comment les remplir`

### Ancienne navigation

- `Page d'Accueil`

La page `Dé à π faces (Le)`, également absente des index alphabétiques de
l'ancien wiki, a été contrôlée séparément : il s'agit bien d'une fiche de
fanzine et non d'une page technique. Elle doit être conservée et ajoutée à
l'index alphabétique lors d'une correction ultérieure.

## Conversion des tableaux MediaWiki

Les 1 543 tableaux écrits avec la syntaxe `{| ... |}` ont été convertis en
tableaux Markdown. Ils contiennent une grande partie des fiches de numéros et
des sommaires. Le contenu, les liens et les images sont conservés, mais les
attributs purement visuels de MediaWiki (`width`, couleurs et `colspan`) ont été
abandonnés.

Les pages les plus concernées sont :

| Page | Tableaux |
| --- | ---: |
| Casus Belli 1e Époque | 148 |
| Jeu de Rôle Magazine | 73 |
| Casus Belli 4e Époque | 68 |
| Jeux & Stratégie | 64 |
| Backstab | 54 |
| Dragon VF | 47 |
| Chroniques d'Altaride | 43 |
| Casus Belli 2e Époque | 41 |
| Graal | 32 |
| Chroniques d'Outre Monde | 31 |
| Palimpseste | 28 |
| Tatou | 28 |
| Dragon Radieux | 27 |
| D20 Magazine | 26 |
| PTGPTB ebook | 26 |
| Ars Mag | 24 |
| Maraudeur (Le) | 24 |
| Grimoire (Le) | 21 |
| Di6dent | 19 |
| Antre du Dragon (L') | 18 |

La page « Rétro-Donj » comportait une fermeture `|}` sans ouverture
correspondante. Cette ligne orpheline est supprimée pendant l’extraction et
signalée dans le rapport.

## Images non classées

107 images ne sont référencées par aucune dernière version des 278 pages
principales. Elles ont été conservées dans `public/images/a-classer/` au lieu
d’être supprimées.

Elles peuvent notamment correspondre à :

- d’anciennes révisions ;
- des pages supprimées ou archivées ;
- des illustrations jamais insérées dans une page ;
- des variantes de couverture ;
- des fichiers portant un nom différent de celui utilisé dans le wikicode.

La liste complète et les empreintes SHA-256 se trouvent dans
`reports/image-manifest.json`.

## Doublons binaires

Les groupes suivants contiennent des fichiers strictement identiques, même
s’ils portent parfois des noms ou des significations différentes :

1. `DeÌ_CaleÌ_01.png` et `DÃ©_CalÃ©_01.png`
2. `DeÌ_CaleÌ_02.png` et `DÃ©_CalÃ©_02.png`
3. `DeÌ_CaleÌ_03.png` et `DÃ©_CalÃ©_03.png`
4. `DeÌ_CaleÌ_04.png` et `DÃ©_CalÃ©_04.png`
5. `JdR_Mag_16.jpg` et `JdR_Mag_16_3.jpg`
6. `ChrysopeeHS01.jpg` et `Revelation04.jpg`

Les doublons n’ont pas été supprimés automatiquement. Le dernier groupe peut
être soit une duplication accidentelle, soit une même illustration utilisée
pour deux publications différentes.

## Noms de fichiers mal encodés

Plusieurs noms liés à « Dé Calé » ont subi un ou plusieurs mauvais décodages
UTF-8. Le script de classement sait les rapprocher des références correctes,
mais les noms sources sont conservés dans le manifeste pour assurer la
traçabilité.

Le fichier `Dé_Calé_05.png`, mentionné dans une ancienne analyse, n’est pas
présent. Sa référence ne figure toutefois plus dans la dernière révision
extraite de la page.

## Images partagées

Dix images génériques sont utilisées par plusieurs publications et se trouvent
dans `public/images/partagees/`. Il s’agit principalement d’indicateurs de
complétude, par exemple :

- `couverture-manquante.png` ;
- `fiche-besoin-d-aide.png` ;
- `fiche-c-est-a-vous.png` ;
- `fiche-complete.png` ;
- `fiche-en-cours.png` ;
- `logo-a-completer.png` ;
- `logo-cherche-couv.png` ;
- `logo-complet.png` ;
- `logo-toutes-couv.png`.

Ces images sont des éléments d’interface hérités du wiki et non des couvertures.
Il faudra décider si elles doivent rester visibles dans le nouveau site ou être
remplacées par des composants Starlight.

## Limites connues de la conversion Markdown

- La mise en page exacte des tableaux MediaWiki n’est pas reproduite : les
  cellules fusionnées deviennent des cellules Markdown ordinaires.
- Certaines balises HTML historiques peuvent encore être présentes.
- Les liens externes pointant vers l’ancien domaine peuvent nécessiter une
  seconde passe pour devenir des liens internes.
- Les descriptions alternatives des images sont actuellement génériques.
- Les 21 redirections sont enregistrées dans le rapport, mais leur configuration
  Vercel n’a pas encore été générée.
- Le contenu n’a pas encore fait l’objet d’une validation éditoriale page par
  page.

## Dépendances du site

Le site construit correctement sous Node.js 24 avec Astro 6.4.8 et Starlight
0.40.0. Cependant, `npm audit` signale six vulnérabilités transitives, dont des
correctifs disponibles seulement avec Astro 7 et Starlight 0.41 au moment de
l’analyse.

La montée vers Astro 7 a été testée, mais son chargeur Vite 8 échoue actuellement
sous Node.js 24/Windows lors du chargement CommonJS de `source-map-js`. Le site
étant entièrement statique et son contenu local, l’exposition aux vulnérabilités
d’exécution est limitée, mais cette dette doit être résolue avant de considérer
la pile technique comme stabilisée.

## Sécurité du dump original

Le dump SQL et son archive contiennent des adresses électroniques, empreintes de
mots de passe, jetons historiques et adresses IP. Ils sont exclus par
`.gitignore` et ne doivent jamais être publiés dans le dépôt GitHub.

Les fichiers Markdown générés ne reprennent pas ces données de comptes. Ils
contiennent néanmoins le nom ou pseudonyme de l’auteur de la dernière révision
dans le frontmatter, à des fins de traçabilité éditoriale.

## Commandes de reproduction

```powershell
python scripts/migrate_images.py
python scripts/extract_mediawiki.py
```

Ces commandes reconstruisent les images organisées, les fichiers Markdown et
les rapports à partir des sources locales ignorées par Git.
