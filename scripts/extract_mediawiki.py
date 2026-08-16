#!/usr/bin/env python3
"""Extrait les dernières versions des articles MediaWiki vers Markdown.

Cette étape produit un corpus intermédiaire vérifiable. Elle ne cherche pas à
imiter MediaWiki : les constructions non converties sont conservées et
signalées dans le rapport afin d'éviter toute perte silencieuse.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import unicodedata
import urllib.parse
from collections import Counter
from pathlib import Path


INSERT_RE = re.compile(br"^INSERT INTO `([^`]+)`")
IMAGE_URL_RE = re.compile(
    r"https?://[^\s\]|<>\"']+/images/([^\s\]|<>\"']+)", re.IGNORECASE
)
INTERNAL_LINK_RE = re.compile(r"\[\[([^\[\]]+?)\]\]")
EXTERNAL_LINK_RE = re.compile(r"\[(https?://[^\s\]]+)(?:\s+([^\]]+))?\]")
HEADING_RE = re.compile(r"^(={1,6})\s*(.*?)\s*\1\s*$")
REDIRECT_RE = re.compile(
    r"^\s*#(?:REDIRECT|REDIRECTION)\s*\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]",
    re.IGNORECASE,
)

# Pages techniques de l'ancien wiki remplacées par la page consolidée
# `normes-edition.md`. Elles restent dans le dump source ignoré par Git, mais ne
# doivent pas être recréées lors d'une nouvelle extraction.
EXCLUDED_PAGE_TITLES = {
    "Auteur",
    "Code Alternatif d'une Fiche de Numéro de Fanzine",
    "Code HTML à récupérer",
    "Code ISSN",
    "Code d'une Fiche de Numéro de Fanzine",
    "Code d'une Fiche de Fanzine",
    "Couverture (Détails)",
    "Couverture (Généralités)",
    "Date de parution",
    "Début parution",
    "Fin parution",
    "Format",
    "Impression",
    "Jeu",
    "Langue",
    "Logos",
    "Nombre total de numéros",
    "Numéro",
    "Page",
    "Page d'Accueil",
    "Pages",
    "Prérequis (Détails)",
    "Prérequis (Généralités)",
    "Prix (Détails)",
    "Prix (Généralités)",
    "Prévisualisation des Fiches et comment les remplir",
    "Périodicité",
    "Série",
    "Site web (Détails)",
    "Thème / Jeu(x)",
    "Titre (Détails)",
    "Titre (Généralités)",
    "Titre de l'article",
    "Type d'article",
    "Type de numéro",
}


def sql_fields(line: bytes) -> list[bytes]:
    value = line.strip().rstrip(b",;")[1:-1]
    fields: list[bytes] = []
    start = 0
    quoted = False
    escaped = False
    for index, char in enumerate(value):
        if quoted:
            if escaped:
                escaped = False
            elif char == 92:
                escaped = True
            elif char == 39:
                quoted = False
        elif char == 39:
            quoted = True
        elif char == 44:
            fields.append(value[start:index].strip())
            start = index + 1
    fields.append(value[start:].strip())
    return fields


def decode_sql(value: bytes) -> str:
    if value.startswith(b"0x"):
        try:
            return bytes.fromhex(value[2:].decode("ascii")).decode("utf-8", "replace")
        except (ValueError, UnicodeDecodeError):
            return ""
    if value == b"''":
        return ""
    return value.decode("utf-8", "replace").strip("'")


def slug(value: str) -> str:
    value = value.replace("_", " ")
    value = unicodedata.normalize("NFKD", value).casefold()
    value = "".join(char for char in value if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-") or "sans-titre"


def name_key(value: str) -> str:
    value = urllib.parse.unquote(value)
    value = unicodedata.normalize("NFKD", value).casefold()
    return "".join(char for char in value if char.isalnum())


def read_dump(sql_path: Path) -> tuple[dict[int, dict], dict[int, dict]]:
    pages: dict[int, dict] = {}
    revisions: dict[int, dict] = {}
    table = ""
    with sql_path.open("rb") as stream:
        for line in stream:
            match = INSERT_RE.match(line)
            if match:
                table = match.group(1).decode("ascii")
                continue
            if not table or not line.startswith(b"("):
                continue
            fields = sql_fields(line)
            if table == "_fanzpage" and int(fields[1]) == 0:
                pages[int(fields[0])] = {
                    "page_id": int(fields[0]),
                    "title": decode_sql(fields[2]).replace("_", " "),
                    "legacy_title": decode_sql(fields[2]),
                    "is_redirect": bool(int(fields[5])),
                    "latest_revision": int(fields[10]),
                    "length": int(fields[11]),
                }
            elif table == "_fanzrevision":
                revisions[int(fields[0])] = {
                    "text_id": int(fields[2]),
                    "timestamp": decode_sql(fields[6]),
                    "author": decode_sql(fields[5]),
                }
    return pages, revisions


def read_texts(sql_path: Path, wanted: set[int]) -> dict[int, str]:
    texts: dict[int, str] = {}
    table = ""
    with sql_path.open("rb") as stream:
        for line in stream:
            match = INSERT_RE.match(line)
            if match:
                table = match.group(1).decode("ascii")
                continue
            if table != "_fanztext" or not line.startswith(b"("):
                continue
            fields = sql_fields(line)
            text_id = int(fields[0])
            if text_id in wanted:
                texts[text_id] = decode_sql(fields[1])
    return texts


def load_image_lookup(manifest_path: Path) -> dict[tuple[str, str], str]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    lookup: dict[tuple[str, str], str] = {}
    for reference in manifest["references"]:
        destinations = reference.get("destinations", [])
        if destinations:
            destination = destinations[0].replace("\\", "/")
            public_marker = "public/"
            public_path = destination.split(public_marker, 1)[-1]
            lookup[(reference["article"].replace("_", " "), name_key(reference["original_url_name"]))] = "/" + public_path
    return lookup


def convert_internal_link(raw: str, known_titles: dict[str, str]) -> str:
    parts = raw.split("|", 1)
    target = parts[0].strip()
    label = parts[1].strip() if len(parts) == 2 else target.replace("_", " ")
    normalized_target = target.partition("#")[0].replace("_", " ")
    if normalized_target in EXCLUDED_PAGE_TITLES:
        return label
    if target.lower().startswith(("category:", "catégorie:")):
        return ""
    if target.lower().startswith(("file:", "fichier:", "image:")):
        return label
    page_target, separator, anchor = target.partition("#")
    target_slug = known_titles.get(page_target.replace("_", " ").casefold(), slug(page_target))
    suffix = f"#{slug(anchor)}" if separator and anchor else ""
    return f"[{label}](../{target_slug}/{suffix})"


def clean_table_cell(value: str) -> str:
    value = value.strip()
    # MediaWiki place les attributs avant un séparateur `|` simple.
    if "|" in value:
        prefix, content = value.split("|", 1)
        if "=" in prefix and not prefix.lstrip().startswith(("[", "!")):
            value = content.strip()
    value = re.sub(r"\s*\n\s*", "<br>", value.strip())
    return value.replace("|", r"\|")


def parse_wikitable(block: list[str]) -> str:
    rows: list[list[tuple[str, bool]]] = []
    current: list[tuple[str, bool]] = []
    caption = ""

    def finish_row() -> None:
        nonlocal current
        if current:
            rows.append(current)
            current = []

    for line in block[1:-1]:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("|+"):
            caption = clean_table_cell(stripped[2:])
        elif stripped.startswith("|-"):
            finish_row()
        elif stripped.startswith("!") and not stripped.startswith("!["):
            finish_row() if current and any(not header for _, header in current) else None
            current.extend((clean_table_cell(cell), True) for cell in stripped[1:].split("!!"))
        elif stripped.startswith("|"):
            current.extend((clean_table_cell(cell), False) for cell in stripped[1:].split("||"))
        elif current:
            value, header = current[-1]
            current[-1] = (f"{value}<br>{clean_table_cell(stripped)}", header)
        elif caption:
            caption += f"<br>{clean_table_cell(stripped)}"
    finish_row()

    if not rows:
        return f"**{caption}**" if caption else ""
    width = max(len(row) for row in rows)
    first_is_header = any(header for _, header in rows[0])
    header_values = [value for value, _ in rows[0]] if first_is_header else [""] * width
    data_rows = rows[1:] if first_is_header else rows

    def render(values: list[str]) -> str:
        values += [""] * (width - len(values))
        return "| " + " | ".join(values) + " |"

    rendered = []
    if caption:
        rendered.extend([f"**{caption}**", ""])
    rendered.append(render(header_values))
    rendered.append(render(["---"] * width))
    for row in data_rows:
        rendered.append(render([value for value, _ in row]))
    return "\n".join(rendered)


def convert_wikitables(text: str) -> tuple[str, int, int, int]:
    lines = text.splitlines()
    output: list[str] = []
    index = 0
    converted = 0
    unterminated = 0
    orphan_closers = 0
    while index < len(lines):
        if lines[index].lstrip().startswith("|}"):
            orphan_closers += 1
            index += 1
            continue
        if not lines[index].lstrip().startswith("{|"):
            output.append(lines[index])
            index += 1
            continue
        end = index + 1
        while end < len(lines) and not lines[end].lstrip().startswith("|}"):
            end += 1
        if end >= len(lines):
            output.extend(lines[index:])
            unterminated += 1
            break
        output.append(parse_wikitable(lines[index : end + 1]))
        converted += 1
        index = end + 1
    return "\n".join(output), converted, unterminated, orphan_closers


def convert_wikitext(
    text: str,
    article: str,
    known_titles: dict[str, str],
    image_lookup: dict[tuple[str, str], str],
) -> tuple[str, dict]:
    stats = Counter()
    text = html.unescape(text).replace("\r\n", "\n").replace("\r", "\n")

    def image_replacement(match: re.Match[str]) -> str:
        raw_name = match.group(1).rstrip(".,;:)")
        destination = image_lookup.get((article, name_key(raw_name)))
        if destination:
            stats["images_rewritten"] += 1
            alt = f"Illustration de {article}"
            return f"![{alt}]({destination})"
        stats["images_missing"] += 1
        return match.group(0)

    text = IMAGE_URL_RE.sub(image_replacement, text)
    # Ce modèle ne contenait que les liens de navigation propres au wiki.
    text, navigation_count = re.subn(r"\{\{\s*Navigation\s*\}\}", "", text, flags=re.IGNORECASE)
    stats["navigation_templates_removed"] += navigation_count
    lines: list[str] = []
    for line in text.splitlines():
        heading = HEADING_RE.match(line)
        if heading:
            level = min(len(heading.group(1)) + 1, 6)
            line = f"{'#' * level} {heading.group(2).strip()}"
            stats["headings"] += 1
        elif line.startswith("* "):
            line = "- " + line[2:]
        elif line.startswith("** "):
            line = "  - " + line[3:]
        elif line.startswith("# "):
            line = "1. " + line[2:]
        lines.append(line)
    text = "\n".join(lines)

    text, count = INTERNAL_LINK_RE.subn(
        lambda match: convert_internal_link(match.group(1), known_titles), text
    )
    stats["internal_links"] += count
    text, count = EXTERNAL_LINK_RE.subn(
        lambda match: f"[{match.group(2) or match.group(1)}]({match.group(1)})", text
    )
    stats["external_links"] += count
    text = re.sub(r"'''(.*?)'''", r"**\1**", text, flags=re.DOTALL)
    text = re.sub(r"''(.*?)''", r"*\1*", text, flags=re.DOTALL)
    text = re.sub(r"<br\s*/?>", "  \n", text, flags=re.IGNORECASE)
    text = re.sub(r"__NOTOC__|__NOEDITSECTION__", "", text, flags=re.IGNORECASE)
    text, converted_tables, unterminated_tables, orphan_table_closers = convert_wikitables(text)
    stats["wikitables_converted"] = converted_tables
    stats["unterminated_wikitables"] = unterminated_tables
    stats["orphan_table_closers_removed"] = orphan_table_closers
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    stats["unconverted_templates"] = len(re.findall(r"\{\{", text))
    stats["unconverted_wikitables"] = len(re.findall(r"^\{\|", text, re.MULTILINE))
    stats["replacement_characters"] = text.count("�")
    return text + "\n", dict(stats)


def frontmatter(page: dict, revision: dict) -> str:
    description = f"Archive de la page MediaWiki « {page['title']} »."
    values = {
        "title": page["title"],
        "description": description,
        "legacy_page_id": page["page_id"],
        "legacy_title": page["legacy_title"],
        "legacy_revision_id": page["latest_revision"],
        "legacy_revision_timestamp": revision["timestamp"],
        "legacy_author": revision["author"],
        "source_format": "mediawiki",
    }
    lines = ["---"]
    for key, value in values.items():
        lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
    lines.extend(["---", ""])
    return "\n".join(lines)


def extract(sql_path: Path, manifest_path: Path, output_dir: Path, report_path: Path) -> dict:
    pages, revisions = read_dump(sql_path)
    wanted = {
        revisions[page["latest_revision"]]["text_id"]
        for page in pages.values()
        if page["latest_revision"] in revisions
    }
    texts = read_texts(sql_path, wanted)
    image_lookup = load_image_lookup(manifest_path)
    known_titles = {page["title"].casefold(): slug(page["title"]) for page in pages.values()}
    output_dir.mkdir(parents=True, exist_ok=True)

    redirects: list[dict] = []
    page_reports: list[dict] = []
    totals = Counter()
    written = 0
    excluded_pages: list[dict] = []
    for page in sorted(pages.values(), key=lambda item: item["title"].casefold()):
        if page["title"] in EXCLUDED_PAGE_TITLES:
            excluded_pages.append(
                {
                    "page_id": page["page_id"],
                    "title": page["title"],
                    "slug": slug(page["title"]),
                    "reason": "technical_page_excluded_from_public_site",
                }
            )
            continue

        revision = revisions.get(page["latest_revision"])
        raw_text = texts.get(revision["text_id"], "") if revision else ""
        redirect = REDIRECT_RE.match(raw_text)
        if page["is_redirect"] or redirect:
            target = redirect.group(1).replace("_", " ") if redirect else ""
            redirects.append(
                {
                    "page_id": page["page_id"],
                    "from_title": page["title"],
                    "from_slug": slug(page["title"]),
                    "to_title": target,
                    "to_slug": slug(target) if target else "",
                }
            )
            continue

        converted, stats = convert_wikitext(raw_text, page["title"], known_titles, image_lookup)
        destination = output_dir / f"{slug(page['title'])}.md"
        destination.write_text(frontmatter(page, revision or {}) + converted, encoding="utf-8")
        written += 1
        totals.update(stats)
        page_reports.append(
            {
                "page_id": page["page_id"],
                "title": page["title"],
                "destination": destination.as_posix(),
                "source_length": len(raw_text),
                "output_length": len(converted),
                **stats,
            }
        )

    report = {
        "summary": {
            "main_namespace_pages": len(pages),
            "markdown_pages": written,
            "redirects": len(redirects),
            "excluded_technical_pages": len(excluded_pages),
            "empty_markdown_pages": sum(page["output_length"] <= 1 for page in page_reports),
            **totals,
        },
        "redirects": redirects,
        "excluded_pages": excluded_pages,
        "pages": page_reports,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report["summary"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sql", type=Path, default=Path("sources/fanzines_jdr_wiki.sql"))
    parser.add_argument("--images", type=Path, default=Path("reports/image-manifest.json"))
    parser.add_argument("--output", type=Path, default=Path("src/content/docs/fanzines"))
    parser.add_argument("--report", type=Path, default=Path("reports/content-migration.json"))
    args = parser.parse_args()
    summary = extract(args.sql, args.images, args.output, args.report)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
