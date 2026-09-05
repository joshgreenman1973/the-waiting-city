"""Computed (grade A-c) distribution: DOB NOW job filings, days from filing_date to approved_date,
for filings approved in the trailing 12 months. Source: w9ak-ipjd. Fails loudly on empty fetch."""
import json, sys, urllib.request, urllib.parse, datetime as dt, statistics
END=dt.date(2026,9,1); START=dt.date(2025,9,1)
BASE="https://data.cityofnewyork.us/resource/w9ak-ipjd.json"
rows=[]; off=0
while True:
    q={"$select":"job_filing_number,filing_date,approved_date,borough,job_type,filing_review_type",
       "$where":f"approved_date >= '{START}T00:00:00' and approved_date < '{END}T00:00:00' and filing_date IS NOT NULL",
       "$limit":50000,"$offset":off,"$order":"job_filing_number"}
    d=json.load(urllib.request.urlopen(BASE+"?"+urllib.parse.urlencode(q),timeout=300))
    rows+=d; off+=50000
    if len(d)<50000: break
if not rows: print("EMPTY FETCH"); sys.exit(1)
def days(r):
    f=dt.datetime.fromisoformat(r["filing_date"][:19]); a=dt.datetime.fromisoformat(r["approved_date"][:19]); return round((a-f).total_seconds()/86400,2)
vals=[(days(r),r) for r in rows]
vals=[(d,r) for d,r in vals if d>=0]
def pct(xs,p):
    xs=sorted(xs); k=(len(xs)-1)*p; f=int(k); c=min(f+1,len(xs)-1); return xs[f]+(xs[c]-xs[f])*(k-f)
def summ(xs):
    return {"n":len(xs),"mean":round(statistics.mean(xs),1),"median":pct(xs,.5),"p75":pct(xs,.75),"p90":pct(xs,.9),"p99":pct(xs,.99),"max":max(xs),
            "share_over_30":round(sum(x>30 for x in xs)/len(xs),3),"share_over_90":round(sum(x>90 for x in xs)/len(xs),3),"share_over_365":round(sum(x>365 for x in xs)/len(xs),3)}
out={"dataset":"w9ak-ipjd","measure":"days from filing_date to approved_date, filings approved Sept. 1, 2025 to Aug. 31, 2026","query_template":BASE+"?"+urllib.parse.urlencode({"$where":q["$where"],"$select":q["$select"]}),
     "computed":"2026-09-05","all":summ([d for d,_ in vals]),"by_borough":{},"by_job_type":{},"by_review_type":{}}
for key,field in (("by_borough","borough"),("by_job_type","job_type"),("by_review_type","filing_review_type")):
    groups={}
    for d,r in vals: groups.setdefault(r.get(field) or "unknown",[]).append(d)
    out[key]={g:summ(x) for g,x in groups.items() if len(x)>=200}
json.dump(out,open("data/computed_dob_filing_to_approval.json","w"),indent=1)
print(len(rows),"rows;",len(vals),"with non-negative durations"); print("ALL",out["all"])
for g,s in sorted(out["by_borough"].items()): print(g,s["n"],"median",s["median"],"p90",s["p90"],">90d",s["share_over_90"])
for g,s in sorted(out["by_job_type"].items()): print(g,s["n"],"median",s["median"],"p90",s["p90"],">90d",s["share_over_90"])
for g,s in sorted(out["by_review_type"].items()): print(g,s["n"],"median",s["median"],"p90",s["p90"])
