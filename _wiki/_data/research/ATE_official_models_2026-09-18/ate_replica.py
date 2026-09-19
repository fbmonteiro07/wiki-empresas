# -*- coding: utf-8 -*-
"""Independent Python replica of 'Capa DCF - Base' for the two ATE workbooks.
Reads the INPUTS back from the built workbook's 'Premissas e fontes' (values; the handful of calibration formulas are
evaluated by a tiny arithmetic evaluator), recomputes the whole Capa, and (after Excel COM recalculation) compares the
Excel-cached values with the replica at named checkpoints."""
import re, json, os, datetime as dt
import openpyxl

YEARS = list(range(2023, 2046))
COLS = [openpyxl.utils.get_column_letter(4 + i) for i in range(len(YEARS))]
BASE = {2023, 2024, 2025}
CELL = re.compile(r"\$?([A-Z]{1,2})\$?(\d+)")


def load_prem(path, R):
    wb = openpyxl.load_workbook(path, data_only=False)
    ws = wb["Premissas e fontes"]
    cache = {}

    def val(addr):
        if addr in cache: return cache[addr]
        v = ws[addr].value
        if isinstance(v, str) and v.startswith("="):
            expr = v[1:]
            expr = CELL.sub(lambda m: repr(val(f"{m.group(1)}{m.group(2)}")), expr)
            v = eval(expr, {"__builtins__": {}}, {})
        cache[addr] = v
        return v

    def row(key, years=YEARS):
        r = R[key]; out = {}
        for i, y in enumerate(years):
            c = COLS[i] if years is YEARS else COLS[years.index(y)]
            v = val(f"{c}{r}")
            if v is not None: out[y] = v
        return out

    def single(key):
        return val(f"D{R[key]}")
    return row, single


def frac_after(vd, y):
    end = dt.date(y, 12, 31); start = dt.date(y, 1, 1)
    return max(0.0, min(1.0, (end - vd).days / ((end - start).days + 1)))


def t_years(vd, y):
    return max(0.0, (dt.date(y, 12, 31) - vd).days / 365)


def replica(path, ticker, R):
    row, single = load_prem(path, R)
    ref_years = list(range(2023, 2029))
    out = {y: {} for y in YEARS}
    wfe_in = row("wfe"); wfe_g = row("wfe_g"); ratio = row("ratio")
    tam_ref = row("tam_ref", ref_years) if False else None
    # tam_ref lives in the reference table (D..I = 2023..2028)
    wb = openpyxl.load_workbook(path, data_only=False); ws = wb["Premissas e fontes"]
    def refrow(key):
        r = R[key]; d = {}
        for i, y in enumerate(ref_years):
            v = ws[f"{COLS[i]}{r}"].value
            if v is not None: d[y] = v
        return d
    tam_ref = refrow("tam_ref")
    wfe = {}
    for y in YEARS:
        wfe[y] = wfe_in[y] if y in wfe_in else wfe[y - 1] * (1 + wfe_g[y])
        out[y]["wfe"] = wfe[y]
    for y in YEARS:
        out[y]["ratio"] = ratio[y]; out[y]["tam"] = wfe[y] * ratio[y]
    vd = single("val_date"); vd = vd.date() if isinstance(vd, dt.datetime) else vd
    wacc, g, roic = single("wacc"), single("g"), single("roic")
    shares = single("shares")
    if ticker == "ADV":
        soc_mix = row("soc_mix"); fx = row("fx"); adv_soc = row("adv_soc"); adv_mem = row("adv_mem"); oth = row("oth_ratio"); so = row("so_ratio")
        rev_ref = refrow("rev_ref"); ts_mix = refrow("ts_mix"); soc_in = refrow("soc_in_ts"); mem_in = refrow("mem_in_ts"); oth_in = refrow("oth_in_ts")
        for y in YEARS:
            o = out[y]; o["tam_soc"] = o["tam"] * soc_mix[y]; o["tam_mem"] = o["tam"] - o["tam_soc"]; o["fx"] = fx[y]
            if y in BASE:
                ts = rev_ref[y] * ts_mix[y]
                o["soc"] = ts * soc_in[y]; o["mem"] = ts * mem_in[y]; o["oth"] = ts * oth_in[y]; o["so"] = rev_ref[y] * (1 - ts_mix[y])
                o["soc_us"] = o["soc"] / fx[y]; o["mem_us"] = o["mem"] / fx[y]
            else:
                o["soc_us"] = o["tam_soc"] * adv_soc[y] * 1000; o["mem_us"] = o["tam_mem"] * adv_mem[y] * 1000
                o["soc"] = o["soc_us"] * fx[y]; o["mem"] = o["mem_us"] * fx[y]; o["oth"] = (o["soc"] + o["mem"]) * oth[y]
                o["so"] = (o["soc"] + o["mem"] + o["oth"]) * so[y]
            o["ts"] = o["soc"] + o["mem"] + o["oth"]; o["rev"] = o["ts"] + o["so"]
    else:
        share = row("share"); ptg = row("pt_g"); robg = row("rob_g")
        semi = refrow("semi"); pt = refrow("pt"); rob = refrow("rob")
        for y in YEARS:
            o = out[y]
            if y in BASE:
                o["semi"], o["pt"], o["rob"] = semi[y], pt[y], rob[y]
            else:
                o["semi"] = o["tam"] * share[y] * 1000; o["pt"] = out[y - 1]["pt"] * (1 + ptg[y]); o["rob"] = out[y - 1]["rob"] * (1 + robg[y])
            o["rev"] = o["semi"] + o["pt"] + o["rob"]
    gm = row("gm"); opex = row("opex"); sbc = row("sbc"); tax = row("tax"); da = row("da"); capex = row("capex"); nwc = row("nwc")
    for y in YEARS:
        o = out[y]; r = o["rev"]
        o["gp"] = r * gm[y]; o["ebit"] = o["gp"] - r * opex[y] - r * sbc[y]; o["ebitm"] = o["ebit"] / r
        o["tax"] = tax[y]; o["nopat"] = o["ebit"] * (1 - tax[y]); o["da"] = r * da[y]; o["capex"] = -r * capex[y]
        o["nwc"] = r * nwc[y] if y >= 2025 else None
        o["dnwc"] = -(o["nwc"] - out[y - 1]["nwc"]) if y >= 2026 else None
        o["fcff"] = o["nopat"] + o["da"] + o["capex"] + o["dnwc"] if y >= 2026 else None
        o["t"] = t_years(vd, y); o["frac"] = frac_after(vd, y)
        o["fcffv"] = (o["fcff"] * o["frac"]) if y >= 2026 else 0.0
        o["pv"] = o["fcffv"] / (1 + wacc) ** o["t"]
    pvx = sum(out[y]["pv"] for y in YEARS if y >= 2026)
    nopat_t = out[2045]["nopat"] * (1 + g); reinv = nopat_t * g / roic; fcff_t = nopat_t - reinv
    tv = fcff_t / (wacc - g); pvtv = tv / (1 + wacc) ** out[2045]["t"]; ev = pvx + pvtv
    extra = single("invsec") if ticker == "ADV" else single("technoprobe")
    netdebt = single("debt") - single("cash") - extra
    equity = ev - netdebt; ps = equity / shares
    val = dict(pvx=pvx, nopat_t=nopat_t, tv=tv, pvtv=pvtv, ev=ev, netdebt=netdebt, equity=equity, ps=ps, tvshare=pvtv / ev, ps_nt=(pvx - netdebt) / shares)
    # wiki block
    fin = row("fin"); sh = row("sh")
    if ticker == "ADV":
        for y in YEARS:
            if y >= 2026:
                o = out[y]; o["ni"] = (o["ebit"] + fin[y]) * (1 - tax[y]); o["eps"] = o["ni"] / sh[y]
                o["fcfe"] = o["ni"] + o["da"] - (-o["rev"] * sbc[y]) + o["dnwc"] + o["capex"]
    else:
        affil = row("affil")
        for y in YEARS:
            if y >= 2026:
                o = out[y]; o["ni"] = (o["ebit"] + fin[y]) * (1 - tax[y]) + affil[y]; o["eps"] = o["ni"] / sh[y]
                o["fcfe"] = o["ni"] + o["da"] - (-o["rev"] * sbc[y]) + o["dnwc"] + o["capex"]
    return out, val


