# Data cleaning and string operations

STAT 386 lecture site, slides, and follow-along notebook. The talk records are **illustrative teaching data**. Speaker names are used only as familiar examples; the titles and word counts are invented.

## Run locally

1. Install [Quarto](https://quarto.org/docs/get-started/) and [uv](https://docs.astral.sh/uv/getting-started/installation/) if needed.
2. Run `uv sync` from this folder.
3. Open `follow-along.ipynb` in Positron and select this project's `.venv` kernel. If the kernel is not listed, run `uv run python -m ipykernel install --user --name stat386-cleaning --display-name "STAT 386 cleaning"`.
4. Run `quarto render` to build the site in `docs/`, or `quarto preview` while editing.

The included `docs/` directory is ready to serve on GitHub Pages. It was built from the Quarto source with the local preview builder. If Quarto is not installed, `python tools/build_preview.py` refreshes that offline HTML preview. `quarto render` produces the native Quarto site and is the preferred build command.

The slides display their outputs directly. The notebook imports `cleaning.py` and uses the same bundled CSV data. It asks students to build a first cleaning function, then inspects the complete versions in `cleaning.py`. `index.qmd` links to both the slides and notebook.

## GitHub Pages

Publish from the same repository: in the repository's **Settings → Pages**, select **Deploy from a branch**, the default branch, and `/docs`. Commit the rendered `docs/` directory after `quarto render`. The site uses relative links and does not require a repository name or custom URL in `_quarto.yml`. The source repo remains the single instructor and student repository.

## Teaching flow (50 minutes)

| Time | Activity |
| --- | --- |
| 0–5 | Missingness warmup and debrief |
| 5–11 | A failed join or split group caused by messy speaker text |
| 11–20 | Predict string operation results, including missing values |
| 20–31 | Follow-along: turn operations into a function and verify outputs |
| 31–39 | Think, pair, share: new batch reveals an internal-space bug |
| 39–47 | Slide examples: v1/v2 numeric scales, saved values, compatibility, reprocessing |
| 47–50 | Exit question and transition to regex |

The version examples are discussions shown in the slides. There is no live implementation of a pipeline versioning system.
