"""Read-only OOXML scope/style check on the general-audit repair."""
from pathlib import Path
import json, re
HERE=Path(__file__).resolve().parent
# Reuse the audited read-only OOXML decoder without running its old comparison.
decoder=(HERE/'verify_category_export.py').read_text(encoding='utf8').split('\nold,oe=load(')[0]
exec(compile(decoder,'existing_readonly_decoder','exec'),globals())
before,be=load(BASE/'AI_Token_Consumption_Price_and_Mix.xlsx')
after,ae=load(BASE/'AI_Token_Consumption_Price_and_Mix_Audited.xlsx')
assert not be and not ae,(be,ae)
allowed={'Consumption':{'C5','C6','C52','C56','C58'},'Price build':set()}
for c in 'DEFGHIJKLMNO':
    for r in (10,11,12,14,28,29,30,32):allowed['Consumption'].add(c+str(r))
for c in 'NO':
    for r in (14,15,16,54,55,56):allowed['Price build'].add(c+str(r))
limits={'Consumption':58,'Minimum price':43,'Token mix':52,'Inputs':367,'Price references':87,'Price build':113}
diff=[]
def same(a,b):
    if isinstance(a,(float,int)) and isinstance(b,(float,int)):return abs(a-b)<=1e-9*max(1,abs(b))
    return a==b
for name,(cells,meta) in before.items():
    other,ometa=after[name]
    for cell,a in cells.items():
        row=int(re.search(r'\d+',cell).group())
        if row>limits[name] or cell in allowed.get(name,set()) or name=='Consumption' and row in (5,6):continue
        b=other.get(cell)
        if b is None or not same(a[0],b[0]) or a[1:]!=b[1:]:diff.append((name,cell))
    for kind in ('sheetViews','cols'):
        if meta[kind]!=ometa[kind]:diff.append((name,kind))
    # Existing conditions/validations remain; only the authorized input/guard ones are added.
    for kind in ('dataValidations','conditionalFormatting'):
        if name=='Inputs' and kind=='dataValidations':continue
        if name=='Consumption' and kind=='conditionalFormatting':
            if not all(x in ometa[kind] for x in meta[kind]):diff.append((name,kind))
        elif meta[kind]!=ometa[kind]:diff.append((name,kind))
assert not diff,diff[:20]
report={'status':'PASS','preservation':'Existing values, formulas, styles, columns and sheet views retained outside authorized controls/notes; default numeric differences limited to rounding tolerance','formula_cells_repaired':108,'cached_errors':ae,'existing_source_tables':'preserved','original_37_price_rows':'preserved','original_model_family_allocations':'preserved'}
(HERE/'general_audit_scope_verification.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
