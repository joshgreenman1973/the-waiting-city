# Blind check, agent pass

Checked 81 claims on Sept. 5, 2026 without opening the registry: 66 rbed-zzin indicators queried live, 12 document or derived claims read from sources/, 3 recomputed from Open Data with fresh code.

Definition check: 49 match, 32 mismatch, 0 cannot check.

## Mismatches

- **dohmh-food-vendor-permit-waitlist#0** (value 5236): Source says 'waitlist for food vendor licenses'; registry says 'permit'. Registry adds 'full-term'/'year-round', which the source does not say. Registry caveat on 'Local Law 54 of 2026' cannot be checked here: the Dec. 18, 2025 source describes a bill passed by Council, not yet law.
- **hpd-housing-connect-furman#0** (value 118): Period: the report states no date range for its sample; the registry period label implies one exists. 'one software vendor' is not in the report. Report's representativeness warning (likely overestimate) omitted from registry caveats.
- **hpd-housing-connect-furman#1** (value nearly 600,000): Period 'Calendar 2024' is not supported by the source; the estimate is undated. The 'roughly ten applications per unique applicant' ratio is a registry computation combining two sources with different (and one unknown) periods, not a figure in either source.
- **doe-3k-waitlist#0** (value more than 6,000 (roughly 15% of 3-K applicants)): line_name 'children without an offer' contradicts the source: 'every family at least got an offer'; the 6,000 were placed in programs they did not list.
- **parks-trees-sidewalks#0** (value see JSON): Standard 'No target time frame exists' omits the audit's 30-day inspection SLA, which the audit says was missed by 71 days on average. Two figures (101 and 419 days) with different denominators; registry end_event mixes repaired, waitlisted and refused cases while the 419-day mean covers repaired sidewalks only. Audit period (fiscal 2017-18) not verifiable from the local copy.
- **nycha-maintenance-work-orders#0** (value 3.94): end_event 'Work order closed' vs source 'date the work is completed'; clock starts at 'date the work order is created' (registry silent).
- **nycha-skilled-trades-work-orders#0** (value 117.06): 'electrician' and 'outside vendor' in what_for are not in the description text (vendor is in the title only). end_event 'closed' vs source 'work is completed'.
- **nycha-elevator-outages#0** (value 6.41): Unit: value appears to be hours:minutes encoded as H.MM (no fractional part >= .60 in 258 values); registry reads it as decimal hours. 6.41 -> 6h41m = 6.68 h.
- **nycha-heat-outages#0** (value 7.12): Unit: hours:minutes encoded as H.MM, registry reads as decimal hours. 7.12 -> 7h12m = 7.20 h. Registry does not carry the source's definition of an outage ('a line of apartments, stair hall, building(s), or development').
- **hpd-section8-lease-up#0** (value 137): center 'median' vs description 'The average time'; contradiction not recorded (it was recorded for hpd-section8-voucher-issuance). Source states the span 'Includes both HPD processing times, as well as search times for the voucher holder'; registry caveats are empty.
- **hpd-lottery-project-approvals#0** (value 210): 'All approvals ... completed' vs source 'completion of 95% of applicant approvals'. Clock starts at 'certificate of occupancy issuance'; registry silent.
- **hpd-homeless-setaside-leaseup#0** (value 235): end_event 'Lease signed' vs source 'shelter exit date'. Clock starts at temporary certificate of occupancy; registry silent.
- **hpd-homeless-voluntary-leaseup#0** (value 162): end_event 'Lease signed' vs source 'shelter exit date'. Clock starts at TCO; registry silent.
- **hpd-inspection-heat#0** (value 1.3): end_event 'First inspection' vs source 'first physical inspection attempt'. Population restriction 'original (non-duplicate) problem ... received within the period' not in registry.
- **hpd-inspection-nonemergency#0** (value 5.3): end_event 'First inspection' vs source 'first physical inspection attempt'. Exclusion 'not including lead-based paint hazard problems' not in registry.
- **hra-idnyc-timeliness#0** (value 98.9): unit 'applications' vs source denominator 'mailed IDNYC cards'.
- **hra-phone-wait#0** (value 96.38): Line is described as a phone wait ('HRA phone wait (Infoline)', 'Call answered'); source describes an in-person wait 'from the time a customer meets with a greeter or information desk representative until he or she is met by a customer service representative'. Unit: minutes:seconds encoded as M.SS; registry reads as decimal minutes. 96.38 -> 96m38s = 96.63 min.
- **dhs-los-single-adults#0** (value 368): Registry points to the families definition; the source definition for single adults is different (exclusions, clock start, treatment of gaps). Wording 'an adult has spent ... during the reporting period' suggests a wait-so-far over current residents rather than a completed stay.
- **hh-third-next-adult#0** (value 9.0): center 'mean' not stated in source. unit 'persons' -- source counts days to an appointment slot, not people.
- **hh-third-next-pediatric#0** (value 11.0): center 'mean' not stated in source. unit 'persons' not supported.
- **dob-first-plan-review#0** (value 5.4): Unit: source is 'business days'; registry says 'days'. Clock starts at status 'application processed - completed', not filing; stop is 'either disapproved status or approved status during first review'.
- **dob-first-plan-review-nb#0** (value 9.9): Unit: source is 'business days'; registry says 'days'. Clock start 'application processed - completed' not stated.
- **dob-inspection-construction#0** (value 5.1): Unit: source 'business days'; registry 'days'. end_event 'Inspection performed' vs source 'the first available date that an inspector can visit a job site' (an appointment-availability measure).
- **dob-inspection-electrical#0** (value 10.2): Unit: source 'business days'; registry 'days'. end_event 'Inspection performed' vs source 'first available date that an inspector can visit'.
- **dob-inspection-plumbing#0** (value 5.8): Unit: source 'business days'; registry 'days'. end_event 'Inspection performed' vs source 'first available date that an inspector can visit'.
- **dcwp-license-processing#0** (value 2): Exclusions not in registry: licenses needing outside-agency approval, special inspections, mandatory waiting periods or extensive legal review are excluded; days pending on the applicant are excluded. Population includes renewal applications; registry what_for 'A business or worker license' does not say so.
- **dcwp-license-within-30#0** (value 99): Exclusions (outside-agency approval, special inspections, mandatory waiting periods, extensive legal review) not in registry. 'agency standard' is the registry's attribution; source states a 30-calendar-day threshold only. Includes renewals.
- **dohmh-birth-certificates#0** (value 2.8): Clock starts at 'receipt of necessary documentation', not at the request. Exclusion 'Outlier, voided and canceled orders are excluded' not in registry. Stop 'response/issuance' is broader than 'Certificate issued'.
- **dohmh-death-certificates#0** (value 1.5): Clock starts at 'receipt of necessary documentation'. Outliers, voided and canceled orders excluded; funeral director orders included; registry silent.
- **bic-waste-hauling-approval#0** (value 234): Exclusion 'does not include applications that undergo long-term investigations and are subsequently approved' not in registry. Stop is 'approval by the Legal Unit'; population includes registrations as well as licenses.
- **bic-waste-hauling-pending#0** (value 63): Exclusion 'does not include applications slated for denial or under long-term investigation' not in registry. Counts 'license and registration applications'; registry what_for 'A trade waste license'.
- **lpc-minor-work-permits#0** (value 91): Clock starts at 'the application being completed', not receipt; registry silent. 'agency standard' is the registry's attribution.

