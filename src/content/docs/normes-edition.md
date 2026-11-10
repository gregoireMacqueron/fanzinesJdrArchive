---
title: Normes d’édition
description: Règles pour rédiger et compléter les fiches de fanzines et de numéros.
sidebar:
  order: 2
---

Cette page rassemble les conventions éditoriales de Fanzines JDR. Elle remplace
les anciennes pages d’aide du MediaWiki et sert de référence pour toute
correction ou nouvelle fiche.

## Principes généraux

- Une publication possède une seule page Markdown dans
  `src/content/docs/fanzines/`.
- La fiche générale ouvre la page sous le titre `## Généralités`.
- Chaque numéro dispose ensuite d’une section `## Numéro n`,
  `## Numéro hors-série n` ou `## Numéro spécial n`.
- Conservez les informations vérifiables et indiquez leur source dans le texte
  ou dans une section « Sources ».
- Utilisez `?` pour une information inconnue et `n/a` seulement lorsqu’un champ
  ne s’applique réellement pas.
- Respectez l’orthographe des noms propres et le titre imprimé sur la publication.
  N’inventez pas une valeur pour compléter visuellement une fiche.

## Fiche générale d’une publication

La fiche générale documente le titre dans son ensemble, indépendamment d’un
numéro particulier.

| Champ | Contenu attendu |
| --- | --- |
| **Titre** | Titre complet du fanzine. La mention historique « généralités » n’a pas besoin d’être répétée dans la valeur. |
| **Couverture** | Couverture représentative, de préférence le numéro 0 ou 1. |
| **Code ISSN** | ISSN de la publication, s’il existe. |
| **Langue** | Langue principale ; le corpus est consacré en priorité aux publications francophones. |
| **Thème / Jeu** | `généraliste`, nom du jeu, système, univers ou éditeur principalement traité. Un lien vers le GROG peut être ajouté. |
| **Description** | Présentation factuelle et concise de la publication. |
| **Remarque** | Particularités qui n’entrent pas dans les autres champs. |
| **Format** | Papier, numérique ou les deux ; dimensions ou format (`A4`, `A5`), portrait ou paysage si connus. |
| **Impression** | Offset, sérigraphie, photocopie, impression à la demande, autre ou numérique uniquement. |
| **Adresse physique** | Adresse ou siège indiqués dans la publication, en tenant compte de leur caractère historique. |
| **Fondateur / Responsable** | Personnes ou structure responsables de la publication. |
| **Éditeur** | Nom de l’éditeur ou de l’association éditrice. |
| **Rédac’chef** | Nom de la ou des personnes assurant la rédaction en chef. |
| **Site web** | Site officiel ou page consacrée à la publication. |
| **Prix** | Prix habituel au numéro, avec la devise et, si utile, la période concernée. |
| **Nombre total de numéros** | Total paru à ce jour, hors-série compris en les signalant séparément si possible. |
| **Périodicité** | Mensuelle, bimestrielle, trimestrielle, semestrielle, annuelle, biennale, variable, aléatoire ou autre. Préférer `semestrielle` à `biannuelle`, qui est ambigu. |
| **Début parution** | Mois et année, ou trimestre et année, du premier numéro. |
| **Fin parution** | Même format pour le dernier numéro, ou `en cours`. |

Exemple minimal :

```md
## Généralités

| Titre : Exemple | **Couverture :** ![Couverture du numéro 1](/images/fanzines/exemple/exemple-01.jpg) | |
| --- | --- | --- |
| **Code ISSN :** ? | **Langue :** français | **Thème / Jeu :** généraliste |
| **Description :** Fanzine associatif consacré au jeu de rôle. | | |
| **Remarque :** ? | | |
| **Format :** papier, A5, portrait | **Impression :** photocopie | **Adresse physique :** ? |
| **Fondateur / Responsable :** ? | **Éditeur :** ? | **Rédac’chef :** ? |
| **Site web :** n/a | **Prix :** ? | **Nombre total de n° :** 1 |
| **Périodicité :** n/a | **Début parution :** mars 1992 | **Fin parution :** mars 1992 |
```

## Fiche d’un numéro

