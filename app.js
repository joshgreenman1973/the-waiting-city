(async function(){
const AG={ACS:"Administration for Children's Services",BIC:"Business Integrity Commission",CCHR:"Commission on Human Rights",DCAS:"Department of Citywide Administrative Services",DCP:"Department of City Planning",DCWP:"Department of Consumer and Worker Protection",DFTA:"Department for the Aging",DHS:"Department of Homeless Services",DOB:"Department of Buildings",DOE:"Department of Education",DOF:"Department of Finance",DOHMH:"Department of Health and Mental Hygiene",DORIS:"Department of Records and Information Services",DOT:"Department of Transportation",DPR:"Department of Parks and Recreation",HPD:"Department of Housing Preservation and Development",HRA:"Human Resources Administration",LPC:"Landmarks Preservation Commission",NYCHA:"New York City Housing Authority",NYCHH:"NYC Health + Hospitals",OATH:"Office of Administrative Trials and Hearings","NYS Unified Court System":"New York State Unified Court System"};
const TYPE={stock:"how many are waiting",duration:"how long it takes",timeliness_rate:"share handled on time",throughput:"cleared per period",demand:"demand at the door",derived:"derived"};
const R=await (await fetch('data/site.json')).json();
const L=R.lines; const byId=Object.fromEntries(L.map(l=>[l.id,l]));
for(const id of ['built','built2','built3']) document.getElementById(id).textContent=fmtDate(R.built);
const $=s=>document.querySelector(s);
let tier='all', q='', ftype='', fgrade='', spreadOnly=false, zero=false, sel=null;

function fmtDate(s){const d=new Date(s+'T12:00:00');return d.toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'}).replace(/(\w{3}) /,'$1. ');}
function fmtNum(v,u){if(v==null)return 'n/a';const n=Math.abs(v)>=1000?Math.round(v).toLocaleString('en-US'):(Number.isInteger(v)?v:+v.toFixed(1)).toLocaleString('en-US');return n+(u?' '+u:'');}
function unitShort(f){let u=f.unit_of_value||'';return u.split(' (')[0];}
function gradeCls(g){return 'grade '+(g==='A-c'?'Ac':g);}
function esc(s){return String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
function primary(l){return l.figures[0];}

// counts
(function(){const figs=L.flatMap(l=>l.figures);const gA=figs.filter(f=>f.grade==='A'||f.grade==='A-c').length;const spread=L.filter(l=>l.figures.some(f=>f.spread)).length;const ags=new Set(L.map(l=>l.agency)).size;
$('#counts').innerHTML=[[L.length,'lines tracked'],[figs.length,'figures'],[gA+' of '+figs.length,'figures re-queryable (grade A)'],[ags,'agencies and bodies'],[spread,'lines with a published spread'],[12,'lines with no public count']].map(([b,s])=>`<div><b>${b}</b><span>${s}</span></div>`).join('');})();

// facts, all pulled from the registry so they cannot drift from it
const FACTS=[
 ['nycha-section8-waitlist-mmr',f=>`<b>${fmtNum(f.value,'households')}</b> were on the New York City Housing Authority's Section 8 voucher waiting list in March 2026. Voucher issuance to that list was paused as of Sept. 29, 2025, while the authority absorbed Emergency Housing Voucher households.`],
 ['hpd-housing-connect',f=>`Housing Connect received about <b>${fmtNum(f.value,'applications')}</b> for about 10,000 units in 2024. The Furman Center cites an HPD estimate of nearly 600,000 unique applicants, undated.`],
 ['dcas-eligible-lists',f=>`<b>${fmtNum(f.value,'entries')}</b> sat on active civil service eligible lists on July 13, 2026. On Sept. 5, 88,082 of the live entries were on lists past their four-year anniversary.`],
 ['hra-cash-assistance-timeliness',f=>`<b>${f.value}%</b> of cash assistance applications were decided within the 30-day standard, fiscal 2026 to date through March 2026. The fiscal 2024 figure was 42.4%.`],
 ['nycha-vacant-unit-turnaround',f=>`A vacant public housing apartment took <b>${fmtNum(f.value,'days')}</b> on average to be re-occupied, fiscal 2026 to date through March 2026.`],
 ['cchr-caseload-age',f=>`The open complaints before the Commission on Human Rights had been open <b>${fmtNum(f.value,'days')}</b> on average in February 2026, against 607 a year earlier; open matters rose from 1,309 to 1,742.`],
 ['dcp-eas-zoning-review',f=>`Zoning actions with an environmental assessment took a median <b>${fmtNum(f.value,'days')}</b> to enter public review in the first four months of fiscal 2026, against 278 a year earlier.`],
 ['dob-filing-to-approval-computed',f=>`Department of Buildings filings: median <b>${f.value.toFixed(1)} days</b> from filing to approval, but professionally certified filings clear in ${f.spread.by_review_type['Professional Certification'].median.toFixed(1)} days and standard plan examination in ${f.spread.by_review_type['Standard Plan Examination'].median.toFixed(1)}, with a 90th percentile of ${Math.round(f.spread.by_review_type['Standard Plan Examination'].p90)}. Filings approved Sept. 1, 2025 to Aug. 31, 2026.`],
 ['hpd-problem-close-computed',f=>`Housing complaints: non-emergency problems took a median <b>${f.spread.by_type['NON EMERGENCY'].median} days</b> to close, with a 90th percentile of ${f.spread.by_type['NON EMERGENCY'].p90}. That 90th percentile was ${f.spread.by_type_borough['NON EMERGENCY|MANHATTAN'].p90} in Manhattan and ${f.spread.by_type_borough['NON EMERGENCY|STATEN ISLAND'].p90} in Staten Island. Problems closed March 1 to Aug. 31, 2026.`],
 ['nycha-skilled-trades-work-orders',f=>`Public housing repairs needing skilled trades or vendors took <b>${fmtNum(f.value,'days')}</b> on average, fiscal 2026 to date through March 2026; the authority's own metrics page shows trade averages from 18 days (roofer) to 608 (painter) and 761 (vendor), undated.`],
 [null,()=>`<b>No public count</b> exists for the public housing waiting list itself. It leads the <a href="gaps.html">list of twelve lines with no citable figure</a>.`]
];
$('#facts').innerHTML=FACTS.map(([id,fn])=>{const l=id?byId[id]:null;const f=l?primary(l):null;try{return `<p>${fn(f)}${l?` <a href="#${l.id}" data-sel="${l.id}" class="per">See the line</a>`:''}</p>`}catch(e){return ''}}).join('');

// filters
function visible(){return L.filter(l=>{
  if(tier!=='all'&&String(l.tier)!==tier)return false;
  if(ftype&&!l.figures.some(f=>f.type===ftype))return false;
  if(fgrade&&!l.figures.some(f=>f.grade===fgrade))return false;
  if(spreadOnly&&!l.figures.some(f=>f.spread))return false;
  if(q){const hay=(l.name+' '+l.agency+' '+(AG[l.agency]||'')+' '+l.what_for+' '+l.figures.map(f=>(f.definition_quote||'')).join(' ')).toLowerCase();if(!hay.includes(q))return false;}
  return true;});}
function renderList(){const v=visible();const el=$('#list');if(!v.length){el.innerHTML='<div class="empty">No lines match.</div>';return;}
  const groups={};for(const l of v){(groups[l.agency]=groups[l.agency]||[]).push(l);}
  el.innerHTML=Object.keys(groups).sort((a,b)=>(AG[a]||a).localeCompare(AG[b]||b)).map(a=>`<div class="colhead"><span>${esc(AG[a]||a)}</span><span>${groups[a].length}</span></div>`+groups[a].sort((x,y)=>x.name.localeCompare(y.name)).map(l=>{const f=primary(l);return `<button class="rec${sel===l.id?' sel':''}" data-sel="${l.id}"><span class="val">${esc(fmtNum(f.value,unitShort(f)))}</span><b>${esc(l.name)}</b><span class="meta"><span class="${gradeCls(f.grade)}">${f.grade}</span>${esc(TYPE[f.type]||f.type)} · ${esc(f.center&&f.center!=='n/a'?f.center:'')} ${f.spread?'· spread published':''}</span></button>`}).join('')).join('');}

// sparkline
function spark(f){const s=f.series;if(!s||s.length<3)return '';const W=640,H=150,P={l:44,r:12,t:12,b:22};
  const vals=s.map(p=>p[1]);const months=s.map(p=>p[2]).filter(v=>v!=null);const all=vals.concat(months);
  let lo=zero?0:Math.min(...all),hi=Math.max(...all);if(hi===lo)hi=lo+1;const pad=(hi-lo)*0.06;if(!zero)lo-=pad;hi+=pad;if(zero&&lo<0)lo=0;
  const x=i=>P.l+(W-P.l-P.r)*i/(s.length-1),y=v=>P.t+(H-P.t-P.b)*(1-(v-lo)/(hi-lo));
  const path=cls=>{let d='';let on=false;s.forEach((p,i)=>{const v=cls==='l'?p[1]:p[2];if(v==null){on=false;return;}d+=(on?'L':'M')+x(i).toFixed(1)+' '+y(v).toFixed(1)+' ';on=true;});return `<path class="${cls}" d="${d}"/>`;};
  const monthsDiffer=months.length&&s.some(p=>p[2]!=null&&p[1]!=null&&Math.abs(p[2]-p[1])>1e-9);
  const yt=[lo+pad,hi-pad].map(v=>`<text x="${P.l-6}" y="${y(v)+3}" text-anchor="end">${fmtNum(+v.toFixed(v<10?1:0))}</text>`).join('');
  const xt=`<text x="${P.l}" y="${H-6}">${s[0][0].slice(0,7)}</text><text x="${W-P.r}" y="${H-6}" text-anchor="end">${s[s.length-1][0].slice(0,7)}</text>`;
  const zeroLine=zero?`<line class="ax" x1="${P.l}" x2="${W-P.r}" y1="${y(0)}" y2="${y(0)}"/>`:'';
  return `<div class="legend"><span><i></i>${monthsDiffer?'fiscal-year-to-date value':'published value'}</span>${monthsDiffer?'<span><i class="m"></i>month value</span>':''}<span>${zero?'y-axis starts at zero':'y-axis fitted to the data (toggle above)'}</span></div><svg class="spark" viewBox="0 0 ${W} ${H}" role="img" aria-label="Series"><line class="ax" x1="${P.l}" x2="${W-P.r}" y1="${H-P.b}" y2="${H-P.b}"/>${zeroLine}${path('l')}${monthsDiffer?path('m'):''}${yt}${xt}</svg>`;}

function spreadTable(sp){if(!sp)return '';const rows=[];const walk=(o,pre)=>{for(const[k,v]of Object.entries(o)){const key=(pre?pre+' · ':'')+k.replace(/_/g,' ');if(v&&typeof v==='object'&&!Array.isArray(v)){if('median' in v||'p90' in v||'n' in v){rows.push([key,Object.entries(v).map(([a,b])=>`${a.replace(/_/g,' ')} ${typeof b==='number'?fmtNum(b):esc(b)}`).join(', ')]);}else walk(v,key);}else rows.push([key,typeof v==='number'?fmtNum(v):esc(String(v))]);}};walk(sp,'');
  return `<table class="spreadt">${rows.map(([k,v])=>`<tr><td>${esc(k)}</td><td class="n">${v}</td></tr>`).join('')}</table>`;}

function detailHTML(l){const f=primary(l);const others=l.figures.slice(1);
  const fig=(f,idx)=>`
   <dl class="f">
    <div><dt>${idx==null?'Latest figure':'Figure '+(idx+2)}</dt><dd><span class="big">${esc(fmtNum(f.value,f.unit_of_value))}</span>${f.value_as_printed?` <span class="per">(printed as ${esc(f.value_as_printed)})</span>`:''}</dd></div>
    <div><dt>Period</dt><dd>${esc(f.period_label)}</dd></div>
    <div><dt>Measure</dt><dd>${esc(TYPE[f.type]||f.type)}${f.center&&f.center!=='n/a'?'; center: '+esc(f.center):''}${f.duration_kind&&f.duration_kind!=='n/a'?'; '+esc(f.duration_kind)+' wait':''}</dd></div>
    ${f.standard?`<div><dt>Standard</dt><dd>${esc(f.standard)}</dd></div>`:''}
    <div><dt>Grade</dt><dd><span class="${gradeCls(f.grade)}">${f.grade}</span>${esc(f.grade_reason)}</dd></div>
    <div><dt>Spread</dt><dd>${f.spread?spreadTable(f.spread):''}${f.spread_note?esc(f.spread_note):(f.spread?'':'Not published.')}</dd></div>
   </dl>
   ${f.series?spark(f):''}
   ${f.definition_quote?`<div class="narr"><h4>The source's own definition</h4><div class="quote">${esc(f.definition_quote)}</div>${f.definition_changes&&f.definition_changes.length>1?`<p style="font-size:.9rem;color:var(--ink2)">The definition text changed ${f.definition_changes.length-1} time(s) across fiscal years in the dataset; each version is in the registry data.</p>`:''}</div>`:''}
   ${f.caveats&&f.caveats.length?`<div class="narr"><h4>Read with</h4><ul class="caveats">${f.caveats.map(c=>`<li>${esc(c)}</li>`).join('')}</ul></div>`:''}
   <div class="narr"><h4>Source</h4><p>${esc(f.source.title)}. ${esc(f.source.publisher)}${f.source.date?', '+esc(f.source.date):''}.</p>${f.source.quote&&f.type!=='derived'?`<div class="quote">${esc(f.source.quote)}</div>`:''}
   ${f.source.url?`<a class="srcbtn" href="${esc(f.source.url)}" target="_blank" rel="noopener">Open the source</a>`:''} ${f.refresh&&f.refresh.method==='soql'&&f.refresh.query_or_url.includes('rbed-zzin')?`<button class="srcbtn" data-soql="${esc(f.refresh.query_or_url)}">See the records</button>`:''}
   <div class="records"></div></div>`;
  return `<div class="dh"><div class="lbl">${esc(AG[l.agency]||l.agency)} · tier ${l.tier}</div><h2>${esc(l.name)}</h2>
   <p style="margin:8px 0 0;font-size:.95rem"><strong>Waiting for:</strong> ${esc(l.what_for)}. <strong>The wait ends when:</strong> ${esc(l.end_event)}. <strong>Counted in:</strong> ${esc(l.unit)}.${l.list_status&&l.list_status!=='rolling'?' <strong>List:</strong> '+esc(l.list_status)+'.':''}</p></div>
   <div class="pad">${fig(f)}${others.map((o,i)=>fig(o,i)).join('')}
   ${l.duplicates_with&&l.duplicates_with.length?`<div class="narr"><h4>The same household may also be in</h4><p>${l.duplicates_with.map(d=>byId[d]?`<a href="#${d}" data-sel="${d}">${esc(byId[d].name)}</a>`:esc(d)).join(' · ')}</p></div>`:''}
   ${l.raise_grade?`<div class="narr"><h4>What would improve this line</h4><p>${esc(l.raise_grade)}</p></div>`:''}</div>`;}

function renderDetail(openDrawer){const l=byId[sel];const el=$('#detail');if(!l){el.innerHTML='<div class="empty">Select a line.</div>';return;}el.innerHTML=detailHTML(l);
  if(openDrawer&&window.matchMedia('(max-width:900px)').matches){$('#dtitle').textContent=l.name;$('#dbody').innerHTML=detailHTML(l);$('#drawer').classList.add('open');}}
async function loadRecords(btn){const url=btn.dataset.soql;const box=btn.closest('.narr').querySelector('.records');box.innerHTML='<p style="font-size:.9rem;color:var(--ink2)">Loading the rows behind this figure…</p>';
  try{const rows=await (await fetch(url)).json();if(!rows.length)throw new Error('no rows');
   box.innerHTML=`<p style="font-size:.9rem;color:var(--ink2)">${rows.length} rows from the Mayor's Management Report indicators dataset, oldest first. Value is the dataset's fiscal-year-to-date field; the month value is shown where the dataset has one.</p><div style="overflow-x:auto"><table class="h"><tr><th>Fiscal year</th><th>Date</th><th class="n">Value (FYTD)</th><th class="n">Month value</th><th>Frequency</th></tr>${rows.slice().reverse().map(r=>`<tr><td>${esc(r.fiscalyear)}</td><td>${esc((r.valuedate||'').slice(0,10))}</td><td class="n">${esc(r.acceptedvalueytd)}</td><td class="n">${esc(r.acceptedvalue??'')}</td><td>${esc(r.frequency||'')}</td></tr>`).join('')}</table></div><p style="font-size:.86rem"><a href="${esc(url)}" target="_blank" rel="noopener">The query itself</a> (returns machine-readable JSON).</p>`;}
  catch(e){box.innerHTML='<p style="font-size:.9rem;color:var(--ink4)">The records could not be loaded just now. <a href="'+esc(url)+'" target="_blank" rel="noopener">Open the query directly.</a></p>';}}

document.addEventListener('click',e=>{const s=e.target.closest('[data-sel]');if(s){e.preventDefault();sel=s.dataset.sel;history.replaceState(null,'','#'+sel);renderList();renderDetail(true);const d=$('#detail');if(!window.matchMedia('(max-width:900px)').matches)d.scrollIntoView({block:'nearest'});return;}
  const b=e.target.closest('[data-soql]');if(b){loadRecords(b);return;}});
$('#tabs').addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;tier=b.dataset.tier;[...$('#tabs').children].forEach(x=>x.classList.toggle('on',x===b));renderList();});
$('#q').addEventListener('input',e=>{q=e.target.value.trim().toLowerCase();renderList();});
$('#ftype').addEventListener('change',e=>{ftype=e.target.value;renderList();});
$('#fgrade').addEventListener('change',e=>{fgrade=e.target.value;renderList();});
$('#spreadonly').addEventListener('click',e=>{spreadOnly=!spreadOnly;e.target.setAttribute('aria-pressed',spreadOnly);renderList();});
$('#zero').addEventListener('click',e=>{zero=!zero;e.target.setAttribute('aria-pressed',zero);renderDetail();});
$('#cautionbtn').addEventListener('click',()=>$('#caution').classList.toggle('open'));
$('#xbtn').addEventListener('click',()=>$('#drawer').classList.remove('open'));$('#scrim').addEventListener('click',()=>$('#drawer').classList.remove('open'));
const h=location.hash.slice(1);if(h&&byId[h])sel=h;else sel='nycha-section8-waitlist-mmr';
renderList();renderDetail();
})();
