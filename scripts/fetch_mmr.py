"""Fetch full fiscal-year series for selected Mayor's Management Report indicators (rbed-zzin).
Fails loudly if any selected indicator returns no rows."""
import json, sys, urllib.request, urllib.parse
BASE="https://data.cityofnewyork.us/resource/rbed-zzin.json"
SELECT=[l.strip().split("|",1) for l in open("data/mmr_selected.txt") if l.strip() and not l.startswith("#")]
out={}
for agency,ind in SELECT:
    agency=agency.strip(); ind=ind.strip()
    q={"$where":f"agency='{agency}' and indicator='{ind.replace(chr(39),chr(39)*2)}'",
       "$select":"fiscalyear,valuedate,acceptedvalueytd,acceptedvalue,description,measurement_type,desireddirection,frequency,reporting_period,critical,retired,source,lagtime,additive",
       "$order":"fiscalyear,valuedate","$limit":2000}
    url=BASE+"?"+urllib.parse.urlencode(q)
    try: rows=json.load(urllib.request.urlopen(url,timeout=120))
    except Exception as e:
        print("QUERY FAILED",agency,ind,e); sys.exit(1)
    if not rows:
        print("NO ROWS for",agency,"|",ind); sys.exit(1)
    out[f"{agency}|{ind}"]={"agency":agency,"indicator":ind,"query":url,"rows":rows}
    print(f"{agency:6} {len(rows):4} rows  {ind[:90]}")
json.dump(out,open("data/mmr_series.json","w"),indent=1)
print(len(out),"indicators saved")
