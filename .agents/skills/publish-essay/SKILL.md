---
name: publish-essay
description: Publish or prepare essays for Avi Thangali's website from Markdown, including images, downloads, and other post-specific artifacts. Use when asked to create an essay draft, publish or update a writing entry, add an essay to the Writing archive, or manage the writing inbox and published writing bundles.
---

# Publish Essay

Use the repository's single authoring bundle:

- Markdown input: `writing-inbox/essay.md`
- Images and other artifacts: `writing-inbox/assets/`

Keep Markdown artifact references relative, such as `![Diagram](assets/diagram.png)` or `[Download the data](assets/data.csv)`. The publisher preserves those paths inside the finished post bundle.

## Prepare a draft

1. Put the essay Markdown in `writing-inbox/essay.md`, or write user-provided essay text there.
2. Put every essay-specific image, PDF, dataset, or download in `writing-inbox/assets/`.
3. Use one level-one Markdown heading as the title. Optionally add YAML front matter with `title`, `description`, `date`, or `slug`; infer missing values from the heading and first prose paragraph.
4. Do not publish unless the user explicitly asks to publish.

## Publish

1. Inspect the inbox Markdown and assets. Require descriptive alt text for meaningful images.
2. From the repository root, run:

   `python3 .agents/skills/publish-essay/scripts/publish_essay.py`

3. The script creates `writing/<slug>/index.md` and copies artifacts to `writing/<slug>/assets/`. Never split one post's artifacts into a shared image directory.
4. If the destination slug already exists, stop and ask whether to update the existing essay or use a different slug. After explicit approval, rerun with `--update` to update without deleting existing artifacts.
5. Inspect the generated front matter, Markdown links, output bundle, and Writing archive behavior.
6. Run `bundle exec jekyll build` when Jekyll dependencies are available. Otherwise, run the repository's structural checks and let GitHub Pages perform the authoritative Jekyll build.
7. Follow the repository `AGENTS.md` instructions for validation, pull request creation, merging, and cleanup.

## Preserve content

- Do not rewrite the author's prose unless asked.
- Do not delete or replace inbox or published artifacts without explicit direction.
- Keep published URLs stable. Treat a slug change as a redirect-requiring change and ask before proceeding.
- Keep styling consistent across desktop and mobile. Ask before introducing breakpoint-specific differences that cannot mirror each other.
