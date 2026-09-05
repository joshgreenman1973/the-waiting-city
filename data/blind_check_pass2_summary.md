# Blind check, pass 2: definitions against sources

Checked Sept. 5, 2026. Scope: the 81 claims in data/blind_claims.json. For the 66 Mayor's Management Report claims the live `description` field of rbed-zzin was pulled for every indicator (129 rows each, description text identical across the series). For the 15 document and computed claims the local copies under sources/ were read, plus the full Comptroller audit PDF (MH18-058A.pdf), the source project's stats.json, the live column lists of w9ak-ipjd and ygpa-z7cr and a live row count of vx8i-nprf. The registry itself was not opened.

Result: 76 match, 5 mismatch, 0 cannot check. All five mismatches are wording or scope slips in caveats; no headline figure, unit, center or clock start was found wrong.

## Encoding check

The three time-span indicators encode the printed clock form as a decimal:

- NYCHA elevator outages (hours:minutes): 129 values, fractional part never above .58.
- NYCHA heat outages (hours:minutes): 82 values, fractional part never above .59.
- HRA benefits-center wait (minutes:seconds): 129 values, fractional part never above .59.

That is consistent with H.MM and M.SS across the whole series. Decoding to decimal hours or minutes is the right treatment.

## Remaining mismatches

1. parks-trees-sidewalks#0. The caveat says "Stale: fiscal 2017-18 data." The audit says "The scope of this audit was July 1, 2015 through December 31, 2017" and "1,069 sidewalks were repaired during Fiscal Year 2017 (July 1, 2016 through June 30, 2017)." The 419-day average is fiscal 2017 repairs and the audit covers fiscal 2016 and 2017, not 2017-18. The period_label's note that "the full report should be pulled" can be closed out with that scope sentence. Separately, the caveat describes the program page as having "a waitlist tier for sites rated 80 to 89 and a three-year expectation for 90 and above"; the page's chart reads "<80", "80-90" and "90-100", with "Site has been waitlisted" under 80-90 and "Site expected to be repaired within three years" under 90-100.

2. nycha-section8-waitlist#0. The caveat says "Households leave the list when housed, when they fail to respond or when found ineligible." The release supports only the eligibility part: "Being named to the waitlist does not necessarily guarantee receipt of a voucher, as applicant eligibility must be confirmed." Failure to respond is not in the source.

3. doe-3k-unlisted-placement#0. The caveat pairs "94,840 3-K and pre-K applications in 2025" with "about 27,000 of 136,000 seats unfilled." Chalkbeat's 136,000 is "seats for the city's free child care programs for children ages 4 and under," which includes infant and toddler care; 3-K plus pre-K capacity in the May 2025 story was roughly 117,000.

4. hpd-close-nonemergency#0. The caveat says "Scope is unique problems in privately owned buildings." Only the emergency indicator's definition says "unique"; the non-emergency definition reads "a nonemergency problem in a privately-owned building received before or during the period that was closed during the reporting period."

5. oath-hearing-decisions#0. The registry unit is "cases"; the definition divides "the total number of days decisions were pending" by "the total number of summonses heard and having a decision rendered." Summonses, not cases, and the figure is a ratio of pending-days to decisions rather than a straightforward per-case mean.

## Notes on matches worth a glance

- nycha-section8-waitlist-mmr#0: the indicator counts "families"; the registry says "households." HUD's "family" includes single persons, so the two are interchangeable here, but the definition's word is families. The caveat's monthly figures were confirmed live: 203 (July 2024), 205 (Aug. 2024), 197 (June 2025), thousands.
- hpd-housing-connect#0: the six-million sentence is in the reporter's voice; the Tigani attribution is inferred from the sentence that follows it.
- dcas-eligible-lists#0: live count on Sept. 5, 2026 was 403,777 rows, 855 exams, 432 titles, exactly as the caveat says; stats.json gives 1,674,337 removals and 452,206 appointments from certifications starting Nov. 7, 2007.
- The four HRA and ACS timeliness standards cite regulations (18 NYCRR 351.8, 7 CFR 273.2, 42 CFR 435.912, 18 NYCRR 415) that were not checked in this pass; the quoted definition text for each does match.
