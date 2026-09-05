# The Waiting City: how the counting works

Draft 1, Sept. 5, 2026. This document comes before the numbers. Nothing appears on the page unless it can be described in the terms below.

## 1. What this project measures

A line, for this project, is a set of people (or households, applications, cases or objects) who have formally asked a government body for a specific thing, have been accepted into a waiting state and have not yet received either the thing or a final decision.

Three tests, all required:

1. **A formal ask.** The person filed an application, a request, a complaint or a claim that the agency acknowledges as pending. Wanting something is not a line. Being eligible for something is not a line.
2. **A defined end.** There is an identifiable event that ends the wait: a voucher issued, a case decided, a permit granted or denied, a repair completed, a seat offered.
3. **A record.** The agency, a court, an oversight body or a public dataset records either how many are waiting, how long they wait, or both.

Excluded, with reasons, in Section 7.

## 2. Four kinds of measurement

Every figure in the registry is tagged with exactly one measurement type. They are not interchangeable and are never added together.

| Type | What it counts | Example | Trap |
|---|---|---|---|
| **Stock** | How many are waiting at one moment | 200,000 households on the Section 8 waitlist | A closed list stops growing without the need going away |
| **Duration** | How long a wait lasts | Average 45.5 days to start home attendant services | Completed waits vs. waits still in progress are different populations (Section 4) |
| **Timeliness rate** | Share handled within a stated standard | 67% of cash assistance applications processed within 30 days | Meaningless without the standard attached; the standard can be legal, administrative or self-set |
| **Throughput** | How many are cleared per period | NYCHA goal of 1,000 vouchers a month | Only becomes a wait estimate when divided into a stock, and then it is a derived figure (Section 5) |

## 3. Units, and why sums are mostly forbidden

Every figure carries a unit: **persons**, **households**, **applications**, **cases**, **requests**, **items** (an elevator, a tree, a sidewalk flag) or **seats**. These differ in ways that matter:

- One household can file many applications. Housing Connect received about six million applications in 2024. That is not six million households; one household applying to 50 lotteries is 50 applications. The registry records the figure as applications and says so.
- Applications are not the waitlist. NYCHA received 633,808 online applications for the 2024 Section 8 lottery and placed 200,000 households on the list. The stock is 200,000 households. The 633,808 measures demand at the door, a different quantity, recorded separately.
- One person can be on several lists at once. A family can be on the NYCHA public housing list, the Section 8 list and in a dozen Housing Connect lotteries. No dataset lets us deduplicate across agencies.

Consequence: **the registry does not produce one number for "New Yorkers waiting."** Where the page shows a total, it is a sum over a named set of lines that share a unit and a measurement type, labeled "sum of published counts, overlap across lists unknown." A sum across units is never shown.

## 4. Duration is two different things

"How long do people wait" has two honest answers and they can diverge by years:

- **Completed-wait duration**: among those who reached the end, how long it took. This is what agencies usually report. It cannot describe people who have not yet reached the end, and in a growing backlog it understates the wait of those still in line.
- **Waiting-so-far duration**: among those still in line, how long they have waited to date. Rarely published. It understates the eventual wait because none of these waits is over.

The registry tags every duration figure as one or the other, and as mean or median where the source says. Where the source does not say which, the figure is graded down (Section 6) and the ambiguity is printed next to it.

## 4a. Averages are not enough

A mean wait hides the people at the back of the line. For every duration and every timeliness figure the registry records whatever the source publishes about the spread, and prints it alongside the center:

- **Median and mean** both, when both exist. A mean far above the median means a long tail.
- **Percentiles or tail shares**: the 90th percentile, the share waiting over a threshold (over 30 days, over one year), the longest wait on record.
- **Breakdowns**: by borough, office, program type, household size or year of application, wherever the source disaggregates. The gap between the best-served and worst-served group is itself a registry field.
- **Over time**: the registry keeps every published period, not just the latest, so the reader can see whether the spread is widening.

Where the source publishes only an average, the entry says "average only; distribution not published" and the grade notes what would fill the gap. A single mean with no spread is presented as a partial measurement, not a fact about the line.

Two variability traps the registry names when they apply:

- A **timeliness rate** (share within 30 days) says nothing about how late the late ones are. 67% within 30 days is compatible with the other 33% taking 31 days or 300.
- An **average over a shrinking backlog** improves as the oldest cases are cleared, even if new applicants wait longer. The registry records the stock alongside the duration so this can be checked.

## 5. Derived figures

Some lines have a published stock and a published throughput but no published duration. Dividing one by the other (200,000 households at 1,000 vouchers a month is about 16.7 years) gives an implied wait under the assumption that the list is worked in order, nobody leaves it and throughput holds. Those assumptions are usually false. Derived figures are shown in a separate visual style, labeled "derived," with the arithmetic printed, and never mixed into totals.

