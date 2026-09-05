# Blind check, pass 3

Checked all 81 claims in data/blind_claims.json on Sept. 5, 2026 without opening the registry, the queue files, the computed files or scripts/. Sources used: the local copies under sources/, the live rbed-zzin dataset (66 claims), fresh recomputations from w9ak-ipjd and ygpa-z7cr, the live vx8i-nprf dataset and nyc-civil-service-hiring/data/stats.json.

Counts: 81 claims; definition_check match 77, mismatch 4, cannot check 0. 29 claims carry at least one problem note; 33 problem notes in total. Confidence: high 76, medium 5, low 0.

## Values extracted

Every rbed-zzin indicator returned a value except Medicaid timeliness, which needed 129 rows rather than 20 to reach its last non-NA figure (88.4, June 2024). The Section 8 waitlist (000) indicator reads 202, i.e. 202,000 families, multiplication_factor 1000. The three time-format indicators (elevator 6.41 hours:minutes, heat 7.12 hours:minutes, HRA counter wait 96.38 minutes:seconds) are consistent with H.MM / M.SS encoding: no fractional part in any FY2026 row exceeds .59, though the dataset never says so.

DOB recomputation (w9ak-ipjd, approvals Sept. 1, 2025 to Aug. 31, 2026): n 141118, median 6.87 days, p90 89.49 days; Professional Certification median 1.62 days (n 65704), Standard Plan Examination median 27.14 days (n 75414). Because filing_date is date-only and approved_date has a time of day, a date-only computation gives median 6.0 and p90 89.0.

HPD recomputation (ygpa-z7cr, problems closed March 1 to Aug. 31, 2026, duplicates excluded): n 377002 (37659 duplicate rows dropped), median 8.27 days, p90 67.19 days; by type: EMERGENCY median 6.11 (n 177038); IMMEDIATE EMERGENCY median 2.24 (n 17122); NON EMERGENCY median 12.68 (n 182842).

Civil service: live vx8i-nprf holds 403,777 rows, 855 exams, 432 titles on Sept. 5, 2026; stats.json (generated 2026-07-13) says 403,200 candidates, 850 exams, 428 titles, 452,206 appointed and 1,674,337 removed since 2007. All match the registry caveats.

## Mismatches

- dcas-eligible-lists#0: 'Lists last up to four years' / 'expire after at most four years' is contradicted by extension_date on 92,636 rows; 88,082 current entries are on lists past their four-year anniversary.
- parks-trees-sidewalks#0: Unit 'requests' vs source '1,069 repaired sidewalks' (work orders). Period label details (scope July 1, 2015-Dec. 31, 2017; fiscal 2017) are absent from the local copy in sources/ and verified only against the live full PDF, which should be added to sources/.
- dcwp-license-processing#0: Registry caveat generalizes the applicant-pending exclusion to all applications; source text limits it to 'the renewal'.
- bic-waste-hauling-pending-age#0: Value selection: acceptedvalueytd 257 is a fiscal-year average of monthly pending ages; the March 2026 snapshot is 223. Registry period label promises the as-of-March value for point-in-time measures.

## All problem notes, by claim

