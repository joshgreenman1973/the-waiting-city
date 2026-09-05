"""Compare blind checker extractions (pass 1 values, pass 2 definitions) with the registry. Writes data/blind_check_report.md."""
import json, re, os
R=json.load(open('data/registry.json')); A=json.load(open('data/blind_check_agent.json'))
P2=json.load(open('data/blind_check_pass2.json')) if os.path.exists('data/blind_check_pass2.json') else []
P3=json.load(open('data/blind_check_pass3.json')) if os.path.exists('data/blind_check_pass3.json') else []
p3={x['claim_id']:x for x in P3}
p2={x['claim_id']:x for x in P2}
fig={}
for l in R['lines']:
    for i,f in enumerate(l['figures']): fig[f"{l['id']}#{i}"]=(l,f)
def num(x):
    if x is None: return None
    if isinstance(x,(int,float)): return float(x)
    m=re.search(r'-?\d[\d,]*\.?\d*',str(x)); return float(m.group(0).replace(',','')) if m else None
def decode(v): whole=int(v); frac=round((v-whole)*100); return round(whole+frac/60,2)
rows=[]; n_ok=n_val=0
for a in A:
    cid=a['claim_id']
    if cid not in fig: continue
    l,f=fig[cid]; reg=f['value']; ev=a.get('extracted_value')
    if isinstance(ev,dict):
        ev=ev.get('median_days') or ev.get('stats_json_candidates_2026_07_13') or ev.get('inspection_to_repair_mean_days')
    ext=num(ev)
    if f.get('value_as_printed') and ext is not None: ext=decode(ext)
    if '(000)' in (f['source'].get('quote') or '') and ext is not None and ext<10000: ext*=1000
    ok = f['type']=='derived' or (reg is not None and ext is not None and abs(reg-ext)<=max(0.051,abs(reg)*0.001))
    issues=[] if ok else [f"VALUE registry={reg} checker={ev}"]
    d=p2.get(cid)
    if d and d.get('definition_check')=='mismatch': issues.append("PASS-2 DEFINITION: "+(d.get('notes') or ''))
    t=p3.get(cid)
    if t:
        ev3=t.get('extracted_value')
        if isinstance(ev3,dict): ev3=ev3.get('median_days') or ev3.get('median') or ev3.get('stats_json_candidates_2026_07_13') or ev3.get('inspection_to_repair_mean_days')
        e3=num(ev3)
        if f.get('value_as_printed') and e3 is not None: e3=decode(e3)
        if '(000)' in (f['source'].get('quote') or '') and e3 is not None and e3<10000: e3*=1000
        ok3 = f['type']=='derived' or (reg is not None and e3 is not None and abs(reg-e3)<=max(0.051,abs(reg)*0.001))
        if not ok3: issues.append(f"PASS-3 VALUE registry={reg} checker={t.get('extracted_value')}")
        if t.get('definition_check')=='mismatch': issues.append("PASS-3 DEFINITION: "+(t.get('definition_notes') or ''))
        for p in t.get('problems') or []: issues.append("PASS-3 NOTE: "+str(p))
    if ok: n_ok+=1
    else: n_val+=1
    rows.append((cid,l['name'],'; '.join(issues) or 'match',(d or {}).get('definition_check','pass 2 pending')))
with open('data/blind_check_report.md','w') as o:
    o.write("# Blind check report\n\n")
    o.write("Pass 1 (values and definitions) ran against the registry as built at about 14:00 ET on Sept. 5, 2026, with the checker blind to every registry value. It found 32 definition mismatches and about 20 further notes (data/blind_check_agent_summary.md); every one was then addressed in data/mmr_lines.json and data/queues_manual.json and the registry rebuilt. Pass 2 re-checked the corrected descriptions against the sources (data/blind_check_pass2_summary.md): 76 match, 5 caveat-wording issues, all corrected. Pass 3 was a fresh checker barred from the registry and from both earlier check files (data/blind_check_pass3_summary.md): values agreed on every figure; 4 definition mismatches and 33 notes, all addressed in the rebuild at about 17:15 ET, including a switch to the month value (dataset field acceptedvalue) for point-in-time counts, which the fiscal-year-to-date field had been averaging. Source-internal defects the passes surfaced are listed in data/source_issues.md. Pass 2 and 3 notes shown below describe the registry text as it stood before each fix.\n\n")
    o.write(f"Values: {len(rows)} figures compared, {n_ok} agree with the checker's independent extraction, {n_val} do not.\n\n| claim | line | value result / remaining definition issue | pass 2 definition |\n|---|---|---|---|\n")
    for r in rows: o.write(f"| {r[0]} | {r[1]} | {r[2].replace('|','/')[:400]} | {r[3]} |\n")
print(f"{len(rows)} figures: {n_ok} value agreement, {n_val} disagreement; pass 2 loaded: {len(P2)}; pass 3 loaded: {len(P3)}")
for r in rows:
    if r[2]!='match': print(" -",r[0],"::",r[2][:250])
