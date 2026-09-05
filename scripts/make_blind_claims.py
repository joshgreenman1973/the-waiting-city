"""Emit data/blind_claims.json: for every figure, the source and a neutral description of the quantity,
with the registry's value, spread and quotes REMOVED, so an independent checker can extract them blind.
Also emits the registry's descriptive fields for the definition check (name, what_for, end_event, unit, center, duration_kind, standard)."""
import json
R=json.load(open('data/registry.json'))
claims=[]
for line in R['lines']:
    for i,f in enumerate(line['figures']):
        src=f['source']
        c={"claim_id":f"{line['id']}#{i}","line_id":line['id'],"agency":line['agency'],
           "quantity":{"type":f['type'],"unit_of_value":f['unit_of_value'],"period_label":f['period_label']},
           "source":{"url":src.get('url'),"title":src.get('title'),"publisher":src.get('publisher'),"date":src.get('date'),"local_copy":src.get('local_copy')},
           "how_to_find": ("Query rbed-zzin for agency='%s' and indicator='%s'; take the latest non-NA acceptedvalueytd and its valuedate; also copy the description field verbatim."%(line['agency'],src['quote'].rsplit(':',1)[0])) if 'rbed-zzin' in (f['refresh'].get('query_or_url') or '')
                          else ("Recompute independently from the dataset named; do not reuse any script in scripts/." if f.get('grade')=='A-c'
                          else ("Derived figure: recompute from the figures in the same line's source." if f['type']=='derived' else "Locate the figure in the source (local copy preferred) and copy the sentence verbatim.")),
           "registry_description_to_check":{"line_name":line['name'],"what_for":line['what_for'],"end_event":line['end_event'],"unit":line['unit'],"center":f.get('center'),"duration_kind":f.get('duration_kind'),"standard":f.get('standard'),"caveats":f.get('caveats')}}
        claims.append(c)
json.dump(claims,open('data/blind_claims.json','w'),indent=1)
print(len(claims),"claims written; values, spreads, quotes and definition_quote withheld")