| Champ | Contenu attendu |
| --- | --- |
| **Titre** | Titre du fanzine ; le numéro est déjà donné par le titre de section. |
| **Couverture** | Image propre à ce numéro. |
| **Numéro** | Chiffres arabes. Identifiez explicitement les hors-série et numéros spéciaux. |
| **Type de numéro** | Normal, thématique, hors-série ou spécial. |
| **Série** | Période ou série éditoriale lorsqu’un titre a connu plusieurs incarnations, par exemple les différentes époques de *Casus Belli*. |
| **Date de parution** | Mois et année ou trimestre et année. Distinguez si nécessaire la date annoncée de la date de sortie constatée. |
| **Pages** | Nombre total de pages du numéro. |
| **Responsable, Rédac’chef, Éditeur** | Informations propres au numéro si elles diffèrent de la fiche générale. |
| **Site web** | Lien officiel ou lien de téléchargement légal du numéro. |
| **Adresse physique** | Adresse publiée dans ce numéro. |
| **Prix** | Prix de ce numéro, avec sa devise. |

Exemple d’en-tête :

```md
## Numéro 1

| Titre : Exemple | **Couverture :** ![Couverture du numéro 1 d’Exemple](/images/fanzines/exemple/exemple-01.jpg) | | | |
| --- | --- | --- | --- | --- |
| **Numéro :** 1 | **Type de numéro :** normal | **Série :** n/a | **Date de parution :** mars 1992 | **Pages :** ? |
| **Responsable :** ? | **Éditeur :** ? | **Rédac’chef :** ? | | |
| **Site web :** n/a | **Adresse physique :** ? | **Prix :** ? | | |
```

### Sommaire

Utilisez de préférence le tableau détaillé lorsque les informations sont
disponibles :

```md
| Titre de l’article | Jeu | Auteur | Page | Type d’article |
| --- | --- | --- | --- | --- |
| Le château oublié | Donjons & Dragons | Camille Martin | Page 12 | Scénario |
```

- N’ajoutez pas de guillemets autour du titre d’un article.
- Donnez les auteurs tels qu’ils sont crédités.
- Indiquez `Page` suivi du nombre en chiffres arabes.
- Renseignez le jeu pour un scénario, une aide de jeu ou une critique. Il n’est
  pas nécessaire de le répéter entre parenthèses dans le titre si la colonne
  `Jeu` est présente.
- Si seules trois informations sont connues, un tableau
  `Titre de l’article | Page | Type d’article` reste acceptable.

Les principaux types d’articles sont : scénario, campagne, synopsis, aide de
jeu, règles, bestiaire, personnage, univers, critique, actualité, entretien,
compte rendu, nouvelle, bande dessinée et inspiration. Une précision peut être
ajoutée après une barre oblique, par exemple `Aide de jeu / Bestiaire`.

## Couvertures et autres images

- Placez les images dans `public/images/fanzines/<slug-du-fanzine>/` et utilisez
  un nom explicite et stable, par exemple `exemple-03.jpg`.
- Référencez-les avec un chemin absolu depuis la racine du site :
  `/images/fanzines/exemple/exemple-03.jpg`.
- Rédigez un texte alternatif précis : `Couverture du numéro 3 d’Exemple`.
- Préférez l’image source la plus lisible disponible. L’ancienne recommandation
  de 200 pixels de large n’est plus une limite.
- N’utilisez pas un hébergeur d’images externe : le fichier doit être conservé
  avec le site pour rester disponible.
- Signalez la provenance de l’image lorsqu’elle est connue. Une demande de
  retrait d’un ayant droit doit être traitée rapidement.
- Si la couverture manque, laissez le champ explicite (`?` ou « couverture
  manquante ») ; les anciens logos colorés du wiki ne sont plus à ajouter.

## Liens et sources

- Privilégiez les sites officiels, les catalogues de bibliothèques, les scans du
  document et les archives web.
- Pour un ISSN, vérifiez si possible le [catalogue général de la BnF](https://catalogue.bnf.fr/).
- Pour un jeu, un système ou un éditeur, un lien vers le
  [Guide du Rôliste Galactique](https://www.legrog.org/) est pertinent.
- Ne présentez comme téléchargement que les fichiers diffusés légalement.
- Conservez un lien ancien utile même s’il est hors ligne, mais accompagnez-le
  si possible d’une archive pérenne.

## Proposer une modification

Modifiez le fichier Markdown concerné dans le
[dépôt GitHub](https://github.com/guillaumejay/fanzinesjdr), puis ouvrez une
pull request. Vous pouvez aussi ouvrir une issue avec les informations, leurs
sources et les images : aucune connaissance de Markdown n’est nécessaire pour
signaler un complément.

