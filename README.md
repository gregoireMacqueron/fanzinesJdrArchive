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
scripts/                   Outils de migration du contenu historique
reports/                   Rapports produits pendant la migration
astro.config.mjs           Configuration Astro et Starlight
```

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
