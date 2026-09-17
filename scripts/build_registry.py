"""Merge hand-sourced lines (data/queues_manual.json) with Mayor's Management Report indicator lines
(data/mmr_series.json, mapped in data/mmr_lines.json) into data/registry.json.
Every MMR figure carries the dataset's own definition text verbatim and the SoQL query used."""
import json, re, datetime as dt
manual=json.load(open('data/queues_manual.json'))
S=json.load(open('data/mmr_series.json'))
M=json.load(open('data/mmr_lines.json'))   # indicator key -> line metadata (id,name,what_for,end_event,unit,type,center,duration_kind,standard,tier)
try: PDF=json.load(open('data/mmr_fy2026_pdf.json'))          # fiscal 2026 actuals read from the printed report
except FileNotFoundError: PDF={"source":{},"indicators":{}}
def fy_label(fy, valuedate, freq, reporting_period):
    d=dt.date.fromisoformat(valuedate[:10]); fy=int(fy)
    if freq=='Monthly':
        # MMR monthly values are fiscal-year-to-date through the value month
        import calendar
        last=calendar.monthrange(d.year,d.month)[1]; end=d.replace(day=last)
        return f"Fiscal {fy} to date, July 1, {fy-1} through {end.strftime('%b. %-d, %Y')} (dataset field acceptedvalueytd: fiscal-year-to-date value)", f"{fy-1}-07-01", end.isoformat()
    if freq=='Quarterly':
        return f"Fiscal {fy} to date; dataset valuedate {d.strftime('%b. %-d, %Y')} (quarterly rows fall at fiscal quarter ends; the dataset does not state which quarter a row closes)", f"{fy-1}-07-01", d.isoformat()
    if freq in ('Annually','PMMR/MMR'):
        if d.month==10: return f"First four months of fiscal {fy}, July 1 to Oct. 31, {fy-1}", f"{fy-1}-07-01", f"{fy-1}-10-31"
        return f"Fiscal {fy}, July 1, {fy-1} to June 30, {fy}", f"{fy-1}-07-01", f"{fy}-06-30"
    return f"Fiscal {fy}", f"{fy-1}-07-01", f"{fy}-06-30"
PDF_FY=2026
def pdf_caveats(pdfrow,use_pdf):
    """What a reader needs to know when a figure comes from the printed report rather than the dataset."""
    if not pdfrow: return []
    out=[]
    if use_pdf:
        out.append(f"The fiscal {PDF_FY} figure is read from the printed Mayor's Management Report "
                   f"(page {pdfrow['printed_page']}, released Sept. 17, 2026); NYC Open Data's indicator file had not "
                   f"been refreshed past the preliminary report when this was built. The printed row's earlier columns "
                   f"match the dataset's own values for every one of fiscal 2022 to 2025 the dataset publishes "
                   f"({pdfrow['history_years_matched']} of the four), which is how the row was identified. The "
                   f"definition text below is the dataset's, from the last year it published one.")
    elif pdfrow.get('fy2026_value') is None:
        out.append(f"The fiscal {PDF_FY} report also prints \u201c{pdfrow['fy2026_printed']}\u201d for this indicator, so "
                   f"the figure here is the last year the city reported one.")
    return out
def to_num(v):
    try: return float(v)
    except: return None
