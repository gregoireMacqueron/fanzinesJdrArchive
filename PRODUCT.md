# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
Primary: researchers and collectors (nostalgic role-players, collectors,
historians of French-language tabletop RPG) looking up a specific title, issue,
table of contents or author. Secondary: contributors who correct or complete
entries through GitHub pull requests or issues.

## Product Purpose
Fanzines JDR is the static successor of the former Fanzines JdR Wiki: a
reference archive of French-language role-playing magazines, fanzines and
e-zines. For each title it documents issues and dates, teams and publishers,
formats, prices and frequency, covers and tables of contents. Success means a
visitor finds a precise publication fact quickly and can trust and cite it.

## Positioning
- Article-level tables of contents (title, author, page, article type), deeper
  than general RPG databases such as the GROG.
- Coverage of amateur, associative and confidential fanzines that are poorly
  documented elsewhere.
- Durability and openness: a static, publicly versioned site that depends on
  neither a wiki engine nor a single host.
- Covers kept with the site rather than hotlinked.

## Operating Context
- Visitors browse alphabetical index pages (`0-9`, `a-d`, … `x-z`), the sidebar,
  or the built-in search, then read long entry pages made of wide Markdown
  tables inherited from MediaWiki.
- Contributors edit Markdown in `src/content/docs/fanzines/` and follow
  `normes-edition.md`; additions are logged in `nouveautes.md`.

## Capabilities and Constraints
- Stack is fixed: Astro + Starlight, content in Markdown editable without
  development skills.
- French only; no translation planned.
- Zero budget: free hosting (Vercel), no paid service.
- 223 entry pages migrated automatically; many remain incomplete or keep
  traces of MediaWiki syntax.
- Undecided: mobile readability of wide tables was not confirmed as a
  requirement.

## Brand Commitments
- Name: Fanzines JDR. Tagline: « La mémoire des revues, fanzines et e-zines
  francophones de jeu de rôle. »
- Voice: factual, welcoming to contributors, credits the community that built
  the original wiki.

## Evidence on Hand
- 223 entries in `src/content/docs/fanzines/`, covers in
  `public/images/fanzines/<slug>/`.
- Placeholder images in `public/images/partagees/`; unused wiki images in
  `public/images/a-classer/`.
- Migration reports in `reports/`, `ANOMALIES.md`.
- No traffic data, testimonials or user research; do not fabricate them.

## Product Principles
1. Accuracy first: never invent a value to fill a field; `?` beats a guess.
2. Findability: any title, issue or article reachable in a few steps or one
   search.
3. Durability: plain files, open repository, no lock-in.
4. Low barrier to contribution: editing a page must stay simple Markdown.
