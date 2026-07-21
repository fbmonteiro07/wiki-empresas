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

    cat_ci = {str(k).lower(): v for k, v in cat.items()}
    cat_tail = {}
    for k, v in cat_ci.items():
        tail = k.rsplit("/", 1)[-1]
        if tail not in cat_tail:
            cat_tail[tail] = v
        elif cat_tail[tail] != v:
            cat_tail[tail] = None  # ambiguous basename: never guess

    def cat_for(ps):
        key = str(ps).lower()
        stripped = stripv(ps).lower()
        return (
            cat.get(ps) or cat.get(stripv(ps))
            or cat_ci.get(key) or cat_ci.get(stripped)
            or cat_tail.get(key.rsplit("/", 1)[-1])
            or cat_tail.get(stripped.rsplit("/", 1)[-1])
        )

    def price_for(ps):
        return price.get(ps) or price.get(stripv(ps))

    def latest_rows(rows):
        last = max(r["date"] for r in rows)
        return [r for r in rows if r["date"] == last]

    def catalog_misses(rows):
        """Every unmatched model/variant is surfaced by the platform guardrail."""
        return sorted({
            "%s|%s" % (r["model_permaslug"], r.get("variant", "standard"))
            for r in rows if cat_for(r["model_permaslug"]) is None
        })

    def rev_at(prompt, comp, pr, cache_frac):
        """$ at list, with cache_frac of INPUT priced at the model's cache-read rate."""
        if pr is None:
            return 0.0
        cr = pr["cache_read"] if pr["cache_read"] > 0 else pr["prompt"]
        in_price = (1 - cache_frac) * pr["prompt"] + cache_frac * cr
        return prompt * in_price + comp * pr["completion"]

    def digest(rows, normalized_catalog=False):
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

    # Lab/model tables use a matched latest-date cohort; platform totals use
    # every observed row in each OpenRouter window.
    wk_models, _ = digest(latest_rows(wk))
    mo_models, _ = digest(latest_rows(mo))
    _, wk_st = digest(wk, normalized_catalog=True)
    _, mo_st = digest(mo, normalized_catalog=True)

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
        pr = price_for(d["permaslug"]) or {}
        models_out.append({
            "permaslug": d["permaslug"], "name": d["name"], "lab": disp, "capture": cap,
            "tokens_week": tok, "daily_tokens": tok / 7.0, "requests_week": d["reqs"],
            "revenue_week": d["r0"], "revenue_annualized": ann(d["r0"]),
            "price_in_mtok": pr.get("prompt", 0.0) * 1e6, "price_out_mtok": pr.get("completion", 0.0) * 1e6,
            "cache_read_mtok": pr.get("cache_read", 0.0) * 1e6,
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
    plat_text_tok_7d_all = plat_text_tok
    plat_text_tok_30d = mo_st["total_tok"] - mo_st["nontext_tok"]
    wk_cutoff = max((r["date"] for r in wk), default="")
    mo_cutoff = max((r["date"] for r in mo), default="")
    wk_unmatched = catalog_misses(wk)
    mo_unmatched = catalog_misses(mo)
    token_momentum_weekly = (
        (plat_text_tok_7d_all / 7.0) / (plat_text_tok_30d / 30.0) - 1.0
        if plat_text_tok_30d > 0 else None
    )
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
    weekly_basis_ok = (
        plat_text_tok_7d_all > 0
        and plat_text_tok_30d >= plat_text_tok_7d_all
        and wk_cutoff == mo_cutoff
        and not wk_unmatched
        and not mo_unmatched
    )
    momentum_text = ("%+.1f%%" % (token_momentum_weekly * 100)) if token_momentum_weekly is not None else "n/a"
    G["weekly_token_momentum_basis"] = (
        "PASS" if weekly_basis_ok else "WARN",
        "OpenRouter all-row observed 7d %.1fT vs 30d %.1fT text tokens (same cutoff %s; unmatched catalog rows 7d=%d, 30d=%d); 7d-vs-30d momentum = (7d/7) / (30d/30) - 1 = %s. Overlapping windows, not strict WoW."
        % (plat_text_tok_7d_all / 1e12, plat_text_tok_30d / 1e12, wk_cutoff or "n/a", len(wk_unmatched), len(mo_unmatched), momentum_text)
    )
    G["implied_$_is_a_CEILING"] = ("WARN", "list & cache-OFF: $%.0fM/mo vs OR actual ~$%sM/mo (%s) = %.1fx. OR spend was ~FLAT Mar~$%.0fM->Jun$%sM, so the gap is list-vs-realized (caching-off + provider discounting), NOT growth." % (spendM, spend_jun, orr.get("spend_asof"), ratio or 0, (spend_mar or 0), spend_jun))
    G["cache_sensitivity"] = ("INFO", "if 50/70%% of input were cache-reads: $%.0fM/$%.0fM per mo (vs $%.0fM at cache-off)" % (rev_month_c50 / 1e6, rev_month_c70 / 1e6, spendM))
    G["input_heaviness"] = ("INFO", "platform prompt:completion = %.1f:1 (%.0f%% input tokens) => $ is an INPUT-price construct" % (input_ratio, wk_st["prompt_tok"] / plat_text_tok * 100 if plat_text_tok else 0))
    G["free_token_share"] = ("INFO", "%.1f%% of text tokens are $0 free-variant (padding the token base; use paid-token share to compare $)" % (wk_st["free_tok"] / plat_text_tok * 100 if plat_text_tok else 0))
    G["nontext_excluded"] = ("INFO", "%.2f%% of all tokens excluded as non-text (image/audio/embed)" % (wk_st["nontext_tok"] / wk_st["total_tok"] * 100 if wk_st["total_tok"] else 0))

    # ---- neocloud / per-provider prices from the endpoints watchlist ----
    # Who serves each model and at what price: maker's own API vs neoclouds
    # (Together/Fireworks/DeepInfra/...) vs hyperscalers appearing as hosts.
    MAKER_PROVIDER = {"deepseek": "DeepSeek", "z-ai": "Z.AI", "minimax": "Minimax",
                      "moonshotai": "Moonshot AI", "mistralai": "Mistral",
                      "anthropic": "Anthropic", "openai": "OpenAI"}
    neoclouds = []
    epf = snap / "endpoints.json"
    if epf.is_file():
        try:
            epdata = json.loads(epf.read_text(encoding="utf-8"))
        except ValueError:
            epdata = {}
        for slug, d in epdata.items():
            eps = d.get("endpoints") or []
            provs = []
            for e in eps:
                p = e.get("pricing") or {}
                pin = f(p.get("prompt")) * 1e6
                pout = f(p.get("completion")) * 1e6
                if pin <= 0 and pout <= 0:
                    continue
                provs.append({"provider": e.get("provider_name") or "?", "in": pin, "out": pout,
                              "quant": e.get("quantization") or "", "ctx": e.get("context_length")})
            if not provs:
                continue
            provs.sort(key=lambda x: x["in"])
            author = slug.split("/")[0]
            maker_name = MAKER_PROVIDER.get(author)
            maker = next((x for x in provs if x["provider"] == maker_name), None)
            c = cat.get(slug) or cat.get(stripv(slug))
            disp, capk, _ = lab_meta(author)
            neoclouds.append({
                "slug": slug, "name": (c["name"] if c else slug.split("/")[-1]), "lab": disp,
                "klass": ("first-party" if capk == "first-party" else "open"),
                "maker": maker, "cheapest": provs[0],
                "together": next((x for x in provs if x["provider"] == "Together"), None),
                "fireworks": next((x for x in provs if x["provider"] == "Fireworks"), None),
                "deepinfra": next((x for x in provs if x["provider"] == "DeepInfra"), None),
                "google": next((x for x in provs if x["provider"] == "Google"), None),
                "bedrock": next((x for x in provs if x["provider"] == "Amazon Bedrock"), None),
                "azure": next((x for x in provs if x["provider"] == "Azure"), None),
                "n_providers": len(provs),
                "spread_in": (provs[-1]["in"] / provs[0]["in"]) if provs[0]["in"] > 0 else None,
            })

    # ---- new models vs previous snapshot (launch tracking) ----
    new_models = []
    raw_dirs = sorted((OR / "raw").glob("20*-*-*"))
    if len(raw_dirs) >= 2:
        try:
            prev_wk = json.loads((raw_dirs[-2] / "rank_week.json").read_text(encoding="utf-8"))["data"]
            prev_slugs = {r["model_permaslug"] for r in prev_wk}
            cur = {}
            for r in latest_rows(wk):
                if r["model_permaslug"] not in prev_slugs:
                    cur[r["model_permaslug"]] = cur.get(r["model_permaslug"], 0.0) + f(r.get("total_prompt_tokens")) + f(r.get("total_completion_tokens"))
            for ps, tokv in sorted(cur.items(), key=lambda kv: -kv[1])[:10]:
                c = cat.get(ps) or cat.get(stripv(ps))
                disp, _, _ = lab_meta(c["author"] if c else ps.split("/")[0])
                new_models.append({"permaslug": ps, "name": (c["name"] if c else ps.split("/")[-1]),
                                   "lab": disp, "tokens_week": tokv, "since": raw_dirs[-2].name})
        except Exception:
            pass

    # ---- product mix (what the system runs) ----
    lr = latest_rows(wk)
    by_mod = defaultdict(float)
    for r in lr:
        ps = r["model_permaslug"]
        t = f(r.get("total_prompt_tokens")) + f(r.get("total_completion_tokens"))
        c = cat.get(ps) or cat.get(stripv(ps))
        outs = None
        for cc in catalog:
            if cc.get("permaslug") == ps or cc.get("slug") == ps:
                outs = cc.get("output_modalities"); break
        outs = outs or (["text"] if (c is None or c["is_text"]) else [])
        bucket = "text" if "text" in outs else ("image" if "image" in outs else ("audio" if "audio" in outs else "embedding/other"))
        by_mod[bucket] += t
    mod_total = sum(by_mod.values()) or 1.0

    def workload_bucket(cats):
        s = " ".join(cats).lower()
        if any(k in s for k in ["roleplay", "companion", "character", "creative", "story", "game"]):
            return "Roleplay / creative"
        if any(k in s for k in ["cod", "program", "cli-agent", "ide", "agent", "app-builder", "dev"]):
            return "Coding / agentic"
        if any(k in s for k in ["chat", "assistant", "search", "writing", "productivity", "general"]):
            return "Chat / assistant"
        return "Other / unlabeled"

    by_wl = defaultdict(float)
    appsum = 0.0
    for a in apps:
        b = workload_bucket(a.get("categories", []))
        by_wl[b] += a["tokens_week"]; appsum += a["tokens_week"]
    appsum = appsum or 1.0

    product_mix = {
        "input_pct": wk_st["prompt_tok"] / (wk_st["prompt_tok"] + wk_st["comp_tok"]) if wk_st["comp_tok"] else 0,
        "output_pct": wk_st["comp_tok"] / (wk_st["prompt_tok"] + wk_st["comp_tok"]) if wk_st["comp_tok"] else 0,
        "ratio": input_ratio,
        "modality": [{"name": k, "pct": v / mod_total} for k, v in sorted(by_mod.items(), key=lambda kv: -kv[1])],
        "workload": [{"name": k, "pct": v / appsum} for k, v in sorted(by_wl.items(), key=lambda kv: -kv[1])],
        "workload_coverage_pct": appsum / plat_text_tok if plat_text_tok else 0,
    }

    # ---- total-system growth (external anchors + our computed run-rate) ----
    sg = {}
    sgp = OR / "system_growth.json"
    if sgp.is_file():
        sg = json.loads(sgp.read_text(encoding="utf-8"))
    tok_series = {}
    for p in sg.get("token_points", []):
        if p.get("plot"):
            tok_series[p["date"]] = p["tokens_mo_T"]
    if hp_prior := (OR / "history.jsonl"):
        if hp_prior.is_file():
            for ln in hp_prior.read_text(encoding="utf-8").splitlines():
                ln = ln.strip()
                if ln:
                    try:
                        rec = json.loads(ln)
                        tok_series[rec["date"]] = rec["tokens_week"] / 7.0 * 30.0 / 1e12
                    except (ValueError, KeyError):
                        pass
    tok_series[asof] = tokens_month / 1e12
    blend_today = (tot_rev / plat_text_tok * 1e6) if plat_text_tok else 0.0  # $/Mtok, current model blend (list)
    token_series_list = [{"date": d, "tokens_mo_T": tok_series[d]} for d in sorted(tok_series)]
    system_growth = {
        "token_series": token_series_list,
        # "total cost growth" = each period's tokens priced at TODAY's model blend (counterfactual;
        # isolates the volume effect). Realized spend (spend_points) is the flat reference.
        "blend_per_mtok": blend_today,
        "cost_series": [{"date": p["date"], "cost_mo_musd": p["tokens_mo_T"] * blend_today,
                         "cost_yr_busd": p["tokens_mo_T"] * blend_today * 12 / 1e3} for p in token_series_list],
        "spend_points": sg.get("spend_points", []),
        "run_rate_quad_yr": tokens_month * 12 / 1e15,
        "token_points_meta": sg.get("token_points", []),
    }

    out = {
        "asof": asof, "generated": dt.datetime.now().isoformat(timespec="seconds"),
        "new_models": new_models, "neoclouds": neoclouds,
        "product_mix": product_mix, "system_growth": system_growth,
        "platform": {
            "tokens_week": plat_text_tok, "tokens_month_run_rate": tokens_month, "daily_tokens": plat_text_tok / 7.0,
            "tokens_7d_observed": plat_text_tok_7d_all, "tokens_30d_observed": plat_text_tok_30d, "token_momentum_weekly": token_momentum_weekly,
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

    # history: one line per date (dedupe keep-last, so intraday re-runs don't pollute the trend)
    hist = {"date": asof, "tokens_week": plat_text_tok, "token_momentum_weekly": token_momentum_weekly, "revenue_annualized": ann(tot_rev),
            "labs": {l["author"]: {"tok_wk": l["tokens_week"], "paid_wk": l["paid_tokens_week"],
                                   "rev_ann": l["revenue_annualized"]} for l in labs[:15]}}
    hp = OR / "history.jsonl"
    by_date = {}
    if hp.is_file():
        for ln in hp.read_text(encoding="utf-8").splitlines():
            ln = ln.strip()
            if ln:
                try:
                    rec = json.loads(ln)
                    by_date[rec.get("date")] = rec
                except ValueError:
                    pass
    by_date[asof] = hist
    hp.write_text("".join(json.dumps(by_date[d]) + "\n" for d in sorted(by_date)), encoding="utf-8")

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
