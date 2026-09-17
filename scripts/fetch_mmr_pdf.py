"""Read Fiscal 2026 actuals for the selected Mayor's Management Report indicators out of the printed
report (nyc.gov PDF), because NYC Open Data's indicator file (rbed-zzin) still stops at the preliminary
report for fiscal 2026.

Every indicator is located by matching the printed table's fiscal 2022-2025 columns against the same
indicator's Open Data series, so a row is only accepted when its own history agrees with the dataset.
Fails loudly if any selected indicator cannot be located, if its history disagrees, or if more than one
row survives.

Writes data/mmr_fy2026_pdf.json and sources/mmr2026.txt (the extracted text used for fact-checking).
"""
import json, re, sys, hashlib, urllib.request, difflib, datetime as dt

PDF_URL = "https://www.nyc.gov/assets/operations/downloads/pdf/mmr2026/2026_mmr.pdf"
PDF_LOCAL = "sources/mmr2026.pdf"
TXT_LOCAL = "sources/mmr2026.txt"
OUT = "data/mmr_fy2026_pdf.json"
FYS = ["2022", "2023", "2024", "2025"]

# Open Data agency code -> the chapter header printed in the report
CHAPTER = {
    "NYCHA": "NEW YORK CITY HOUSING AUTHORITY",
    "HPD": "HOUSING PRESERVATION AND DEVELOPMENT",
    "HRA": "HUMAN RESOURCES ADMINISTRATION",
    "DHS": "DEPARTMENT OF HOMELESS SERVICES",
    "ACS": "ADMINISTRATION FOR CHILDREN’S SERVICES",
    "NYCHH": "NYC HEALTH + HOSPITALS",
    "DCAS": "DEPARTMENT OF CITYWIDE ADMINISTRATIVE SERVICES",
    "DOF": "DEPARTMENT OF FINANCE",
    "DOB": "DEPARTMENT OF BUILDINGS",
    "DCP": "DEPARTMENT OF CITY PLANNING",
    "DCWP": "DEPARTMENT OF CONSUMER AND WORKER PROTECTION",
    "DOHMH": "DEPARTMENT OF HEALTH AND MENTAL HYGIENE",
    "DORIS": "DEPARTMENT OF RECORDS & INFORMATION SERVICES",
    "DOT": "DEPARTMENT OF TRANSPORTATION",
    "BIC": "BUSINESS INTEGRITY COMMISSION",
    "CCHR": "CITY COMMISSION ON HUMAN RIGHTS",
    "OATH": "OFFICE OF ADMINISTRATIVE TRIALS AND HEARINGS",
    "LPC": "LANDMARKS PRESERVATION COMMISSION",
    "DFTA": "DEPARTMENT FOR THE AGING",
}


