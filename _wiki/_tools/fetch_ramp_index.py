r"""fetch_ramp_index.py -- pull the Ramp AI Index straight off ramp.com/data/ai-index.

The page is a Next.js app that ships EVERY dataset behind its charts inline, as the
server-component ("flight") payload in `self.__next_f.push([1,"..."])` script chunks:
adoption (overall, vendor, sector, size, state, Census estimate), the model-share
breakdown (overall + curated cuts), spend per employee (overall + curated cuts),
AI share of business spend, and the Token Spend Management sample (weekly token
volume / spend per model, daily 7-day token prices per maker). No CSV endpoint is
needed -- and the in-app browser cannot post to localhost anyway.

What this writes (ALL under _wiki/_data/ramp-ai-index/, feature-script rule):

  raw/<dataset>.json      every dataset exactly as Ramp ships it ("$undefined" -> null)
  fetch_meta.json         when fetched, row counts, latest month per dataset
  spend_per_employee.csv  the legacy 4-column export, regenerated from raw/spendPerEmployee
  model_share.csv         the legacy 5-column export, regenerated from raw/modelBreakdown
                          (model_share fraction -> model_share_pct)
  vintages/<name>.through-<YYYY-MM>.csv
                          the PREVIOUS csv, archived before it is overwritten, so a
                          restatement by Ramp stays auditable (build_ramp_index.py
                          diffs them into restatement.json)

Then run build_ramp_index.py -> build_ramp_dash.py as before.

    py "E:\Wiki Felipe empresas\_wiki\_tools\fetch_ramp_index.py"             # live
    py "E:\Wiki Felipe empresas\_wiki\_tools\fetch_ramp_index.py" --from-file page.html

stdlib only (machine sits behind a TLS proxy: unverified SSL context, browser UA).
"""
import csv
import datetime as dt
import io
import json
import os
import re
import shutil
import ssl
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
WIKI = os.path.dirname(HERE)
DIR = os.path.join(WIKI, "_data", "ramp-ai-index")
RAW = os.path.join(DIR, "raw")
VINT = os.path.join(DIR, "vintages")
URL = "https://ramp.com/data/ai-index"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")

LEGACY_SPEND = [
    ("date_month", "date_month"),
    ("median_monthly_spend_per_employee_usd", "median_pepm"),
    ("top_10_percent_median_spend_per_employee_usd", "top_10_percent_median_pepm"),
    ("top_1_percent_median_spend_per_employee_usd", "top_1_percent_median_pepm"),
]


