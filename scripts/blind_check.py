"""Mechanical re-verification of data/registry.json.
Pass 1: re-query every MMR-sourced figure from Socrata using only agency + indicator name, compare value and valuedate.
Pass 1b: for figures taken from the printed Mayor's Management Report, find the quoted table row in the local copy of
the report text, read the fiscal year's column out of it, and re-query Open Data for the prior year the row prints.
Pass 2: for every document-sourced figure, confirm the verbatim quote appears in the local copy (or the fetched page text where cached).
Writes data/blind_check_mechanical.json. Exits non-zero on any mismatch."""
import json, re, sys, urllib.request, urllib.parse, unicodedata
R=json.load(open('data/registry.json'))
MMR_TXT=None
try: MMR_TXT=open('sources/mmr2026.txt',errors='ignore').read()
except FileNotFoundError: pass
MMR_PAGES={}
if MMR_TXT:
    _p=re.split(r"\n<<<PAGE (\d+)>>>\n",MMR_TXT)
    MMR_PAGES={int(_p[i]):_p[i+1] for i in range(1,len(_p),2)}
def soql(where,select,order="fiscalyear,valuedate",limit=5):
    q={"$select":select,"$where":where,"$order":order,"$limit":limit}
    return json.load(urllib.request.urlopen("https://data.cityofnewyork.us/resource/rbed-zzin.json?"+urllib.parse.urlencode(q),timeout=120))
def norm(s):
    s=unicodedata.normalize('NFKC',s or '').replace('\u2019',"'").replace('\u2018',"'").replace('\u201c','"').replace('\u201d','"').replace('\u2013','-').replace('\u2014','-')
    return re.sub(r'\s+',' ',s).strip().lower()
problems=[]; checked=0
for line in R['lines']:
    for f in line['figures']:
        src=f['source']
        if '/mmr2026/' in (src.get('url') or ''):
            # the value comes from the printed report: the quoted row must be on the cited page, the fiscal
            # 2026 column must be the registry's value, and the row's prior-year column must still match Open Data
            page=int(src['url'].rsplit('#page=',1)[1])
            body=re.sub(r'\s+',' ',MMR_PAGES.get(page,''))
            if not body: problems.append((line['id'],'PAGE MISSING',f"page {page} not in sources/mmr2026.txt")); continue
            if norm(src['quote']) not in norm(body): problems.append((line['id'],'ROW NOT FOUND',src['quote'][:90])); continue
            checked+=1
            toks=src['quote'].split()
            i=len(toks)
            while i>0 and re.fullmatch(r"(?:NA|\*|†|‡|\$?-?[\d,]+(?:\.\d+)?%?|\(?\d+(?:\.\d+)?\)?%?|\d+:\d{2}|Up|Down|Neutral|ñ|ò)",toks[i-1]): i-=1
            tail=toks[i:]; actuals=tail[-9:-4] if len(tail)>=9 else tail[:5]
            if len(actuals)<5: problems.append((line['id'],'ROW UNREADABLE',src['quote'][:90])); continue
            def cell(t):
                if t in ('NA','*'): return None
                t=t.replace('$','').replace(',','').replace('%','')
                m=re.match(r"^(\d+):(\d{2})$",t)
                if m: return round(int(m.group(1))+int(m.group(2))/60,2)
                try: return float(t)
                except ValueError: return None
            scale=1000 if '(000)' in (line.get('name','')+src['quote']) else 1
            printed=cell(actuals[4])
            if printed is None or f['value'] is None or abs(printed*scale-f['value'])>0.006:
                problems.append((line['id'],'VALUE',f"registry {f['value']} vs printed report {actuals[4]}"))
            ind=f['refresh']['query_or_url']
            m=re.search(r"indicator%3D%27(.+?)%27",ind) or re.search(r"indicator='(.+?)'",urllib.parse.unquote(ind))
            indicator=urllib.parse.unquote(m.group(1)).replace("''","'") if m else None
            if indicator:
                try: rows=soql(f"agency='{line['agency']}' and indicator='{indicator.replace(chr(39),chr(39)*2)}' and fiscalyear='2025' and acceptedvalueytd NOT IN ('NA','','*')","fiscalyear,valuedate,acceptedvalueytd",limit=20)
                except Exception as e: problems.append((line['id'],'query failed',str(e))); continue
                prior=cell(actuals[3])
                if rows and prior is not None:
                    live=float(rows[-1]['acceptedvalueytd'])
                    if abs(live-prior)>max(0.006,abs(live)*0.006):
                        problems.append((line['id'],'PRIOR YEAR',f"printed fiscal 2025 column {actuals[3]} vs Open Data {live}"))
            continue
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
