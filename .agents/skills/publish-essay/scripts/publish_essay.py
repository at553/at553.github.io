#!/usr/bin/env python3
"""Publish the writing inbox as a self-contained Jekyll essay bundle."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path


PLACEHOLDER_TITLE = "Paste essay title here"
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+['\"][^'\"]*['\"])?\)")


def fail(message: str) -> None:
    raise ValueError(message)


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def split_front_matter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    try:
        closing = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        fail("The YAML front matter is missing its closing --- line.")

    metadata: dict[str, str] = {}
    for line in lines[1:closing]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            fail(f"Unsupported front matter line: {line}")
        key, value = line.split(":", 1)
        metadata[key.strip()] = unquote(value)
    return metadata, "\n".join(lines[closing + 1 :]).lstrip("\n")


def title_from_body(body: str) -> str | None:
    for line in body.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    return None


def strip_title_heading(body: str, title: str) -> str:
    lines = body.splitlines()
    normalized_title = re.sub(r"\s+", " ", title).strip().casefold()
    for index, line in enumerate(lines):
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if not match:
            continue
        normalized_heading = re.sub(r"\s+", " ", match.group(1)).strip().casefold()
        if normalized_heading == normalized_title:
            del lines[index]
            while index < len(lines) and not lines[index].strip():
                del lines[index]
        break
    return "\n".join(lines).strip() + "\n"


def plain_text(markdown: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", markdown)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[`*_>#]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def description_from_body(body: str) -> str | None:
    paragraphs = re.split(r"\n\s*\n", body)
    for paragraph in paragraphs:
        if paragraph.lstrip().startswith(("#", "![", "```", "---")):
            continue
        candidate = plain_text(paragraph)
        if candidate:
            return candidate[:177].rstrip() + ("..." if len(candidate) > 177 else "")
    return None


def slugify(value: str) -> str:
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_value.lower()).strip("-")
    if not slug:
        fail("Could not derive a URL slug from the essay title; add a slug to the front matter.")
    return slug


def validate_artifact_links(body: str, assets_dir: Path) -> None:
    scannable_body = re.sub(r"```.*?```|~~~.*?~~~", "", body, flags=re.DOTALL)
    for raw_target in LINK_RE.findall(scannable_body):
        target = raw_target.strip("<>")
        if not target.startswith("assets/"):
            continue
        relative = Path(target)
        if ".." in relative.parts:
            fail(f"Artifact path cannot leave the post bundle: {target}")
        source = assets_dir.parent / relative
        if not source.is_file():
            fail(f"Referenced artifact does not exist: {source}")


def quoted(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def render_document(title: str, description: str, date: str, slug: str, body: str) -> str:
    return (
        "---\n"
        "layout: essay\n"
        f"title: {quoted(title)}\n"
        f"description: {quoted(description)}\n"
        f"date: {date}\n"
        f"slug: {slug}\n"
        "---\n\n"
        f"{body}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root")
    parser.add_argument("--date", help="Publication date in YYYY-MM-DD format")
    parser.add_argument("--update", action="store_true", help="Update an existing slug after approval")
    parser.add_argument("--dry-run", action="store_true", help="Validate and report without writing")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    inbox = root / "writing-inbox"
    source_path = inbox / "essay.md"
    assets_dir = inbox / "assets"

    if not source_path.is_file():
        fail(f"Essay input not found: {source_path}")

    metadata, body = split_front_matter(source_path.read_text(encoding="utf-8"))
    title = metadata.get("title") or title_from_body(body)
    if not title or title.casefold() == PLACEHOLDER_TITLE.casefold():
        fail("Replace the placeholder with the essay's title before publishing.")

    description = metadata.get("description") or description_from_body(body)
    if not description:
        fail("Add a description to the front matter or begin the essay with a prose paragraph.")

    publication_date = args.date or metadata.get("date") or dt.date.today().isoformat()
    try:
        dt.date.fromisoformat(publication_date)
    except ValueError:
        fail("Publication date must use YYYY-MM-DD format.")

    slug = metadata.get("slug") or slugify(title)
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        fail("Slug must contain lowercase letters, numbers, and single hyphens only.")

    body = strip_title_heading(body, title)
    validate_artifact_links(body, assets_dir)

    destination = root / "writing" / slug
    output_path = destination / "index.md"
    if destination.exists() and not args.update:
        fail(f"Published essay already exists at {destination}; ask before using --update.")

    document = render_document(title, description, publication_date, slug, body)
    if args.dry_run:
        print(f"Validated essay: {title}")
        print(f"Would publish to: {output_path}")
        return 0

    destination.mkdir(parents=True, exist_ok=True)
    output_path.write_text(document, encoding="utf-8")
    if assets_dir.is_dir():
        shutil.copytree(assets_dir, destination / "assets", dirs_exist_ok=True)

    print(f"Published essay bundle: {destination}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)