def fetch_html(path=None):
    if path:
        return io.open(path, encoding="utf-8").read()
    ctx = ssl._create_unverified_context()
    req = urllib.request.Request(URL, headers={"User-Agent": UA, "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=120, context=ctx) as r:
        return r.read().decode("utf-8", "replace")


def flight_props(html):
    """Concatenate the flight chunks, then find the props object that carries the
    datasets (the one holding both adoptionOverall and spendPerEmployee)."""
    chunks = re.findall(r'self\.__next_f\.push\(\[1,("(?:[^"\\]|\\.)*")\]\)', html)
    if not chunks:
        raise SystemExit("no flight chunks found -- page layout changed?")
    payload = "".join(json.loads(c) for c in chunks)

    def find(o):
        if isinstance(o, dict):
            if "adoptionOverall" in o and "spendPerEmployee" in o:
                return o
            for v in o.values():
                r = find(v)
                if r:
                    return r
        elif isinstance(o, list):
            for v in o:
                r = find(v)
                if r:
                    return r
        return None

    for line in payload.split("\n"):
        if '"adoptionOverall"' not in line:
            continue
        m = re.match(r'^[0-9a-f]+:(.*)$', line)
        if not m:
            continue
        try:
            obj = json.loads(m.group(1))
        except ValueError:
            continue
        found = find(obj)
        if found:
            return found
    raise SystemExit("flight payload parsed but the dataset props object was not found")


def clean(o):
    """Ramp serialises missing values as the string '$undefined'."""
    if isinstance(o, dict):
        return dict((k, clean(v)) for k, v in o.items())
    if isinstance(o, list):
        return [clean(v) for v in o]
    if o == "$undefined":
        return None
    return o


def archive_previous(name):
    """Move the current csv to vintages/<name>.through-<last month>.csv (no overwrite)."""
    src = os.path.join(DIR, name + ".csv")
    if not os.path.exists(src):
        return None
    with io.open(src, newline="", encoding="utf-8-sig") as f:
        months = [r["date_month"][:7] for r in csv.DictReader(f) if r.get("date_month")]
    if not months:
        return None
    os.makedirs(VINT, exist_ok=True)
    dest = os.path.join(VINT, "%s.through-%s.csv" % (name, max(months)))
    if not os.path.exists(dest):
        shutil.copyfile(src, dest)
    return dest


def write_csv(path, header, rows):
    with io.open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def main(argv):
    src = None
    if "--from-file" in argv:
        src = argv[argv.index("--from-file") + 1]
    html = fetch_html(src)
    props = clean(flight_props(html))
    os.makedirs(RAW, exist_ok=True)

    meta = {"url": URL, "fetched_at": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "source_file": src, "html_bytes": len(html.encode("utf-8")),
            "filterModeBundleVersion": props.get("filterModeBundleVersion"),
            "datasets": {}}
    for k, v in sorted(props.items()):
        if not isinstance(v, (list, dict)):
            continue
        with io.open(os.path.join(RAW, k + ".json"), "w", encoding="utf-8") as f:
            json.dump(v, f, ensure_ascii=True, separators=(",", ":"))
        rows = v if isinstance(v, list) else sum((x for x in v.values() if isinstance(x, list)), [])
        dates = sorted(set(str(r.get("date_month") or r.get("my_date") or r.get("period_end")
                               or r.get("usage_date") or "")[:10] for r in rows if isinstance(r, dict)))
        dates = [d for d in dates if d]
        meta["datasets"][k] = {"rows": len(rows), "first": dates[0] if dates else None,
                               "latest": dates[-1] if dates else None}
        print("  raw/%-28s %6d rows  %s -> %s" % (k + ".json", len(rows),
                                                   dates[0] if dates else "-", dates[-1] if dates else "-"))

    # ---- legacy csv 1: spend per employee (3 cohorts)
    prev = archive_previous("spend_per_employee")
    spe = sorted(props["spendPerEmployee"], key=lambda r: r["date_month"])
    write_csv(os.path.join(DIR, "spend_per_employee.csv"), [h for h, _ in LEGACY_SPEND],
              [[r[k] for _, k in LEGACY_SPEND] for r in spe])
    print("spend_per_employee.csv: %d months, %s -> %s%s" % (
        len(spe), spe[0]["date_month"][:7], spe[-1]["date_month"][:7],
        ("  (previous archived -> %s)" % os.path.relpath(prev, DIR)) if prev else ""))

    # ---- legacy csv 2: model share (named models, pct)
    prev = archive_previous("model_share")
    mb = sorted(props["modelBreakdown"],
                key=lambda r: (r["date_month"], r["provider_display_order"], r["model_display_order"]))
    write_csv(os.path.join(DIR, "model_share.csv"),
              ["date_month", "provider", "model", "model_type", "model_share_pct"],
              [[r["date_month"], r["ai_provider"], r["model_label"],
                "Named model" if r["model_spend_type"] == "named_model" else r["model_spend_type"],
                "%.4f" % (100.0 * r["model_share"])] for r in mb])
    months = sorted(set(r["date_month"][:7] for r in mb))
    print("model_share.csv: %d rows, %d months, %s -> %s%s" % (
        len(mb), len(months), months[0], months[-1],
        ("  (previous archived -> %s)" % os.path.relpath(prev, DIR)) if prev else ""))

    with io.open(os.path.join(DIR, "fetch_meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=1)
    print("fetch_meta.json written (%s)" % meta["fetched_at"])


if __name__ == "__main__":
    main(sys.argv[1:])
