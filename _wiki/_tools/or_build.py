r"""
or_build.py — turn the cached OpenRouter snapshot into the dashboard model.

Reads the newest _wiki/_data/openrouter/raw/<date>/ snapshot (pointer: latest.txt),
joins the token rankings to per-token pricing, maps each model to its lab, and
computes token share (total AND paid-only) + request share + IMPLIED $ + momentum,
by model and by lab.

IMPLIED $ = observed tokens x observed OpenRouter LIST price, with CACHING OFF
(the public feed reports total_native_tokens_cached = 0 on every row, so every
input token is billed at full list). It is therefore a CEILING on inference spend
routed through OpenRouter — NOT realized revenue and NOT a lab's total ARR. We
carry a cache-sensitivity range (0/50/70% of input priced at each model's
cache-read rate) to show how soft the ceiling is. Lead with RELATIVE RANK.

Writes _wiki/_data/openrouter/dashboard.json and appends _.../history.jsonl.
Prints a guardrail report (Step-3 of the estimate discipline) to stdout.

Run:  py "E:\Wiki Felipe empresas\_wiki\_tools\or_build.py"
"""
import json
import re
import datetime as dt
from pathlib import Path
from collections import defaultdict

DATA = Path("E:/Wiki Felipe empresas/_wiki/_data")
OR = DATA / "openrouter"

# capture: how OpenRouter $ maps to the lab.
LAB = {
    "openai": ("OpenAI", "first-party", "OpenAI (private)"),
    "anthropic": ("Anthropic", "first-party", "Anthropic (private)"),
    "google": ("Google (Gemini)", "first-party", "GOOGL"),
    "x-ai": ("xAI (Grok)", "first-party", "xAI (private)"),
    "deepseek": ("DeepSeek", "open+own", "DeepSeek (private)"),
    "moonshotai": ("Moonshot (Kimi)", "open+own", "Moonshot (private)"),
    "mistralai": ("Mistral", "open+own", "Mistral (private)"),
    "z-ai": ("Z.ai (Zhipu)", "open+own", "Zhipu (private)"),
    "minimax": ("MiniMax", "open+own", "MiniMax (private)"),
    "stepfun": ("StepFun", "open+own", "StepFun (private)"),
    "qwen": ("Qwen (Alibaba)", "open-weight", "BABA"),
    "meta": ("Meta (Llama)", "open-weight", "META"),
    "nvidia": ("NVIDIA (Nemotron)", "open-weight", "NVDA"),
    "tencent": ("Tencent", "open-weight", "0700.HK"),
    "xiaomi": ("Xiaomi", "open-weight", "1810.HK"),
    "kwaipilot": ("Kuaishou (Kwai)", "open-weight", "1024.HK"),
    "meituan": ("Meituan", "open-weight", "3690.HK"),
    "thinkingmachines": ("Thinking Machines", "open+own", "TM (private)"),
    "poolside": ("Poolside", "open+own", "Poolside (private)"),
    "nousresearch": ("Nous Research", "open-weight", "private"),
    "nous": ("Nous Research", "open-weight", "private"),
    "cohere": ("Cohere", "first-party", "Cohere (private)"),
    "amazon": ("Amazon (Nova)", "first-party", "AMZN"),
    "microsoft": ("Microsoft (Phi)", "open-weight", "MSFT"),
    "perplexity": ("Perplexity", "first-party", "Perplexity (private)"),
}


def lab_meta(author):
    a = (author or "").lower()
    return LAB.get(a, (author or "unknown", "open-weight", ""))


def latest_dir():
    p = OR / "latest.txt"
    if p.is_file():
        d = OR / "raw" / p.read_text(encoding="utf-8").strip()
        if d.is_dir():
            return d
    dirs = sorted((OR / "raw").glob("20*-*-*"))
    if not dirs:
        raise SystemExit("no snapshot found — run or_fetch.py first")
    return dirs[-1]


def loadj(d, name):
    return json.loads((d / (name + ".json")).read_text(encoding="utf-8"))


def f(x, default=0.0):
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def stripv(s):
    return re.sub(r"-\d{8}$", "", re.sub(r"-\d{4}-\d{2}-\d{2}$", "", s or ""))


