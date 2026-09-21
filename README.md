# Sakura Notes

A bilingual AI glossary, published at **https://anaclacp.github.io/sakura-notes/**.

## Updating the glossary

Edit `others/ai-glossary.md` in `anaclacp/ai-agents-in-action`, then commit and
push to `main`. No build commands or updates to this repository are needed.

The source repository remains private. Its synchronization workflow copies
only that Markdown document and its source commit identifier into this public
repository. It uses a dedicated SSH deploy key scoped to Sakura Notes, stored
as the encrypted `SAKURA_SYNC_KEY` secret in the source repository.

A push starts the source workflow, then this repository builds and publishes
GitHub Pages. Allow a few minutes, or longer when new translations require
downloading the language model. Nothing runs on the author's computer.

Do not edit `content/glossary.md` here: the next synchronization overwrites it.
To retry synchronization, open **Actions > Sync glossary to Sakura Notes >
Run workflow** in the source repository. To retry only publication, use
**Actions > Publish Sakura Notes > Run workflow** here.

## Portuguese translations

Existing translations are retained in `glossary_pt-BR.json`. Each entry's
English source hash is tracked in `translation_state.json`. Only new or
changed definitions are translated; removed entries are removed from the
translation cache. The workflow commits successful translation updates here.

Automatic translations use the open-source Argos English-to-Portuguese model
on the Actions runner, without a paid translation API or external inference
service. These are machine translations, not guaranteed Brazilian technical
terminology. The original English remains available beside the Portuguese
title and through the language selector. Code examples are preserved.

To improve a translation, edit its `term` and/or `html` in
`glossary_pt-BR.json`. Your correction is kept until its English definition
changes. Avoid editing the source hashes by hand. No API billing is enabled;
the small synchronization job uses the private source repository's existing
GitHub Actions allowance.

If validation, translation or deployment fails, the last successful site stays
online. Check the red workflow run in **Actions**, correct the error, and rerun.
No partial translation set is published.

## Local development

Python 3.12+:

```sh
python -m venv .venv
# Activate .venv for your shell.
python -m pip install -r requirements.txt
python sync_translations.py --check
# Needed only when the check reports new or changed translations:
python -m pip install -r requirements-translation.txt
python sync_translations.py
python build_html.py --output _site/index.html
python -m unittest discover -s tests -v
python tests/check_site.py _site/index.html
```

Open `_site/index.html` directly. The HTML embeds fonts, artwork, styles,
translations and scripts, so no development server is required. Generated
HTML and local environments are excluded from Git. Pages receives only the
`_site` artifact, not the build scripts or source repository.

The optional `test_translation` input in the publication workflow runs an
additional real-engine integration test. Parser, cache synchronization and
artifact checks run on every publication.

For the browser checks, install Playwright in your development environment and
run `node tests/browser.cjs`; set `SITE_URL` to test the published website or
`PLAYWRIGHT_CHANNEL=chrome` to use an installed Chrome browser.

## Credits

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for the Uiverse selector,
bundled font licenses and sakura artwork. Build dependencies retain their
respective licenses and are not included in the browser artifact.
