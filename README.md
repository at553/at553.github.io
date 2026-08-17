# at553.github.io

Personal GitHub Pages site for Avinash Thangali.

## Local Preview

This site uses Jekyll so Markdown essays can be rendered with the existing design. Install the bundle, then run:

```sh
bundle install
bundle exec jekyll serve
```

Then visit `http://localhost:4000`.

## Publish an essay

1. Paste the finished Markdown into `writing-inbox/essay.md`.
2. Put that essay's images, PDFs, datasets, and other files in `writing-inbox/assets/` and reference them as `assets/filename.ext`.
3. Ask Codex to publish the essay with `$publish-essay`.

Published essays are organized as self-contained bundles under `writing/<slug>/`, with the Markdown at `index.md` and artifacts in the adjacent `assets/` directory. The Writing archive updates automatically during the Jekyll build.

Every pushed branch receives a GitHub-hosted Jekyll build check. Merges to `master` deploy the generated site automatically through GitHub Pages.

## Structure

- `index.html` contains the home page content and metadata.
- `css/grayscale.css` contains the custom responsive styles.
- `img/me.jpg` is the profile image used on the page and in link previews.
- `writing-inbox/` is the stable authoring location for the next essay and its artifacts.
- `.agents/skills/publish-essay/` contains the repository-local publishing workflow.
- `_layouts/essay.html` controls the generated essay pages.
