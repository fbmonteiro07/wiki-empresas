from pathlib import Path
p=Path('automation/financials/validate.py');s=p.read_text(encoding='utf-8');needle='for k,v in checks.items():\n';replace='from check_rendered import check as check_rendered\nrendered_checks,rendered_issues=check_rendered(root);checks.update(rendered_checks);issues.extend(rendered_issues)\n'+needle
assert s.count(needle)==1;s=s.replace(needle,replace);p.write_text(s,encoding='utf-8')
