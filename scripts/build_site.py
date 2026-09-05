"""Build the static site: data/site.json (slim registry for the page) and the Markdown pages (methodology, checks, gaps, source issues) as HTML in house chrome."""
import json, re, html, datetime as dt
R=json.load(open('data/registry.json'))
# slim registry: keep series as (date,value) pairs only, drop bulky repeats
slim={"built":R['built'],"lines":[]}
for l in R['lines']:
    L=dict(l); L['figures']=[]
    for f in l['figures']:
        F={k:v for k,v in f.items() if k not in ('series',)}
        if f.get('series'):
            F['series']=[[s['date'],s['value'],s.get('value_month')] for s in f['series'] if s.get('value') is not None]
        L['figures'].append(F)
    slim['lines'].append(L)
json.dump(slim,open('data/site.json','w'),separators=(',',':'))
print("site.json",len(json.dumps(slim))//1024,"KB")

def md_to_html(md):
    out=[]; in_table=False; in_list=False
    def inline(s):
        s=html.escape(s,quote=False)
        s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
        s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
        s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'<a href="\2">\1</a>',s)
        return s
    for line in md.split('\n'):
        if line.startswith('|'):
            cells=[c.strip() for c in line.strip().strip('|').split('|')]
            if all(re.fullmatch(r'-{3,}',c) for c in cells): continue
            if not in_table: out.append('<div class="tw"><table>'); in_table=True; out.append('<tr>'+''.join(f'<th>{inline(c)}</th>' for c in cells)+'</tr>'); continue
            out.append('<tr>'+''.join(f'<td>{inline(c)}</td>' for c in cells)+'</tr>'); continue
        elif in_table: out.append('</table></div>'); in_table=False
        if re.match(r'^\s*[-•]\s',line):
            if not in_list: out.append('<ul>'); in_list=True
            out.append('<li>'+inline(re.sub(r'^\s*[-•]\s','',line))+'</li>'); continue
        elif in_list and line.strip()=='' : out.append('</ul>'); in_list=False
        elif in_list: out.append('</ul>'); in_list=False
        m=re.match(r'^(#{1,4})\s+(.*)',line)
        if m: out.append(f'<h{len(m.group(1))+1}>{inline(m.group(2))}</h{len(m.group(1))+1}>'); continue
        if re.match(r'^\d+\.\s',line): out.append('<p class="num">'+inline(line)+'</p>'); continue
        if line.strip()=='': continue
        out.append('<p>'+inline(line)+'</p>')
    if in_table: out.append('</table></div>')
    if in_list: out.append('</ul>')
    return '\n'.join(out)

CHROME=open('site_chrome.html').read()
pages=[("methodology.html","How the counting works",["METHODOLOGY.md"]),
       ("checks.html","Fact-checking record",["data/blind_check_report.md","data/blind_check_agent_summary.md","data/blind_check_pass2_summary.md","data/blind_check_pass3_summary.md"]),
       ("gaps.html","Lines with no public count",["data/gaps.md","data/source_issues.md"])]
for fn,title,srcs in pages:
    body='\n<hr class="rule">\n'.join(md_to_html(open(s).read()) for s in srcs)
    open(fn,'w').write(CHROME.replace('{{TITLE}}',title).replace('{{BODY}}',body).replace('{{BUILT}}',R['built']))
    print("wrote",fn)