## 6. Confidence grades

Each figure gets a grade based on who measured it and how it can be checked. The grade rates the measurement, not the agency.

| Grade | Criteria |
|---|---|
| **A** | Published as structured data by the agency or an oversight body, with a written indicator definition, refreshed on a schedule. We can re-query it. Example: Mayor's Management Report indicators on Open Data with a printed description. |
| **B** | Published by the agency or an oversight body (Comptroller, Independent Budget Office, court monitor, State Comptroller) in a report, testimony or rulemaking document, with a date. Not re-queryable; we hold a copy of the document. |
| **C** | Reported in the press with attribution to a named agency and a date, and we could not find the primary document. Or a primary document without a date or a definition. |
| **D** | Derived by us (Section 5), or a figure whose unit or definition the source leaves ambiguous. |

One more class sits alongside grade A: **computed**. Where an agency publishes only a mean, but also publishes record-level data (every permit filing with its dates, every complaint with open and close dates, every exam with its administration and results dates), this project computes the distribution itself: median, 90th percentile, share over a threshold, spread across boroughs or offices. Computed figures are graded **A-c**: re-queryable and fully specified, but produced by this project rather than the agency, so the code and the query are published with the figure and the agency's own mean is shown next to it for reconciliation. Where the two disagree, the disagreement is printed, not resolved quietly.

A grade C or D figure is never used in a headline or a total. It appears in the registry so the gap is visible, with a note on what would raise its grade (usually a Freedom of Information Law request, which is then logged).

## 7. What is left out

- **Service response that is not a queue in the sense above**: 911 and 311 response times are waits, but they are already measured by other projects and the request is not an application for a rationed thing. They are linked, not duplicated.
- **Court dockets** are state-run. They appear in a separate section labeled as state lines that New Yorkers stand in, never in city totals. The same for Access-A-Ride eligibility (Metropolitan Transportation Authority), cannabis licensing (state Office of Cannabis Management) and Department of Motor Vehicles waits.
- **Private waits** the city regulates but does not run (a landlord's repair, a hospital's appointment outside NYC Health + Hospitals).
- **Eligibility populations** ("X New Yorkers qualify for Y but do not receive it"). Not a line by test 1.
- **Lotteries as such.** A lottery entrant is not queued; a lottery winner placed on a waitlist is. Housing Connect application counts are recorded as demand, not stock.

## 8. Scope tiers

- **Tier 1**: mayoral agencies.
- **Tier 2**: city-controlled entities that are not mayoral agencies: New York City Housing Authority, NYC Health + Hospitals, Department of Education, Economic Development Corporation.
- **Tier 3**: state or independent bodies whose lines New Yorkers stand in. Shown apart.

## 9. Dates

Every figure carries the period it describes, printed as a date or date range ("first four months of fiscal 2026, July 1 to Oct. 31, 2025"), never as a relative phrase. Fiscal years are the city's (July to June) unless the source says otherwise. Where a source gives no date, the figure gets grade C at best and the publication date of the source is shown as an upper bound.

## 10. Refresh and provenance

Each registry entry records how its figure is refreshed: automated query (with the query stored), document re-fetch (with the URL and a hash of the copy we hold), manual (with the person and date) or FOIL pending (with the request date). Every number on the page opens the source and the verbatim sentence or table row it came from. Where our figure differs from a widely reported one, both are shown and the difference is explained.

## 11. What the agency's own words mean

Agencies define "timely," "processed," "pending" and "waitlist" differently, and the same agency changes definitions between years. The registry stores the source's own definition verbatim alongside each figure. Where the Mayor's Management Report changes an indicator's definition, the dataset's own description field is stored per fiscal year and breaks in the series are marked.


Two habits this project adopted after the first blind check:

- **Read the definition, not the title.** In the Mayor's Management Report dataset the title can say "median" while the definition says "average," or say "time to approve an applicant" while the definition starts the clock at the building's certificate of occupancy. Every registry line is described from the definition text, and where title and definition disagree the figure is graded B and the disagreement printed.
- **Decode the encoding.** Indicators labeled "(hours:minutes)" or "(minutes:seconds)" are stored as H.MM and M.SS, not decimals: 6.41 is six hours and 41 minutes. The registry stores the printed form and the decoded decimal side by side.

## 12. AI involvement

Research, source retrieval and drafting were done with Claude (Anthropic) working under Josh Greenman's direction. Every figure was traced to a source document or query that a reader can open. Claude can misread a document; the verbatim quote next to each figure exists so the reader does not have to trust the reading.
