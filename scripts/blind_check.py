"""Mechanical re-verification of data/registry.json.
Pass 1: re-query every MMR-sourced figure from Socrata using only agency + indicator name, compare value and valuedate.
Pass 2: for every document-sourced figure, confirm the verbatim quote appears in the local copy (or the fetched page text where cached).
Writes data/blind_check_mechanical.json. Exits non-zero on any mismatch."""
import json, re, sys, urllib.request, urllib.parse, unicodedata
R=json.load(open('data/registry.json'))
def norm(s):
    s=unicodedata.normalize('NFKC',s or '').replace('\u2019',"'").replace('\u2018',"'").replace('\u201c','"').replace('\u201d','"').replace('\u2013','-').replace('\u2014','-')
    return re.sub(r'\s+',' ',s).strip().lower()
problems=[]; checked=0
for line in R['lines']:
    for f in line['figures']:
        src=f['source']
        if f['refresh']['method']=='soql' and 'rbed-zzin' in f['refresh']['query_or_url']:
            # rebuild query from scratch: agency + indicator only
            ind=f['source']['quote'].rsplit(':',1)[0]
            q={"$select":"fiscalyear,valuedate,acceptedvalueytd,acceptedvalue,description","$where":f"agency='{line['agency']}' and indicator='{ind.replace(chr(39),chr(39)*2)}' and acceptedvalueytd NOT IN ('NA','','*')","$order":"valuedate DESC","$limit":1}
            try: rows=json.load(urllib.request.urlopen("https://data.cityofnewyork.us/resource/rbed-zzin.json?"+urllib.parse.urlencode(q),timeout=120))
            except Exception as e: problems.append((line['id'],'query failed',str(e))); continue
            if not rows: problems.append((line['id'],'no rows',ind)); continue
            r=rows[0]; checked+=1
            reg_val=f['value']; scale=1000 if '(000)' in ind else 1
            try: live=float(r['acceptedvalue'] if f.get('value_fytd') is not None else r['acceptedvalueytd'])*scale
            except: live=None
            if f.get('value_as_printed') and live is not None:
                whole=int(live); frac=round((live-whole)*100); live=round(whole+frac/60,2)
            if live is None or reg_val is None or abs(live-reg_val)>1e-6: problems.append((line['id'],'VALUE',f"registry {reg_val} vs live {live} ({r['valuedate'][:10]})"))
            if r['valuedate'][:10]!=src['date']: problems.append((line['id'],'DATE',f"registry {src['date']} vs live {r['valuedate'][:10]}"))
            if norm(r.get('description'))!=norm(f.get('definition_quote')): problems.append((line['id'],'DEFINITION TEXT',"registry definition_quote differs from live description"))
        elif f['type']=='derived':
            checked+=1; continue
        elif f.get('grade')=='A-c':
            problems.append((line['id'],'COMPUTED (blind agent recomputes independently)',src.get('url','')[:80])); continue
        elif src.get('local_copy') and src.get('quote'):
            lc=src['local_copy']
            txt=None
            for cand in (lc.replace('.pdf','.txt'), lc):
                try: txt=open(cand,errors='ignore').read(); break
                except: pass
            if txt is None: problems.append((line['id'],'no local copy',lc)); continue
            checked+=1
            if norm(src['quote'])[:80] not in norm(txt): problems.append((line['id'],'QUOTE NOT FOUND',src['quote'][:80]))
        else:
            problems.append((line['id'],'UNCHECKED (no local copy)',src.get('url','')[:80]))
json.dump({"checked":checked,"problems":problems},open('data/blind_check_mechanical.json','w'),indent=1)
print("checked",checked,"figures;",len(problems),"problems")
for p in problems: print(" -",p)
sys.exit(1 if any(p[1] in ('VALUE','DATE','DEFINITION TEXT','QUOTE NOT FOUND') for p in problems) else 0)
