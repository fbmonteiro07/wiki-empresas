"""Date-aware observations shared by the credit dashboard and weekly brief."""
import datetime as dt
import math


def observations(series, asof=None):
    cutoff = (asof or dt.date.today()).isoformat()
    valid = {}
    for date, value in series.get('points', []):
        try:
            dt.date.fromisoformat(date)
            if date <= cutoff and math.isfinite(float(value)):
                valid[date] = float(value)
        except (ValueError, TypeError):
            continue
    return sorted(valid.items())


def change(series, days, asof=None):
    """Calendar lookback; retain actual dates and reject remote baselines."""
    pts = observations(series, asof)
    if not pts:
        return None
    end, last = pts[-1]
    target = dt.date.fromisoformat(end) - dt.timedelta(days=days)
    eligible = [(date, value) for date, value in pts if date <= target.isoformat()]
    if not eligible:
        return None
    start, previous = eligible[-1]
    if (target - dt.date.fromisoformat(start)).days > 4:
        return None
    unit = series.get('unit', '')
    scale = 100 if unit == '%' else 1
    return {'value': round((last - previous) * scale, 4),
            'unit': 'bp' if unit == '%' else unit, 'start': start, 'end': end}


def change_text(series, days, asof=None):
    value = change(series, days, asof)
    if value is None:
        return 'Unavailable — insufficient matching history'
    return f"{value['value']:+.1f} {value['unit']} ({value['start']} → {value['end']})"


def market_health(market, config, asof=None):
    today = asof or dt.date.today()
    required = config.get('market_series', []) + config.get('bonds', [])
    found = {(s['ticker'], s.get('field', 'PX_LAST')): s for s in market.get('series', [])}
    issues = list(market.get('errors', []))
    dates = []
    for item in required:
        key = (item['ticker'], item.get('field', 'PX_LAST'))
        pts = observations(found.get(key, {}), today)
        if not pts:
            issues.append(f'{key[0]}: no usable observations')
        else:
            date = pts[-1][0]
            dates.append(date)
            if (today - dt.date.fromisoformat(date)).days > 4:
                issues.append(f'{key[0]}: latest observation {date} is stale')
    return {'ok': bool(required) and not issues, 'issues': issues,
            'earliest': min(dates) if dates else 'unavailable',
            'latest': max(dates) if dates else 'unavailable'}