def compare(path, ticker, layout):
    """Compare Excel-cached values (after COM recalc) with the replica at checkpoints. Returns list of (name, excel, replica, ok)."""
    R = layout["R"]; pl = layout["pl"]; val = layout["val"]; wiki = layout["wiki"]
    out, v = replica(path, ticker, R)
    wb = openpyxl.load_workbook(path, data_only=True); ws = wb["Capa DCF - Base"]
    rev_row = 32 if ticker == "ADV" else 22
    res = []
    def chk(name, addr, rep, tol=1e-6):
        x = ws[addr].value
        ok = (x is not None) and abs(x - rep) <= tol * max(1.0, abs(rep))
        res.append((name, addr, x, rep, ok))
    for y in (2024, 2025, 2026, 2027, 2028, 2035, 2045):
        c = COLS[YEARS.index(y)]
        chk(f"rev {y}", f"{c}{rev_row}", out[y]["rev"])
        chk(f"ebit {y}", f"{c}{pl['ebit']}", out[y]["ebit"])
        if y >= 2026:
            chk(f"fcff {y}", f"{c}{pl['fcff']}", out[y]["fcff"])
            if y <= 2028:
                chk(f"eps {y}", f"{c}{wiki + 7}", out[y]["eps"])
    chk("pv explicit", f"D{val['pvx']}", v["pvx"]); chk("pv tv", f"D{val['pvtv']}", v["pvtv"]); chk("ev", f"D{val['ev']}", v["ev"])
    chk("equity", f"D{val['equity']}", v["equity"]); chk("per share", f"D{val['ps']}", v["ps"]); chk("tv/ev", f"D{val['tvshare']}", v["tvshare"])
    chk("grid centre", f"I{val['grid_center_row']}", v["ps"])
    return res, out, v


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    lay = json.load(open(os.path.join(here, "layout.json")))
    for tk, fn in (("ADV", "Template DCF ADVANTEST.xlsx"), ("TER", "Template DCF TER.xlsx")):
        L = lay["adv" if tk == "ADV" else "ter"]
        L["R"] = {k: int(v) for k, v in L["R"].items()}
        res, out, v = compare(os.path.join(here, fn), tk, L)
        bad = [r for r in res if not r[4]]
        print(f"== {tk}: {len(res)} checkpoints, {len(bad)} mismatches; per share replica = {v['ps']:,.2f}")
        for r in res:
            flag = "OK " if r[4] else "BAD"
            print(f"  {flag} {r[0]:14s} {r[1]:6s} excel={r[2]!s:>18} replica={r[3]:,.4f}")
