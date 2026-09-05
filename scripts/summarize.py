"""Human-readable registry table with year-over-year comparison where the series allows. Facts only. Writes data/registry_summary.md."""
import json, datetime as dt
R=json.load(open('data/registry.json'))
def fmt(v,u):
    if v is None: return "n/a"
    if abs(v)>=1000 and float(v).is_integer(): return f"{int(v):,} {u}"
    return f"{v:g} {u}"
out=["# Registry summary","",f"Built {R['built']}. {len(R['lines'])} lines. Grades per METHODOLOGY.md. Every figure's source and definition text are in data/registry.json.",""]
for tier,title in ((1,"Tier 1: mayoral agencies"),(2,"Tier 2: city-controlled entities"),(3,"Tier 3: state lines, shown apart")):
    out+=[f"## {title}","","| line | agency | measure | latest | period | center | spread published | grade |","|---|---|---|---|---|---|---|---|"]
    for l in sorted([l for l in R['lines'] if l['tier']==tier],key=lambda l:(l['agency'],l['name'])):
        for f in l['figures']:
            spread = "yes" if f.get('spread') else "no"
            yoy=""
            s=f.get('series')
            if s and f['value'] is not None:
                last=s[-1]; prior=[r for r in s if r['date']==(dt.date.fromisoformat(last['date']).replace(year=dt.date.fromisoformat(last['date']).year-1)).isoformat() and r['value'] is not None]
                if prior: yoy=f" (same month prior year: {prior[0]['value']:g})"
            out.append(f"| {l['name']} | {l['agency']} | {f['type']} | {fmt(f['value'],f['unit_of_value'])}{yoy} | {f['period_label'].split(' (')[0]} | {f.get('center')} | {spread} | {f['grade']} |")
    out.append("")
open('data/registry_summary.md','w').write('\n'.join(out)); print(len(out),"lines written")
