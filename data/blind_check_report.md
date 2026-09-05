# Blind check report

Pass 1 (values and definitions) ran against the registry as built at about 14:00 ET on Sept. 5, 2026, with the checker blind to every registry value. It found 32 definition mismatches and about 20 further notes (data/blind_check_agent_summary.md); every one was then addressed in data/mmr_lines.json and data/queues_manual.json and the registry rebuilt. Pass 2 re-checked the corrected descriptions against the sources (data/blind_check_pass2_summary.md): 76 match, 5 caveat-wording issues, all corrected. Pass 3 was a fresh checker barred from the registry and from both earlier check files (data/blind_check_pass3_summary.md): values agreed on every figure; 4 definition mismatches and 33 notes, all addressed in the rebuild at about 17:15 ET, including a switch to the month value (dataset field acceptedvalue) for point-in-time counts, which the fiscal-year-to-date field had been averaging. Source-internal defects the passes surfaced are listed in data/source_issues.md. Pass 2 and 3 notes shown below describe the registry text as it stood before each fix.

Values: 79 figures compared, 78 agree with the checker's independent extraction, 1 do not.

| claim | line | value result / remaining definition issue | pass 2 definition |
|---|---|---|---|
| nycha-section8-waitlist#0 | Section 8 Housing Choice Voucher waitlist | PASS-2 DEFINITION: 200,000 households; release: '200,000 households randomly selected via lottery' and later 'a total of 200,000 applications were randomly selected by lottery' -- both units present, caveat correct. 'will continue to be served and did not have to reapply' verbatim. MMR series checked live: July 2024 = 203, Aug 2024 = 205, June 2025 = 197 (thousands), as the caveat says. One unsupp | mismatch |
| nycha-section8-waitlist#1 | Section 8 Housing Choice Voucher waitlist | PASS-3 VALUE registry=633808 checker={'online': 633808, 'paper': 4416, 'total': 638224} | match |
| nycha-section8-waitlist#2 | Section 8 Housing Choice Voucher waitlist | match | match |
| nycha-section8-waitlist#3 | Section 8 Housing Choice Voucher waitlist | match | match |
| hpd-housing-connect#0 | Housing Connect affordable housing lotteries | match | match |
| dohmh-food-vendor-permit-waitlist#0 | Food vendor waiting list (Department of Health) | match | match |
| dcwp-general-vendor-waitlist#0 | General vendor license waitlist | match | match |
| dob-filing-to-approval-computed#0 | DOB NOW filings: filing to approval (computed distribution) | PASS-3 NOTE: Single median masks a bimodal split by filing_review_type (about 1.6 vs 27 days).; PASS-3 NOTE: Timestamp vs date-only computation changes the median by up to a day; registry should state which it used. | match |
| hpd-problem-close-computed#0 | HPD housing complaint problems: received to closed (computed distribution) | PASS-3 NOTE: Registry caveats do not mention the duplicate-flag exclusion or the emergency/non-emergency split. | match |
| dcas-eligible-lists#0 | Civil service eligible lists | PASS-3 VALUE registry=403200 checker={'live_2026_09_05': {'rows': 403777, 'exams': 855, 'titles': 432}, 'stats_json_2026_07_13': {'candidates': 403200, 'exams': 850, 'titles': 428, 'oldest_list': '2018-02-14', 'newest_list': '2026-07-01'}, 'funnel': {'appointed': 452206, 'removed_total': 1674337}}; PASS-3 DEFINITION: Counts, the 1.67 million removals and 452,206 appointments, and the Sept. 5 live  | match |
| hpd-housing-connect-furman#0 | Housing Connect: verification and approval (Furman Center sample) | PASS-3 NOTE: Registry omits the clock start (receipt of a log number) and the exclusions (appeals, complaints, HPD audit) the report states. | match |
| hpd-housing-connect-furman#1 | Housing Connect: verification and approval (Furman Center sample) | PASS-3 NOTE: Wording: source 'nearly 600,000', registry 'roughly 600,000'. | match |
| parks-trees-sidewalks#0 | Trees and Sidewalks repair program | PASS-2 DEFINITION: Landing page: 'our review of 1,069 repaired sidewalks found that the average time from inspection to repair was 419 days'; 'homeowners had to wait an average of 101 days ... 71 days longer than the 30 day internal DPR SLA'; 'does not have a target time frame'; eligibility 'owner occupied one-, two-, and three-family homes (property tax class 1)'. Those match. Two mismatches: (1) | mismatch |
| housing-court-eviction-cases#0 | Housing Court active eviction cases | PASS-3 NOTE: Source contradicts itself on the moratorium end (January 2021 in the intro vs January 15, 2022 in the body); registry notes only the intro-vs-key-findings difference. | match |
| nycha-section8-waitlist-mmr#0 | Section 8 voucher waiting list (Mayor's Management Report count) | PASS-3 NOTE: Unit word: source says 'families', registry says 'households'. | match |
| nycha-vacant-unit-turnaround#0 | Turnaround of vacant public housing apartments | match | match |
| nycha-maintenance-work-orders#0 | NYCHA maintenance work orders | match | match |
| nycha-skilled-trades-work-orders#0 | NYCHA skilled-trades and vendor work orders | match | match |
| nycha-elevator-outages#0 | NYCHA elevator outages | PASS-3 NOTE: Encoding as hours:minutes is inferred from the title and measurement_type, not stated in the description; the registry should say so. | match |
| nycha-heat-outages#0 | NYCHA heat outages | PASS-3 NOTE: FYTD value averages only heating-season months; July-Sept rows are 0.00. | match |
| nycha-nonemergency-service-requests#0 | NYCHA non-emergency service requests | match | match |
| nycha-nonemergency-within-15#0 | NYCHA non-emergency requests within 15 days | match | match |
| nycha-nonemergency-within-60#0 | NYCHA non-emergency requests within 60 days | match | match |
| nycha-emergency-transfer#0 | NYCHA emergency transfer requests | PASS-3 NOTE: Unit word: source says 'cases', registry says 'requests'. | match |
| hpd-section8-voucher-issuance#0 | HPD Section 8: completed application to voucher | PASS-3 NOTE: Period label 'through quarter beginning Oct. 2025' is not supported by the dataset; the source only gives valuedate 2025-10-01 (and an identical 78 at 2025-09-01).; PASS-3 NOTE: Unit: description counts 'applications'; registry says 'households'. | match |
| hpd-section8-lease-up#0 | HPD Section 8: voucher to lease | PASS-3 NOTE: Period label 'through quarter beginning Oct. 2025' is not supported by the dataset (valuedate 2025-10-01; identical 137 at 2025-09-01). | match |
| hpd-lottery-applicant-approval#0 | Housing Connect: certificate of occupancy to applicant approval | match | match |
| hpd-lottery-project-approvals#0 | Housing Connect: certificate of occupancy to 95% of applicant approvals | PASS-3 NOTE: Source description is internally garbled ('from the certificate of occupancy issuance to approval to completion of 95%'). | match |
| hpd-homeless-setaside-leaseup#0 | Homeless set-aside units in new construction: lease-up | match | match |
| hpd-homeless-voluntary-leaseup#0 | Homeless voluntary units in new construction: lease-up | PASS-3 NOTE: Source description typos: 'revealed TCO' and 'HPS'. | match |
| hpd-inspection-heat#0 | HPD heat and hot water complaints: first inspection | match | match |
| hpd-inspection-nonemergency#0 | HPD non-emergency complaints: first inspection | match | match |
| hpd-close-emergency#0 | HPD emergency complaint problems: close | PASS-3 NOTE: Unit inconsistency inside the registry: 'requests' here vs 'items (problems...)' on hpd-problem-close-computed for the same object; source says 'problems'. | match |
| hpd-close-nonemergency#0 | HPD non-emergency complaint problems: close | PASS-2 DEFINITION: Definition: 'The median number of calendar days to close a nonemergency problem in a privately-owned building received before or during the period that was closed during the reporting period. Problems can be closed due to an inspection, callback to tenant, or repeated attempts for access.' Registry caveat says 'Scope is unique problems in privately owned buildings' -- the word ' | mismatch |
| hra-cash-assistance-timeliness#0 | Cash assistance applications decided on time | PASS-3 NOTE: end_event 'accepted or denied' is not the source's wording ('application processing completed'). | match |
| hra-snap-timeliness#0 | SNAP applications decided on time | PASS-3 NOTE: Nov. 2025 monthly and YTD values are blank in the dataset. | match |
| hra-medicaid-timeliness#0 | Medicaid applications decided on time | PASS-3 NOTE: Caveat wording: data are unavailable after fiscal 2024 (from fiscal 2025), not 'since fiscal 2024'.; PASS-3 NOTE: Query per instructions ($limit=20) returns no non-NA row; had to widen to 129 rows. | match |
| hra-idnyc-timeliness#0 | IDNYC cards issued on time | match | match |
| hra-hasa-timeliness#0 | HASA rental assistance applications decided on time | PASS-3 NOTE: end_event 'approved or denied' vs source 'processed'. | match |
| hra-home-care-initiation#0 | Home attendant and housekeeper services: start of care | match | match |
| dhs-los-families-children#0 | Families with children in shelter: length of stay | match | match |
| dhs-los-single-adults#0 | Single adults in shelter: length of stay | match | match |
| dhs-los-adult-families#0 | Adult families in shelter: length of stay | PASS-3 NOTE: Caveat overstates: adult-families and families-with-children definitions are word-for-word the same; only single adults differs. | match |
| acs-child-care-eligibility#0 | Child care assistance eligibility decided on time | match | match |
| hh-third-next-adult#0 | NYC Health + Hospitals: new adult primary care appointment | match | match |
| hh-third-next-pediatric#0 | NYC Health + Hospitals: new pediatric appointment | match | match |
| dcas-exam-results#0 | Civil service exam results | match | match |
| dof-scrie-initial#0 | SCRIE initial applications | match | match |
| dof-drie-initial#0 | DRIE initial applications | match | match |
| dof-sche-initial#0 | SCHE initial applications | match | match |
| dof-dhe-initial#0 | DHE initial applications | match | match |
| dof-property-tax-refund#0 | Property tax refunds | match | match |
| dof-parking-hearing-mail#0 | Parking summons hearings by mail | match | match |
| dof-parking-hearing-inperson#0 | Parking summons hearings in person | match | match |
| dob-filing-to-approval#0 | DOB NOW filings: filing to approval | match | match |
| dob-first-plan-review#0 | DOB NOW filings: first plan review | match | match |
| dob-first-plan-review-nb#0 | DOB NOW new building filings: first plan review | match | match |
| dob-inspection-construction#0 | DOB construction inspections | match | match |
| dob-inspection-electrical#0 | DOB electrical inspections | match | match |
| dob-inspection-plumbing#0 | DOB plumbing inspections | match | match |
| dcp-simple-zoning-review#0 | Simple zoning actions: pre-certification | PASS-3 NOTE: Caveat about DCP publishing applicant-vs-agency time split is not in this source (cannot check here). | match |
| dcp-eas-zoning-review#0 | Zoning actions with an environmental assessment: pre-certification | match | match |
| dcp-eis-zoning-review#0 | Zoning actions with an environmental impact statement: pre-certification | match | match |
| dcwp-license-processing#0 | DCWP license applications | PASS-3 DEFINITION: Description: 'median number of calendar days required to process new and renewal applications for DCWP-issued licenses. Licenses requiring approval by outside agencies, special inspections, mandatory waiting periods, or extensive legal review are excluded ... Days where the renewal is pending additional information from the applicant or clearance of certain requirements ... are  | match |
| dcwp-license-within-30#0 | DCWP license applications within 30 days | match | match |
| dcwp-licensing-center-wait#0 | DCWP Licensing Center in-person wait | match | match |
| dohmh-birth-certificates#0 | Birth certificate requests | match | match |
| dohmh-death-certificates#0 | Death certificate requests | match | match |
| doris-vital-records#0 | Municipal Archives vital record requests | match | match |
| dot-permit-processing#0 | DOT permit applications | match | match |
| bic-waste-hauling-pending-age#0 | Waste hauling license applications: age of pending | VALUE registry=223.0 checker=257; PASS-3 VALUE registry=223.0 checker=257; PASS-3 DEFINITION: Description: 'average number of days new waste hauling license and registration applications are pending, from the date of the filing through the current reporting period. This does not include applications slated for denial or under long-term investigation.' Registry text matches. But the value: accepted | match |
| bic-waste-hauling-approval#0 | Waste hauling license applications: time to approve | match | match |
| bic-waste-hauling-pending#0 | Waste hauling license applications pending | match | match |
| cchr-caseload-age#0 | Human Rights Commission complaints: age of open caseload | match | match |
| cchr-open-matters#0 | Human Rights Commission open matters | PASS-3 NOTE: Source says 'matters'; registry assumes these are discrimination complaints. | match |
| oath-hearing-decisions#0 | OATH hearings: decision after hearing | PASS-2 DEFINITION: Definition: 'The average time decisions were pending at the OATH Hearings Division calculated by dividing the total number of days decisions were pending at the Hearings Division by the total number of summonses heard and having a decision rendered at the OATH Hearings Division during the reporting period.' Registry unit is 'cases'; the definition counts summonses. The figure is | mismatch |
| oath-trials-decisions#0 | OATH Trials Division decisions | match | match |
| oath-special-ed-hearings#0 | Special education impartial hearings | PASS-3 NOTE: Period label 'through quarter beginning Mar. 2026' is not supported; rows fall at Sept./Dec./March, which are fiscal quarter ends. | match |
| lpc-minor-work-permits#0 | Landmarks permits for minor work within 10 business days | match | match |