## Problems on lines that otherwise match

- **nycha-section8-waitlist#0**: Registry caveat cites 'the Mayor's Management Report count ... shows 203,000 for fiscal 2025'; rbed-zzin fiscal 2025 monthly rows are [('2024-07', '203'), ('2024-08', '205'), ('2024-09', '204'), ('2024-10', '204'), ('2024-11', '204'), ('2024-12', '203'), ('2025-01', '203'), ('2025-02', '202'), ('2025-03', '200'), ('2025-04', '198'), ('2025-05', '197'), ('2025-06', '197')] (thousands). 203 is the July 2024 and Dec. 2024-Jan. 2025 value; fiscal year-end (June 2025) is 197, peak 205 in Aug. 2024. The month should be stated.
- **nycha-section8-waitlist#1**: Registry caveat about duplicates/deduplication is not in the source text.
- **dcwp-general-vendor-waitlist#0**: Registry caveat attributes the 853-cap figure to 'public comment quoted on the NYC Rules page, not an agency figure'; the Gothamist source states it directly ('capped at 853 since 1979').
- **dob-filing-to-approval-computed#0**: A single median (about 7 days) blends two populations with medians of about 1.6 and 27 days; the registry description does not flag the professional-certification/plan-examination split.
- **hpd-problem-close-computed#0**: Unit: the dataset row is a problem, not a request or complaint; one complaint_id can carry several problem_ids. Registry unit 'requests' should say problems.
- **dcas-eligible-lists#0**: Registry end_event says lists expire in 'one to four years'; stats.json supports the four-year maximum (window_median_days 1461) but not the one-year minimum.
- **nycha-section8-waitlist-mmr#0**: Registry caveat says 'the Mayor's Management Report count ... shows 203,000 for fiscal 2025'. The dataset's fiscal 2025 monthly rows run [('2024-07', '203'), ('2024-08', '205'), ('2024-09', '204'), ('2024-10', '204'), ('2024-11', '204'), ('2024-12', '203'), ('2025-01', '203'), ('2025-02', '202'), ('2025-03', '200'), ('2025-04', '198'), ('2025-05', '197'), ('2025-06', '197')] (thousands): 203 is the July 2024, Dec. 2024 and Jan. 2025 value; the fiscal year-end (June 2025) value is 197 and the peak is 205 (Aug. 2024). A single 'fiscal 2025' figure should say which month it is.
- **nycha-nonemergency-within-15#0**: Source does not say 15 days is 'NYCHA's own standard'; it is a reporting threshold in the description.
- **nycha-nonemergency-within-60#0**: Source does not say 60 days is 'NYCHA's own standard'.
- **hpd-close-emergency#0**: Registry caveat 'found no violation' is not in the source text; source lists 'inspection, callback to tenant, or repeated attempts for access'. Scope 'in a privately-owned building' and 'unique' problems not in registry.
- **hpd-close-nonemergency#0**: 'found no violation' not in source text. Scope 'in a privately-owned building' not in registry.
- **hra-hasa-timeliness#0**: Source cohort is 'applications submitted in the reporting month'; registry period label treats the value as fiscal-year-to-date (the dataset field is acceptedvalueytd, so both readings are defensible but the registry does not note the monthly-cohort wording).
- **dof-scrie-initial#0**: Source stop includes 'deemed incomplete' (no decision); registry end_event 'Application processed' does not mention it.
- **dof-drie-initial#0**: Source stop includes 'deemed incomplete' (no decision); registry end_event 'Application processed' does not mention it.
- **dof-sche-initial#0**: Source stop includes 'deemed incomplete' (no decision); registry end_event 'Application processed' does not mention it.
- **dof-dhe-initial#0**: Source stop includes 'deemed incomplete' (no decision); registry end_event 'Application processed' does not mention it.
- **dof-parking-hearing-inperson#0**: Span includes the hearing itself ('to the completion of the hearing'); registry end_event 'Hearing held' is close but does not say the hearing time is included. Non-commercial drivers only.
- **doris-vital-records#0**: end_event 'Record sent' -- source counts sending 'either a certified copy of the record or a "not found" statement'.
- **dot-permit-processing#0**: Population is approved permits only ('to issue an approved permit'); registry 'Permit processed' does not say so.
- **oath-special-ed-hearings#0**: what_for 'A decision' -- source closures include 'resolution, withdrawal, dismissal, or final decision'.

