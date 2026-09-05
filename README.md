# The Waiting City

How many New Yorkers are standing in a line the city controls, and how long each line is. A registry of queues, with every figure tied to a source document or a re-runnable query, graded by how it was measured, and carrying whatever the source says about the spread, not just the average.

Status, Sept. 5, 2026: definitions and registry stage, three blind-check passes run. No page yet. See data/blind_check_report.md and data/gaps.md.

- [METHODOLOGY.md](METHODOLOGY.md): what counts as a line, the four measurement types, units and why they are never summed, completed vs. waiting-so-far durations, variability requirements, confidence grades, exclusions, scope tiers.
- [data/registry.json](data/registry.json): the registry. Built by `scripts/build_registry.py` from:
  - `data/queues_manual.json`: hand-sourced lines (press releases, testimony, audits, research reports, computed distributions), each with a verbatim quote.
  - `data/mmr_lines.json` + `data/mmr_series.json`: lines drawn from the Mayor's Management Report indicators dataset (rbed-zzin), with the dataset's own definition text per figure and the full fiscal-year series. Fetched by `scripts/fetch_mmr.py` from the list in `data/mmr_selected.txt`.
- `data/registry_schema.md`: field definitions.
- `scripts/compute_dob.py`, `scripts/compute_hpd.py`: distributions computed from record-level Open Data (grade A-c), outputs in `data/computed_*.json`.
- `scripts/blind_check.py`: independent re-verification (see below).
- `sources/`: local copies of every document cited (PDF and extracted text).

## Fact-checking

Two passes, both recorded in `data/blind_check_report.md`:

1. Mechanical: every Mayor's Management Report figure is re-queried from Open Data by agency and indicator name alone and compared to the registry; every document figure's verbatim quote is searched for in the local copy of the source.
2. Blind: a reader who has not seen the registry's values is given each figure's source and a neutral description of the quantity, extracts the value independently, and the two are diffed. The same reader compares each line's name, "what for," end event, unit and center (mean/median) against the source's own definition text, word by word.

## Rules carried over from other projects

Facts only, no characterization. Every window printed as an explicit date range. Every number opens its source. AP style, sentence case, no serial comma, "New York City" in full, straight quotes.
