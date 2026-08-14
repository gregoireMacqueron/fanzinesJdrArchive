#!/usr/bin/env python3
"""Classe les images MediaWiki par article à partir du dump SQL.

Le script ne modifie jamais ``sources/images``. Il copie les fichiers dans
``public/images`` et produit un manifeste JSON permettant de rejouer et
contrôler la migration.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import unicodedata
import urllib.parse
from collections import Counter, defaultdict
from pathlib import Path


INSERT_RE = re.compile(br"^INSERT INTO `([^`]+)`")
IMAGE_URL_RE = re.compile(
    r"https?://[^\s\]|<>\"']+/images/([^\s\]|<>\"']+)", re.IGNORECASE
)


def sql_fields(line: bytes) -> list[bytes]:
    """Découpe un tuple phpMyAdmin sans charger le dump en mémoire."""
    value = line.strip().rstrip(b",;")[1:-1]
    fields: list[bytes] = []
    start = 0
    quoted = False
    escaped = False
    for index, char in enumerate(value):
        if quoted:
            if escaped:
                escaped = False
            elif char == 92:  # backslash
                escaped = True
            elif char == 39:  # apostrophe
                quoted = False
        elif char == 39:
            quoted = True
        elif char == 44:  # virgule
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
    value = unicodedata.normalize("NFKD", value).casefold()
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "sans-titre"


def name_key(value: str) -> str:
    value = urllib.parse.unquote(value)
    value = unicodedata.normalize("NFKD", value).casefold()
    return "".join(char for char in value if char.isalnum())


def repaired_names(value: str) -> set[str]:
    """Retourne aussi des variantes réparées de noms UTF-8 mal décodés."""
    variants = {value}
    frontier = {value}
    for _ in range(2):
        next_frontier: set[str] = set()
        for candidate in frontier:
            for encoding in ("latin1", "cp1252"):
                try:
                    repaired = candidate.encode(encoding).decode("utf-8")
                except (UnicodeEncodeError, UnicodeDecodeError):
                    continue
                if repaired not in variants:
                    variants.add(repaired)
                    next_frontier.add(repaired)
        frontier = next_frontier
    return variants


def read_pages_and_revisions(sql_path: Path) -> tuple[dict[int, tuple[str, int]], dict[int, int]]:
    pages: dict[int, tuple[str, int]] = {}
    revision_to_text: dict[int, int] = {}
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
                pages[int(fields[0])] = (decode_sql(fields[2]), int(fields[10]))
            elif table == "_fanzrevision":
                revision_to_text[int(fields[0])] = int(fields[2])
    return pages, revision_to_text


def read_selected_texts(sql_path: Path, wanted: set[int]) -> dict[int, str]:
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


def unique_destination(directory: Path, filename: str, source: Path, claimed: dict[Path, Path]) -> Path:
    stem = slug(Path(filename).stem)
    extension = source.suffix.lower() or ".bin"
    destination = directory / f"{stem}{extension}"
    if destination not in claimed or claimed[destination] == source:
        return destination
    digest = hashlib.sha256(source.read_bytes()).hexdigest()[:8]
    return directory / f"{stem}-{digest}{extension}"


def migrate(sql_path: Path, source_dir: Path, output_dir: Path, manifest_path: Path) -> dict:
    pages, revision_to_text = read_pages_and_revisions(sql_path)
    wanted = {
        revision_to_text[revision]
        for _, revision in pages.values()
        if revision in revision_to_text
    }
    texts = read_selected_texts(sql_path, wanted)

    references: list[dict] = []
    owners_by_key: dict[str, set[str]] = defaultdict(set)
    for title, revision in pages.values():
        text_id = revision_to_text.get(revision)
        for raw_name in IMAGE_URL_RE.findall(texts.get(text_id, "")):
            raw_name = raw_name.rstrip(".,;:)")
            basename = Path(urllib.parse.unquote(raw_name)).name
            key = name_key(basename)
            owners_by_key[key].add(title)
            references.append({"article": title, "original_url_name": raw_name, "key": key})

    files = sorted(path for path in source_dir.iterdir() if path.is_file())
    files_by_key: dict[str, list[Path]] = defaultdict(list)
    for path in files:
        for variant in repaired_names(path.name):
            files_by_key[name_key(variant)].append(path)

    claimed: dict[Path, Path] = {}
    file_entries: list[dict] = []
    source_to_destination: dict[Path, Path] = {}
    for source in files:
        possible_keys = {name_key(name) for name in repaired_names(source.name)}
        owners = sorted({owner for key in possible_keys for owner in owners_by_key.get(key, set())})
        if len(owners) == 1:
            category = "fanzines"
            owner_slug = slug(owners[0])
            directory = output_dir / category / owner_slug
        elif len(owners) > 1:
            category = "partagees"
            owner_slug = None
            directory = output_dir / category
        else:
            category = "a-classer"
            owner_slug = None
            directory = output_dir / category

        destination = unique_destination(directory, source.name, source, claimed)
        claimed[destination] = source
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        source_to_destination[source] = destination
        file_entries.append(
            {
                "source": source.as_posix(),
                "destination": destination.as_posix(),
                "category": category,
                "articles": owners,
                "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "bytes": source.stat().st_size,
            }
        )

    missing: list[dict] = []
    for reference in references:
        candidates = files_by_key.get(reference["key"], [])
        if candidates:
            reference["destinations"] = sorted(
                source_to_destination[path].as_posix() for path in set(candidates)
            )
        else:
            reference["destinations"] = []
            missing.append(reference)
        del reference["key"]

    duplicate_groups = []
    by_hash: dict[str, list[str]] = defaultdict(list)
    for entry in file_entries:
        by_hash[entry["sha256"]].append(entry["source"])
    for digest, names in sorted(by_hash.items()):
        if len(names) > 1:
            duplicate_groups.append({"sha256": digest, "sources": names})

    summary = {
        "articles": len(pages),
        "article_texts_read": len(texts),
        "image_references": len(references),
        "unique_reference_names": len({name_key(r["original_url_name"]) for r in references}),
        "source_files": len(files),
        "classified_files": sum(entry["category"] == "fanzines" for entry in file_entries),
        "shared_files": sum(entry["category"] == "partagees" for entry in file_entries),
        "unclassified_files": sum(entry["category"] == "a-classer" for entry in file_entries),
        "missing_references": len(missing),
        "duplicate_groups": len(duplicate_groups),
    }
    manifest = {
        "summary": summary,
        "files": file_entries,
        "references": references,
        "missing_references": missing,
        "duplicate_groups": duplicate_groups,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sql", type=Path, default=Path("sources/fanzines_jdr_wiki.sql"))
    parser.add_argument("--source", type=Path, default=Path("sources/images"))
    parser.add_argument("--output", type=Path, default=Path("public/images"))
    parser.add_argument("--manifest", type=Path, default=Path("reports/image-manifest.json"))
    args = parser.parse_args()
    summary = migrate(args.sql, args.source, args.output, args.manifest)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