def fetch_pdf():
    req = urllib.request.Request(PDF_URL, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            blob = r.read()
            last_mod = r.headers.get("Last-Modified", "")
    except Exception as e:
        print("DOWNLOAD FAILED", PDF_URL, e)
        sys.exit(1)
    if len(blob) < 1_000_000 or blob[:5] != b"%PDF-":
        print("NOT A PDF or too small:", len(blob), "bytes")
        sys.exit(1)
    open(PDF_LOCAL, "wb").write(blob)
    return hashlib.sha256(blob).hexdigest(), last_mod, len(blob)


def extract_text():
    import pypdf
    reader = pypdf.PdfReader(PDF_LOCAL)
    parts = []
    for i, page in enumerate(reader.pages):
        parts.append(f"\n<<<PAGE {i+1}>>>\n" + (page.extract_text() or ""))
    text = "".join(parts)
    open(TXT_LOCAL, "w").write(text)
    return text, len(reader.pages)


def page_chapters(pages):
    """Chapter header per PDF page. Even pages carry only the report's own name, so unlabeled pages
    inherit the chapter before and after them (chapters are contiguous)."""
    hdr = {}
    for n, t in pages.items():
        for a, b in re.findall(r"^(?:Page \d+\s+\|\s+(.+)|(.+?)\s+\|\s+Page \d+)\s*$", t, re.M):
            s = (a or b).strip()
            if s and "MAYOR" not in s.upper():
                hdr[n] = s
                break
    labeled = sorted(hdr)
    out = {}
    for n in sorted(pages):
        if n in hdr:
            out[n] = {hdr[n]}
        else:
            before = [p for p in labeled if p < n]
            after = [p for p in labeled if p > n]
            out[n] = set()
            if before:
                out[n].add(hdr[before[-1]])
            if after:
                out[n].add(hdr[after[0]])
    return out


VAL = re.compile(r"^(?:NA|\*|†|‡|\$?-?[\d,]+(?:\.\d+)?%?|\d+:\d{2}(?::\d{2})?|\(?\d+(?:\.\d+)?\)?%?)$")
TREND = re.compile(r"^(?:Up|Down|Neutral|NA|\*|ñ|ò|Higher|Lower)$")


def parse_rows(pages, chapters):
    """Indicator rows out of the performance tables. Columns run
    FY22 FY23 FY24 FY25 FY26 actual | FY26 target | FY27 target | 5-year trend | desired direction,
    so the five actuals are the five tokens before the last four."""
    rows = []
    for pg in sorted(pages):
        chap = chapters.get(pg)
        if not chap:
            continue
        wrapped = []
        for raw in pages[pg].split("\n"):
            s = raw.strip()
            if not s:
                wrapped = []
                continue
            if s.startswith("Critical Indicator"):
                wrapped = []
                continue
            toks = s.split()
            i = len(toks)
            while i > 0 and (VAL.match(toks[i - 1]) or TREND.match(toks[i - 1])):
                i -= 1
            tail = toks[i:]
            label = " ".join(toks[:i]).strip()
            if len(tail) >= 6 and i > 0:
                full = re.sub(r"\s+", " ", (" ".join(wrapped) + " " + label)).strip()
                actuals = tail[-9:-4] if len(tail) >= 9 else tail[:5]
                rows.append({"page": pg, "chapters": sorted(chap), "label": full,
                             "actuals": actuals, "tail": tail, "line": s})
                wrapped = []
            else:
                if len(s) < 200 and not s.startswith("Performance Indicators"):
                    wrapped.append(s)
                wrapped = wrapped[-3:]
    return rows


def num(t):
    """A printed cell as a number. Times print as h:mm; the dataset stores those as h.mm, so match that."""
    if t in ("NA", "*", "", "†", "‡"):
        return None
    t = t.replace("$", "").replace(",", "").replace("%", "").strip("()")
    m = re.match(r"^(\d+):(\d{2})$", t)
    if m:
        return float(f"{m.group(1)}.{m.group(2)}")
    try:
        return float(t)
    except ValueError:
        return None


def close(a, b):
    return abs(a - b) <= max(0.006, abs(a) * 0.006)


def printed_page(pages, pg):
    m = re.search(r"Page (\d+)\s+\|", pages[pg]) or re.search(r"\|\s+Page (\d+)", pages[pg])
    return int(m.group(1)) if m else None


def main():
    series = json.load(open("data/mmr_series.json"))
    selected = [l.strip().split("|", 1) for l in open("data/mmr_selected.txt") if l.strip() and not l.startswith("#")]
    sha, last_mod, size = fetch_pdf()
    text, npages = extract_text()
    parts = re.split(r"\n<<<PAGE (\d+)>>>\n", text)
    pages = {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}
    chapters = page_chapters(pages)
    rows = parse_rows(pages, chapters)
    print(f"{npages} pages, {len(rows)} indicator rows parsed, pdf sha256 {sha[:12]}…")

    out = {}
    failures = []
    for agency, indicator in selected:
        agency, indicator = agency.strip(), indicator.strip()
        key = f"{agency}|{indicator}"
        if key not in series:
            failures.append(f"{key}: not in data/mmr_series.json")
            continue
        chap = CHAPTER[agency]
        # last Open Data value of each fiscal year, both fields
        od = {"acceptedvalueytd": {}, "acceptedvalue": {}}
        june = {}
        for r in series[key]["rows"]:
            for field in od:
                v = r.get(field)
                if v not in (None, "NA", "*"):
                    try:
                        od[field][r["fiscalyear"]] = float(v)
                    except ValueError:
                        pass
            if r["valuedate"][5:7] == "06":
                june[r["fiscalyear"]] = r
        hits = []
        for row in rows:
            if chap not in row["chapters"]:
                continue
            vals = [num(t) for t in row["actuals"]]
            if len(vals) < 5:
                continue
            for field in od:
                ok = tot = 0
                for i, fy in enumerate(FYS):
                    a, b = od[field].get(fy), vals[i]
                    if a is None or b is None:
                        continue
                    tot += 1
                    ok += 1 if close(a, b) else 0
                if tot >= 2 and ok == tot:
                    hits.append({"row": row, "field": field, "matched_years": tot})
        # one row can match on both fields; collapse to distinct rows
        distinct = {}
        for h in hits:
            distinct.setdefault((h["row"]["page"], tuple(h["row"]["tail"])), h)
        cands = list(distinct.values())
        if len(cands) > 1:
            def norm(x):
                return re.sub(r"[^a-z0-9]+", " ", x.lower()).strip()
            sim = lambda h: difflib.SequenceMatcher(None, norm(indicator), norm(h["row"]["label"])).ratio()
            cands.sort(key=sim, reverse=True)
            if not (sim(cands[0]) >= 0.75 and sim(cands[0]) - sim(cands[1]) >= 0.2):
                failures.append(f"{key}: {len(cands)} rows match the fiscal 2022-2025 history and none wins on name: "
                                + " // ".join(f'p{c["row"]["page"]} {c["row"]["label"][-60:]}' for c in cands[:4]))
                continue
            cands = cands[:1]
        if not cands:
            failures.append(f"{key}: no row in the {chap} chapter matches the fiscal 2022-2025 history")
            continue
        hit = cands[0]
        row = hit["row"]
        printed = row["actuals"][4]
        value = num(printed)
        # do the printed fiscal-year figures equal the June (year-end) month value, or the year-to-date field?
        june_match = None
        if all(fy in june for fy in FYS if od["acceptedvalue"].get(fy) is not None):
            checks = []
            for i, fy in enumerate(FYS):
                r = june.get(fy)
                pv = num(row["actuals"][i])
                if not r or pv is None or r.get("acceptedvalue") in (None, "NA", "*"):
                    continue
                checks.append(close(float(r["acceptedvalue"]), pv))
            june_match = all(checks) if checks else None
        out[key] = {
            "agency": agency,
            "indicator": indicator,
            "row_label": row["label"],
            "row_line": row["line"],
            "pdf_page": row["page"],
            "printed_page": printed_page(pages, row["page"]),
            "actuals_fy22_fy26": row["actuals"],
            "fy2026_printed": printed,
            "fy2026_value": value,
            "history_matched_field": hit["field"],
            "history_years_matched": hit["matched_years"],
            "printed_equals_june_month_value": june_match,
        }
        flag = "" if value is not None else "   (fiscal 2026 not reported)"
        print(f'{key[:64]:66} FY26 {printed:>9}  p{row["page"]}  {hit["matched_years"]} yrs matched{flag}')

    if failures:
        print("\nFAILED to place these indicators:")
        for f in failures:
            print("  -", f)
        sys.exit(1)

    json.dump({
        "source": {
            "title": "Mayor's Management Report, Fiscal 2026",
            "publisher": "Mayor's Office of Operations, City of New York",
            "url": PDF_URL,
            "released": "2026-09-17",
            "last_modified_header": last_mod,
            "bytes": size,
            "sha256": sha,
            "retrieved": dt.date.today().isoformat(),
            "local_text": TXT_LOCAL,
            "why": "NYC Open Data's Mayor's Management Report indicator file (rbed-zzin) had not been refreshed "
                   "past the preliminary fiscal 2026 report when this was built, so fiscal 2026 figures are read "
                   "from the printed report and each row is checked against the dataset's own fiscal 2022-2025 values.",
        },
        "indicators": out,
    }, open(OUT, "w"), indent=1)
    print(f"\n{len(out)} indicators written to {OUT}")


if __name__ == "__main__":
    main()