lines=list(manual)
for key,meta in M.items():
    s=S[key]; rows=[r for r in s['rows'] if r.get('acceptedvalueytd') not in (None,'NA','','*')]
    if not rows: raise SystemExit("no values for "+key)
    last=rows[-1]
    # The printed Mayor's Management Report carries a full fiscal year before NYC Open Data's indicator
    # file is refreshed. Use the printed figure until the dataset itself reaches the end of that year.
    pdfrow=PDF['indicators'].get(key)
    od_full_year = last['fiscalyear']==str(PDF_FY) and last['valuedate'][5:7]=='06'
    use_pdf = bool(pdfrow) and pdfrow.get('fy2026_value') is not None and not od_full_year
    label,ps,pe=fy_label(last['fiscalyear'],last['valuedate'],last.get('frequency',''),last.get('reporting_period',''))
    val=to_num(last['acceptedvalueytd']); val_month=to_num(last.get('acceptedvalue'))
    point_in_time = meta['type']=='stock' or str(meta.get('duration_kind','')).startswith('waiting_so_far')
    if point_in_time and val_month is not None and last.get('frequency')=='Monthly':
        val_fytd=val; val=val_month
        label=f"As of {dt.date.fromisoformat(last['valuedate'][:10]).strftime('%B %Y')} (dataset field acceptedvalue, the month's value; the fiscal-year-to-date average, acceptedvalueytd, is {val_fytd:g})"
    else: val_fytd=None
    printed=None
    pdf_note=None
    if use_pdf:
        val=to_num(pdfrow['fy2026_value']); val_fytd=None
        printed_note=(f"the figure printed in the Mayor's Management Report; NYC Open Data's indicator file "
                      f"still ended at the preliminary report when this was built")
        if point_in_time and pdfrow.get('printed_equals_june_month_value'):
            label=f"As of June {PDF_FY} ({printed_note})"
        else:
            label=f"Fiscal {PDF_FY}, July 1, {PDF_FY-1} to June 30, {PDF_FY} ({printed_note})"
        ps,pe=f"{PDF_FY-1}-07-01",f"{PDF_FY}-06-30"
        pdf_note=pdfrow
    def decode(v):
        if v is None: return None
        whole=int(v); frac=round((v-whole)*100)
        return round(whole+frac/60,2)
    is_hm = last.get('measurement_type')=='TimeSpan' and ('hours:minutes' in s['indicator'] or 'minutes:seconds' in s['indicator'])
    if is_hm:
        whole=int(val); frac=round((val-whole)*100); printed=f"{whole}:{frac:02d}"; val=decode(val)
        if use_pdf: printed=pdfrow['fy2026_printed']
    mult=to_num(last.get('multiplication_factor') or 1) or 1
    series=[{"fy":r['fiscalyear'],"date":r['valuedate'][:10],"value":(decode(to_num(r['acceptedvalueytd'])) if is_hm else to_num(r['acceptedvalueytd'])),"value_month":to_num(r.get('acceptedvalue')),"printed":r['acceptedvalueytd'],"description":r.get('description')} for r in rows]
    if use_pdf:
        pv=to_num(pdfrow['fy2026_value'])
        series.append({"fy":str(PDF_FY),"date":f"{PDF_FY}-06-30","value":(decode(pv) if is_hm else pv),
                       "value_month":(pv if pdfrow.get('printed_equals_june_month_value') else None),
                       "printed":pdfrow['fy2026_printed'],"description":last.get('description'),
                       "from_printed_report":True})
    # definition changes across years
    defs=sorted({(r['fiscalyear'],r.get('description','')) for r in rows})
    changes=[]; prev=None
    for fy,d in defs:
        if d!=prev: changes.append({"from_fy":fy,"description":d}); prev=d
    unit_of_value = "percent" if last.get('measurement_type')=='Percentage' else meta.get('unit_of_value','')
    fig={"type":meta['type'],"value":val*meta.get('scale',1) if val is not None else None,"unit_of_value":unit_of_value,"value_as_printed":printed,"value_fytd":val_fytd,
         "center":meta.get('center','n/a'),"spread":None,"spread_note":meta.get('spread_note',"Agency publishes a single figure; no distribution."),
         "duration_kind":meta.get('duration_kind','n/a'),"standard":meta.get('standard'),
         "period_start":ps,"period_end":pe,"period_label":label,
         "source":({"url":f"{PDF['source']['url']}#page={pdfrow['pdf_page']}","title":f"Mayor's Management Report, fiscal {PDF_FY}, page {pdfrow['printed_page']}","publisher":"Mayor's Office of Operations, City of New York","date":PDF['source'].get('released'),"quote":pdfrow['row_line'],"retrieved":PDF['source'].get('retrieved')} if use_pdf else
                    {"url":"https://data.cityofnewyork.us/City-Government/Mayor-s-Management-Report-Agency-Performance-Indic/rbed-zzin","title":"Mayor's Management Report - Agency Performance Indicators","publisher":"Mayor's Office of Operations via NYC Open Data","date":last['valuedate'][:10],"quote":f"{s['indicator']}: {last['acceptedvalueytd']}","retrieved":"2026-09-05"}),
         "definition_quote":last.get('description'),"definition_changes":changes,
         "grade":meta.get("grade_override","A"),"grade_reason":("Source title and definition text disagree; see caveats. " if meta.get("grade_override") else "")+"Structured agency data with a printed indicator definition, refreshed on the Mayor's Management Report schedule; re-queryable.",
         "refresh":{"method":"soql","query_or_url":s['query']},
         "caveats":meta.get('caveats',[])+pdf_caveats(pdfrow,use_pdf),"series":series,"desired_direction":last.get('desireddirection'),"frequency":last.get('frequency'),"critical":last.get('critical')}
    lines.append({"id":meta['id'],"name":meta['name'],"agency":s['agency'],"tier":meta.get('tier',1),"what_for":meta['what_for'],"end_event":meta['end_event'],
                  "unit":meta['unit'],"list_status":meta.get('list_status','rolling'),"figures":[fig],"related_lines":meta.get('related_lines',[]),
                  "duplicates_with":meta.get('duplicates_with',[]),"raise_grade":meta.get('raise_grade',"Record-level data to compute the distribution (see METHODOLOGY.md, computed grade).")})
json.dump({"built":dt.date.today().isoformat(),"methodology":"METHODOLOGY.md","lines":lines},open('data/registry.json','w'),indent=1)
print(len(lines),"lines,",sum(len(l['figures']) for l in lines),"figures")