- nycha-section8-waitlist#0 (match): Release uses four unit words for 200,000 (households, applications, applicants, New Yorkers); registry caveat cites two.
- dob-filing-to-approval-computed#0 (match): Single median masks a bimodal split by filing_review_type (about 1.6 vs 27 days).
- dob-filing-to-approval-computed#0 (match): Timestamp vs date-only computation changes the median by up to a day; registry should state which it used.
- hpd-problem-close-computed#0 (match): Registry caveats do not mention the duplicate-flag exclusion or the emergency/non-emergency split.
- dcas-eligible-lists#0 (mismatch): 'Lists last up to four years' / 'expire after at most four years' is contradicted by extension_date on 92,636 rows; 88,082 current entries are on lists past their four-year anniversary.
- hpd-housing-connect-furman#0 (match): Registry omits the clock start (receipt of a log number) and the exclusions (appeals, complaints, HPD audit) the report states.
- hpd-housing-connect-furman#1 (match): Wording: source 'nearly 600,000', registry 'roughly 600,000'.
- doe-3k-unlisted-placement#0 (match): 'including infant and toddler care' is inferred, not stated, in the Jan. 30, 2026 Chalkbeat text.
- parks-trees-sidewalks#0 (mismatch): Unit 'requests' vs source '1,069 repaired sidewalks' (work orders).
- parks-trees-sidewalks#0 (mismatch): Period label details (scope July 1, 2015-Dec. 31, 2017; fiscal 2017) are absent from the local copy in sources/ and verified only against the live full PDF, which should be added to sources/.
- housing-court-eviction-cases#0 (match): Source contradicts itself on the moratorium end (January 2021 in the intro vs January 15, 2022 in the body); registry notes only the intro-vs-key-findings difference.
- nycha-section8-waitlist-mmr#0 (match): Unit word: source says 'families', registry says 'households'.
- nycha-elevator-outages#0 (match): Encoding as hours:minutes is inferred from the title and measurement_type, not stated in the description; the registry should say so.
- nycha-heat-outages#0 (match): FYTD value averages only heating-season months; July-Sept rows are 0.00.
- nycha-emergency-transfer#0 (match): Unit word: source says 'cases', registry says 'requests'.
- hpd-section8-voucher-issuance#0 (match): Period label 'through quarter beginning Oct. 2025' is not supported by the dataset; the source only gives valuedate 2025-10-01 (and an identical 78 at 2025-09-01).
- hpd-section8-voucher-issuance#0 (match): Unit: description counts 'applications'; registry says 'households'.
- hpd-section8-lease-up#0 (match): Period label 'through quarter beginning Oct. 2025' is not supported by the dataset (valuedate 2025-10-01; identical 137 at 2025-09-01).
- hpd-lottery-project-approvals#0 (match): Source description is internally garbled ('from the certificate of occupancy issuance to approval to completion of 95%').
- hpd-homeless-voluntary-leaseup#0 (match): Source description typos: 'revealed TCO' and 'HPS'.
- hpd-close-emergency#0 (match): Unit inconsistency inside the registry: 'requests' here vs 'items (problems...)' on hpd-problem-close-computed for the same object; source says 'problems'.
- hpd-close-nonemergency#0 (match): Unit: source 'problem', registry 'requests'.
- hra-cash-assistance-timeliness#0 (match): end_event 'accepted or denied' is not the source's wording ('application processing completed').
- hra-snap-timeliness#0 (match): Nov. 2025 monthly and YTD values are blank in the dataset.
- hra-medicaid-timeliness#0 (match): Caveat wording: data are unavailable after fiscal 2024 (from fiscal 2025), not 'since fiscal 2024'.
- hra-medicaid-timeliness#0 (match): Query per instructions ($limit=20) returns no non-NA row; had to widen to 129 rows.
- hra-hasa-timeliness#0 (match): end_event 'approved or denied' vs source 'processed'.
- dhs-los-adult-families#0 (match): Caveat overstates: adult-families and families-with-children definitions are word-for-word the same; only single adults differs.
- dcp-simple-zoning-review#0 (match): Caveat about DCP publishing applicant-vs-agency time split is not in this source (cannot check here).
- dcwp-license-processing#0 (mismatch): Registry caveat generalizes the applicant-pending exclusion to all applications; source text limits it to 'the renewal'.
- bic-waste-hauling-pending-age#0 (mismatch): Value selection: acceptedvalueytd 257 is a fiscal-year average of monthly pending ages; the March 2026 snapshot is 223. Registry period label promises the as-of-March value for point-in-time measures.
- cchr-open-matters#0 (match): Source says 'matters'; registry assumes these are discrimination complaints.
- oath-special-ed-hearings#0 (match): Period label 'through quarter beginning Mar. 2026' is not supported; rows fall at Sept./Dec./March, which are fiscal quarter ends.

## Things that checked out and are worth saying

- NYCHA press release: 200,000; 633,808 online and 4,416 paper applications; the 1,000-a-month goal 'contingent on funding and the authorized voucher capacity'; 'Last year, NYCHA issued 7,538 vouchers'; the Sept. 29, 2025 pause ('NYCHA must temporarily pause voucher issuance and outreach to applicants on the general HCV waitlist'); and the MMR trail 203,000 (July 2024), 205,000 (Aug. 2024), 197,000 (June 2025) all verified.
- Gothamist: 5,236 people (food, Department of Health) and about 8,900 people (general merchandise, DCWP); 853 cap since 1979; NYC Rules pages confirm the Dec. 12, 2021 effective date, 'full-term permit waiting list', up to 445 permits a year for 10 years from July 1, 2022, and Local Law 54 of 2026.
- Furman: 118-day median from log number to approval for an offer, about 64,000 applications in 101 buildings, sample 'more likely to result in overestimates of processing times', 'nearly 600,000 unique Housing Connect applicants', HPD's 142 days in fiscal 2025.
- Chalkbeat 2025: 'Roughly 15% of 3-K applicants, more than 6,000 students'; CBS 2024: 'more than 2,400 ... out of the 43,000 who applied'; Chalkbeat 2026: 94,840 applications, 'more than 27,000 of roughly 136,000 seats', offer for any family applying by the deadline.
- Comptroller trees audit: 419-day mean over 1,069 repaired sidewalks; 30-day SLA missed by 71 days; no repair target. Parks page: 80-90 waitlisted, 90-100 within three years, below 80 hire a contractor.
- Comptroller evictions: about 33,000 to 177,000 active cases, March 2020 to March 2024 in the key findings.
- Of the 66 rbed-zzin descriptions, 64 match the registry's plain-language reading on center (mean/median), clock start and stop, calendar vs business days, and the exclusions the registry lists. Registry caveats that quote the description ('the definition does not call it a standard', 'first physical inspection attempt', 'received before or during the period', 'Includes both HPD processing times, as well as search times') are verbatim-accurate.
