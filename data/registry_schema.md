# Registry fields (data/queues.json)

Each entry is one line. Each line has one or more `figures`. Fields follow METHODOLOGY.md.

- `id`: slug
- `name`: plain-language name of the line
- `agency`, `tier` (1 mayoral agency, 2 city-controlled entity, 3 state/independent)
- `what_for`: the thing being waited for
- `end_event`: what ends the wait
- `unit`: persons | households | applications | cases | requests | items | seats
- `list_status`: open | closed | lottery-gated | rolling | n/a
- `figures[]`:
  - `type`: stock | duration | timeliness_rate | throughput | demand | derived
  - `value`, `unit_of_value` (count, days, minutes, percent, per month)
  - `center`: mean | median | n/a; `spread`: object of whatever is published (p90, share_over_threshold, min, max, by_group) or `null` with `spread_note`
  - `duration_kind`: completed | waiting_so_far | n/a
  - `standard`: the threshold behind a timeliness rate, with its legal basis
  - `period_start`, `period_end` (ISO), `period_label` (printed form)
  - `source`: {url, title, publisher, date, quote (verbatim), retrieved, local_copy}
  - `definition_quote`: the source's own definition of the indicator, verbatim, or null
  - `grade`: A | B | C | D, `grade_reason`
  - `refresh`: {method: soql | document | manual | foil_pending, query_or_url}
  - `caveats[]`
- `related_lines[]`, `duplicates_with[]` (other lines the same household may be on)
- `raise_grade`: what would move it up (usually a FOIL, with the request logged)