## Cross-cutting

- Three indicators are labelled hours:minutes or minutes:seconds (NYCHA elevator outages, NYCHA heat outages, HRA customer service wait). Across every published value of each, the fractional part never exceeds .59, so the numbers are H.MM / M.SS, not decimals. The registry reads them as decimal hours and minutes.
- The HRA 'phone wait' line is not a phone wait. The dataset's definition describes the in-person wait from greeter to customer service representative.
- Five DOB indicators are in business days per their definitions; the registry carries 'days' on the four plan-review and inspection lines (it gets business days right only on filing-to-approval). The three DOB inspection lines stop at the first available appointment date, not at an inspection performed.
- Registry caveats are empty on several lines whose definitions carry material exclusions (DCWP licensing, BIC approval and pending counts, DOHMH certificates, HPD non-emergency inspections).
- The registry caveat that the Mayor's Management Report shows 203,000 Section 8 waitlist families for fiscal 2025 matches the July 2024 and Dec. 2024-Jan. 2025 monthly rows only; the fiscal year-end (June 2025) row is 197,000 and the peak was 205,000 (Aug. 2024). Fiscal 2025 monthly values: 2024-07: 203, 2024-08: 205, 2024-09: 204, 2024-10: 204, 2024-11: 204, 2024-12: 203, 2025-01: 203, 2025-02: 202, 2025-03: 200, 2025-04: 198, 2025-05: 197, 2025-06: 197 (thousands).

## Recomputes

- DOB w9ak-ipjd, approvals Sept. 1, 2025 to Aug. 31, 2026: n=141118, median 6.87 days, p90 89.49 days. Professional Certification median 1.62, Standard Plan Examination median 27.14.
- HPD ygpa-z7cr, problems closed March 1 to Aug. 31, 2026, non-duplicate: n=377002, median 8.27 days, p90 67.19 days. By type: EMERGENCY median 6.11 (n=177038); NON EMERGENCY median 12.68 (n=182842); IMMEDIATE EMERGENCY median 2.24 (n=17122).
- Civil service vx8i-nprf: 403,777 rows live vs 403,200 in stats.json (July 13, 2026); 855 vs 850 exams; 432 vs 428 titles.