def build():
    snap = latest_dir()
    asof = snap.name
    models = loadj(snap, "models")["data"]
    catalog = loadj(snap, "catalog")["data"]
    wk = loadj(snap, "rank_week")["data"]
    mo = loadj(snap, "rank_month")["data"]
    apps_raw = loadj(snap, "apps")["data"]

    # price index: prompt / completion / cache_read (raw; 0 => no separate cache price)
    price = {}
    for m in models:
        p = m.get("pricing") or {}
        rec = {"prompt": f(p.get("prompt")), "completion": f(p.get("completion")),
               "cache_read": f(p.get("input_cache_read"))}
        for k in (m.get("id"), m.get("canonical_slug"), stripv(m.get("canonical_slug"))):
            if k:
                price.setdefault(k, rec)

    cat = {}
    for c in catalog:
        outs = c.get("output_modalities") or []
        rec = {"author": c.get("author") or c.get("author_display_name"),
               "name": c.get("short_name") or c.get("name"),
               "is_text": ("text" in outs) if outs else True}
        for k in (c.get("permaslug"), c.get("slug")):
            if k:
                cat.setdefault(k, rec)

    def price_for(ps):
        return price.get(ps) or price.get(stripv(ps))

    def latest_rows(rows):
        last = max(r["date"] for r in rows)
        return [r for r in rows if r["date"] == last]

    def rev_at(prompt, comp, pr, cache_frac):
        """$ at list, with cache_frac of INPUT priced at the model's cache-read rate."""
        if pr is None:
            return 0.0
        cr = pr["cache_read"] if pr["cache_read"] > 0 else pr["prompt"]
        in_price = (1 - cache_frac) * pr["prompt"] + cache_frac * cr
        return prompt * in_price + comp * pr["completion"]

    def digest(rows):
        by_model = {}
        st = defaultdict(float)
        for r in rows:
            ps = r["model_permaslug"]; var = r.get("variant", "standard")
            prompt = f(r.get("total_prompt_tokens")); comp = f(r.get("total_completion_tokens"))
            tok = prompt + comp; reqs = f(r.get("count"))
            st["total_tok"] += tok
            c = cat.get(ps) or cat.get(stripv(ps))
            if c and not c["is_text"]:
                st["nontext_tok"] += tok
                continue
            pr = price_for(ps)
            is_free = (var == "free")
            r0 = 0.0 if is_free else rev_at(prompt, comp, pr, 0.0)
            r50 = 0.0 if is_free else rev_at(prompt, comp, pr, 0.5)
            r70 = 0.0 if is_free else rev_at(prompt, comp, pr, 0.7)
            paid = (not is_free) and (r0 > 0)
            if pr is None and not is_free:
                st["unpriced_tok"] += tok
            else:
                st["priced_tok"] += tok
            if is_free:
                st["free_tok"] += tok
            if paid:
                st["paid_tok"] += tok
            st["prompt_tok"] += prompt; st["comp_tok"] += comp; st["reqs"] += reqs
            author = (c["author"] if c else ps.split("/")[0])
            d = by_model.setdefault(ps, {"permaslug": ps, "author": author,
                                         "name": (c["name"] if c else ps.split("/")[-1]),
                                         "tokens": 0.0, "paid_tokens": 0.0, "prompt": 0.0,
                                         "comp": 0.0, "reqs": 0.0, "r0": 0.0, "r50": 0.0, "r70": 0.0})
            d["tokens"] += tok; d["prompt"] += prompt; d["comp"] += comp; d["reqs"] += reqs
            d["r0"] += r0; d["r50"] += r50; d["r70"] += r70
            if paid:
                d["paid_tokens"] += tok
        return by_model, st

    wk_models, wk_st = digest(latest_rows(wk))
    mo_models, _ = digest(latest_rows(mo))

    def agg_lab(md):
        a = defaultdict(lambda: defaultdict(float))
        for d in md.values():
            k = (d["author"] or "unknown").lower()
            for fld in ("tokens", "paid_tokens", "prompt", "comp", "reqs", "r0", "r50", "r70"):
                a[k][fld] += d[fld]
        return a

    wk_lab = agg_lab(wk_models); mo_lab = agg_lab(mo_models)
    tot_tok = sum(v["tokens"] for v in wk_lab.values()) or 1.0
    tot_paid = sum(v["paid_tokens"] for v in wk_lab.values()) or 1.0
    tot_rev = sum(v["r0"] for v in wk_lab.values()) or 1.0
    tot_reqs = sum(v["reqs"] for v in wk_lab.values()) or 1.0

    arr = json.loads((OR / "arr.json").read_text(encoding="utf-8"))
    arr_labs = arr.get("labs", {}); orr = arr.get("openrouter", {})

    def ann(x):
        return x / 7.0 * 365.0

    labs = []
    for author, v in wk_lab.items():
        disp, cap, parent = lab_meta(author)
        tok_wk = v["tokens"]; rev_wk = v["r0"]
        tok_mo = mo_lab.get(author, {}).get("tokens", 0.0)
        mom = ((tok_wk / 7.0) / (tok_mo / 30.0) - 1.0) if tok_mo > 0 else None
        arr_rec = arr_labs.get(author, {}); arr_b = arr_rec.get("arr_busd")
        rev_ann = ann(rev_wk)
        labs.append({
            "author": author, "display": disp, "capture": cap, "parent": parent,
            "tokens_week": tok_wk, "tokens_month": tok_mo, "paid_tokens_week": v["paid_tokens"],
            "daily_tokens": tok_wk / 7.0, "requests_week": v["reqs"],
            "token_share": tok_wk / tot_tok, "paid_token_share": v["paid_tokens"] / tot_paid,
            "req_share": v["reqs"] / tot_reqs,
            "revenue_week": rev_wk, "revenue_annualized": rev_ann, "rev_share": rev_wk / tot_rev,
            "revenue_annualized_cache50": ann(v["r50"]), "revenue_annualized_cache70": ann(v["r70"]),
            "blended_price_per_mtok": (rev_wk / tok_wk * 1e6) if tok_wk else 0.0,
            "input_ratio": (v["prompt"] / v["comp"]) if v["comp"] else None,
            "tokens_per_req": (tok_wk / v["reqs"]) if v["reqs"] else 0.0,
            "dollars_per_mreq": (rev_wk / v["reqs"] * 1e6) if v["reqs"] else 0.0,
            "momentum": mom,
            "arr_busd": arr_b, "arr_tag": arr_rec.get("tag"), "arr_asof": arr_rec.get("asof"),
            "arr_source": arr_rec.get("source"),
            "or_pct_of_arr": (rev_ann / 1e9 / arr_b * 100.0) if arr_b else None,
        })
    labs.sort(key=lambda x: -x["revenue_annualized"])

    models_out = []
    for d in wk_models.values():
        disp, cap, parent = lab_meta(d["author"])
        tok = d["tokens"]
        models_out.append({
            "permaslug": d["permaslug"], "name": d["name"], "lab": disp, "capture": cap,
            "tokens_week": tok, "daily_tokens": tok / 7.0, "requests_week": d["reqs"],
            "revenue_week": d["r0"], "revenue_annualized": ann(d["r0"]),
            "blended_price_per_mtok": (d["r0"] / tok * 1e6) if tok else 0.0,
            "input_ratio": (d["prompt"] / d["comp"]) if d["comp"] else None,
        })
    models_out.sort(key=lambda x: -x["revenue_annualized"])

    apps = []
    for a in apps_raw.get("week", []):
        app = a.get("app", {})
        apps.append({"title": app.get("title"), "url": app.get("origin_url"),
                     "categories": app.get("categories", []),
                     "tokens_week": f(a.get("total_tokens")), "requests_week": f(a.get("total_requests")),
                     "rank": a.get("rank")})
    apps.sort(key=lambda x: -x["tokens_week"])

    # platform + guardrails
    # text tokens = everything minus non-text; free rows already sit inside priced_tok,
    # so derive the total from (all - nontext) to avoid double-counting the free subset.
    plat_text_tok = wk_st["total_tok"] - wk_st["nontext_tok"]
    tokens_month = plat_text_tok / 7.0 * 30.0
    rev_month = tot_rev / 7.0 * 30.0
    rev_month_c50 = sum(v["r50"] for v in wk_lab.values()) / 7.0 * 30.0
    rev_month_c70 = sum(v["r70"] for v in wk_lab.values()) / 7.0 * 30.0
    coverage = wk_st["priced_tok"] / (wk_st["priced_tok"] + wk_st["unpriced_tok"]) if (wk_st["priced_tok"] + wk_st["unpriced_tok"]) else 0
    input_ratio = wk_st["prompt_tok"] / wk_st["comp_tok"] if wk_st["comp_tok"] else 0

    spend_jun = orr.get("reported_monthly_spend_musd")      # ~76 (Jun-26 actual)
    or_rev_ann = orr.get("reported_or_revenue_annualized_musd")  # ~50 (Mar-26)
    take = (orr.get("take_rate_pct") or 5) / 100.0
    spend_mar = (or_rev_ann / take / 12.0) if or_rev_ann else None  # ~83M/mo implied Mar
    spendM = rev_month / 1e6
    ratio = spendM / spend_jun if spend_jun else None

    G = {}
    G["priced_token_coverage"] = ("PASS" if coverage >= 0.90 else "WARN", "%.2f%% of text tokens priced" % (coverage * 100))
    G["platform_tokens_vs_anchor"] = ("INFO", "computed ~%.0fT tok/mo vs OR-reported ~%sT/mo (%s); tokens ~2.7x since => on-trend" % (tokens_month / 1e12, orr.get("reported_tokens_per_month_T"), orr.get("tokens_asof")))
    G["implied_$_is_a_CEILING"] = ("WARN", "list & cache-OFF: $%.0fM/mo vs OR actual ~$%sM/mo (%s) = %.1fx. OR spend was ~FLAT Mar~$%.0fM->Jun$%sM, so the gap is list-vs-realized (caching-off + provider discounting), NOT growth." % (spendM, spend_jun, orr.get("spend_asof"), ratio or 0, (spend_mar or 0), spend_jun))
    G["cache_sensitivity"] = ("INFO", "if 50/70%% of input were cache-reads: $%.0fM/$%.0fM per mo (vs $%.0fM at cache-off)" % (rev_month_c50 / 1e6, rev_month_c70 / 1e6, spendM))
    G["input_heaviness"] = ("INFO", "platform prompt:completion = %.1f:1 (%.0f%% input tokens) => $ is an INPUT-price construct" % (input_ratio, wk_st["prompt_tok"] / plat_text_tok * 100 if plat_text_tok else 0))
    G["free_token_share"] = ("INFO", "%.1f%% of text tokens are $0 free-variant (padding the token base; use paid-token share to compare $)" % (wk_st["free_tok"] / plat_text_tok * 100 if plat_text_tok else 0))
    G["nontext_excluded"] = ("INFO", "%.2f%% of all tokens excluded as non-text (image/audio/embed)" % (wk_st["nontext_tok"] / wk_st["total_tok"] * 100 if wk_st["total_tok"] else 0))

    out = {
        "asof": asof, "generated": dt.datetime.now().isoformat(timespec="seconds"),
        "platform": {
            "tokens_week": plat_text_tok, "tokens_month_run_rate": tokens_month, "daily_tokens": plat_text_tok / 7.0,
            "paid_tokens_week": wk_st["paid_tok"], "requests_week": wk_st["reqs"],
            "revenue_week": tot_rev, "revenue_month_run_rate": rev_month, "revenue_annualized": ann(tot_rev),
            "revenue_month_cache50": rev_month_c50, "revenue_month_cache70": rev_month_c70,
            "priced_coverage": coverage, "input_ratio": input_ratio,
            "free_token_pct": wk_st["free_tok"] / plat_text_tok if plat_text_tok else 0,
            "blended_price_per_mtok": tot_rev / plat_text_tok * 1e6 if plat_text_tok else 0,
        },
        "anchors": orr, "anchor_spend_mar_musd": spend_mar,
        "guardrails": G, "labs": labs, "models": models_out[:40], "apps": apps[:20],
    }
    (OR / "dashboard.json").write_text(json.dumps(out, indent=1), encoding="utf-8")

    hist = {"date": asof, "tokens_week": plat_text_tok, "revenue_annualized": ann(tot_rev),
            "labs": {l["author"]: {"tok_wk": l["tokens_week"], "paid_wk": l["paid_tokens_week"],
                                   "rev_ann": l["revenue_annualized"]} for l in labs[:15]}}
    with (OR / "history.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(hist) + "\n")

    # console report
    print("=" * 78)
    print("OpenRouter AI-lab traction — as of", asof)
    print("=" * 78)
    print("PLATFORM  %.1f T tok/day (~%.0f T/mo)  |  implied list/cache-OFF spend ~$%.0f M/mo (~$%.2f B/yr) = CEILING"
          % (plat_text_tok / 7 / 1e12, tokens_month / 1e12, spendM, ann(tot_rev) / 1e9))
    print("          prompt:completion %.1f:1 | free tokens %.0f%% | blended $%.3f/Mtok | coverage %.1f%%"
          % (input_ratio, out["platform"]["free_token_pct"] * 100, out["platform"]["blended_price_per_mtok"], coverage * 100))
    print("\nGUARDRAILS")
    for k, (stt, msg) in G.items():
        print("  [%-4s] %-24s %s" % (stt, k, msg))
    print("\nTOP LABS  (lead with RANK; $ is a ceiling)")
    print("  %-20s %7s %7s %7s %7s %7s %7s %6s  %s" % ("lab", "$B/yr", "tok%", "paid%", "req%", "$/Mtok", "in:out", "mom", "capture"))
    for l in labs[:14]:
        print("  %-20s %7.2f %6.1f%% %6.1f%% %6.1f%% %7.3f %6s %6s  %s" % (
            l["display"][:20], l["revenue_annualized"] / 1e9, l["token_share"] * 100, l["paid_token_share"] * 100,
            l["req_share"] * 100, l["blended_price_per_mtok"],
            ("%.0f:1" % l["input_ratio"]) if l["input_ratio"] else "n/a",
            ("%+.0f%%" % (l["momentum"] * 100)) if l["momentum"] is not None else "n/a", l["capture"]))
    print("\nwrote", OR / "dashboard.json")
    return out


if __name__ == "__main__":
    build()
