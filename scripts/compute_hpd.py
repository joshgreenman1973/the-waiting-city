"""Computed (grade A-c) distribution: HPD housing maintenance complaint problems, days from received_date
to problem_status_date for problems closed in the trailing 6 months. Source: ygpa-z7cr. Fails loudly on empty fetch."""
import json, sys, urllib.request, urllib.parse, datetime as dt, statistics
END=dt.date(2026,9,1); START=dt.date(2026,3,1)
BASE="https://data.cityofnewyork.us/resource/ygpa-z7cr.json"
rows=[]; off=0
while True:
    q={"$select":"problem_id,received_date,problem_status_date,borough,type,major_category,problem_status,problem_duplicate_flag",
       "$where":f"problem_status='CLOSE' and problem_status_date >= '{START}T00:00:00' and problem_status_date < '{END}T00:00:00'",
       "$limit":100000,"$offset":off,"$order":"problem_id"}
    d=json.load(urllib.request.urlopen(BASE+"?"+urllib.parse.urlencode(q),timeout=300))
    rows+=d; off+=100000; print("fetched",len(rows),file=sys.stderr)
    if len(d)<100000: break
if not rows: print("EMPTY FETCH"); sys.exit(1)
rows=[r for r in rows if r.get('problem_duplicate_flag','N')!='Y']
def days(r):
    a=dt.datetime.fromisoformat(r['received_date'][:19]); b=dt.datetime.fromisoformat(r['problem_status_date'][:19]); return (b-a).total_seconds()/86400
vals=[(days(r),r) for r in rows if r.get('received_date') and r.get('problem_status_date')]
vals=[(d,r) for d,r in vals if d>=0]
def pct(xs,p):
    xs=sorted(xs); k=(len(xs)-1)*p; f=int(k); c=min(f+1,len(xs)-1); return round(xs[f]+(xs[c]-xs[f])*(k-f),1)
def summ(xs):
    return {"n":len(xs),"mean":round(statistics.mean(xs),1),"median":pct(xs,.5),"p75":pct(xs,.75),"p90":pct(xs,.9),"p99":pct(xs,.99),"max":round(max(xs),1),
            "share_over_12":round(sum(x>12 for x in xs)/len(xs),3),"share_over_21":round(sum(x>21 for x in xs)/len(xs),3),"share_over_90":round(sum(x>90 for x in xs)/len(xs),3)}
out={"dataset":"ygpa-z7cr","measure":"days from received_date to problem_status_date, problems closed March 1 to Aug. 31, 2026, duplicates excluded","query_template":BASE+"?"+urllib.parse.urlencode({"$where":q["$where"],"$select":q["$select"]}),
     "computed":"2026-09-05","all":summ([d for d,_ in vals]),"by_type":{},"by_borough":{},"by_type_borough":{},"by_major_category":{}}
def grp(field):
    g={}
    for d,r in vals: g.setdefault(r.get(field) or "unknown",[]).append(d)
    return {k:summ(x) for k,x in g.items() if len(x)>=300}
out["by_type"]=grp("type"); out["by_borough"]=grp("borough"); out["by_major_category"]=grp("major_category")
g={}
for d,r in vals: g.setdefault(f"{r.get('type')}|{r.get('borough')}",[]).append(d)
out["by_type_borough"]={k:summ(x) for k,x in g.items() if len(x)>=300}
json.dump(out,open("data/computed_hpd_problem_close.json","w"),indent=1)
print(len(rows),"non-duplicate closed problems;",len(vals),"with durations"); print("ALL",out["all"])
for k,s in sorted(out["by_type"].items()): print(k,s["n"],"median",s["median"],"p90",s["p90"],">21d",s["share_over_21"])
for k,s in sorted(out["by_type_borough"].items()): print(k,s["n"],"median",s["median"],"p90",s["p90"])
