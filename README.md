# Fanzines JDR

Archives des revues, fanzines et e-zines francophones consacrés au jeu de rôle.

Le projet reprend le fonds de l'ancien **Fanzines JdR Wiki** sous la forme d'un
site statique, durable et versionné publiquement. Il rassemble notamment les
titres, périodes de parution, équipes, formats, couvertures et sommaires des
publications recensées.

## Site en ligne

Le site est déployé sur Vercel :

**[fanzinesjdr.vercel.app](https://fanzinesjdr.vercel.app)**

## Technologies

- [Astro](https://astro.build/)
- [Starlight](https://starlight.astro.build/)
- Markdown pour les fiches et la documentation
- Vercel pour l'hébergement

## Installation locale

Le projet nécessite **Node.js 24**.

```bash
git clone https://github.com/guillaumejay/fanzinesjdr.git
cd fanzinesjdr
npm install
npm run dev
```

Le serveur de développement indique ensuite l'adresse locale à ouvrir dans le
navigateur, généralement `http://localhost:4321`.

## Commandes disponibles

| Commande | Description |
| --- | --- |
| `npm run dev` | Lance le serveur de développement Astro |
| `npm run build` | Génère le site statique dans `dist/` |
| `npm run preview` | Prévisualise localement la version générée |

## Organisation du projet

```text
src/content/docs/          Pages et documentation du site
src/content/docs/fanzines/ Fiches des publications
public/images/fanzines/    Couvertures et autres images par publication
public/images/partagees/   Images génériques communes à plusieurs fiches
public/images/a-classer/   Images de l'ancien wiki non rattachées à une fiche
scripts/                   Scripts Python de migration du wiki historique
reports/                   Rapports produits pendant la migration
astro.config.mjs           Configuration Astro et Starlight
```

Les images de `public/images/partagees/` servent d'indicateurs (couverture
manquante, fiche à compléter, etc.). Celles de `public/images/a-classer/`
n'étaient utilisées par aucune page lors de la migration : elles sont conservées
en attendant d'être rattachées à une fiche ou écartées. Le détail figure dans
[ANOMALIES.md](ANOMALIES.md).

## Scripts de migration

Les scripts de `scripts/` ont servi à convertir l'ancien MediaWiki en fiches
Markdown. Ils ne sont pas nécessaires pour faire évoluer le site : les fiches se
modifient désormais directement. Ils sont conservés pour documenter et, au
besoin, rejouer la migration.

Ils nécessitent Python 3 et n'utilisent que la bibliothèque standard. Ils lisent
le dump SQL et les images d'origine dans `sources/`, qui ne sont pas versionnés
car ils contiennent des données personnelles. Les commandes se lancent depuis la
racine du dépôt, dans cet ordre :

```bash
python scripts/migrate_images.py
python scripts/extract_mediawiki.py
```

1. `migrate_images.py` copie et classe les images de `sources/images/` dans
   `public/images/` et produit `reports/image-manifest.json`.
2. `extract_mediawiki.py` convertit les dernières versions des pages en
   Markdown dans `src/content/docs/fanzines/` et produit
   `reports/content-migration.json`.

Les chemins par défaut peuvent être changés avec les options `--sql`,
`--source`, `--images`, `--output`, `--manifest` et `--report` ; `--help`
affiche celles de chaque script.

> **Attention :** relancer `extract_mediawiki.py` régénère les fiches à partir
> du dump et écrase les corrections faites depuis la migration.

## Contribuer

Les corrections et compléments sont bienvenus : informations bibliographiques,
sommaires, nouveaux titres ou couvertures manquantes.

Vous pouvez modifier directement la fiche Markdown concernée dans
`src/content/docs/fanzines/`, puis proposer une pull request. Vous pouvez aussi
[ouvrir une issue](https://github.com/guillaumejay/fanzinesjdr/issues) avec une
description de la correction et, si possible, sa source.

Avant de proposer une modification, consultez les
[normes d'édition](https://fanzinesjdr.vercel.app/normes-edition/).

## Construire le site

```bash
npm run build
```

La version statique est générée dans le dossier `dist/`. Sur Vercel, la commande
de construction est détectée à partir de la configuration Astro du projet.

## Remerciements

Merci à David, créateur du **Fanzines JdR Wiki**, pour m'avoir autorisé à
reprendre le contenu du wiki et pour m'avoir confié la sauvegarde de la base
MediaWiki d'origine. Sans lui, cette archive n'existerait pas.
