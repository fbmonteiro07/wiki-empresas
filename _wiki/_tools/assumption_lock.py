#!/usr/bin/env python
"""
assumption_lock.py - freeze model assumptions BEFORE the model runs.

Why this exists
---------------
Two adversarial audits found the same failure: an assumption changed late in a
build, after the analyst saw an output he did not like. In the COHR v3 model the
TAM interior was raised 51% at the end of the build; it moved CY27 by -17.5% and
flipped the base case from a share DECLINE to a share HOLD without the share
number changing. It was documented in a code comment and still invisible in the
deliverable.

The problem is sequencing, not honesty. So make the sequence enforceable:
assumptions are hashed at first run; any later change fails the build unless it
carries an explicit reason, and every reason is appended to a revision log that
ships inside the workbook.

Usage
-----
    from assumption_lock import check_lock

    A = {"inp_growth_cq3_26": 1.00, "internal_share_exit": 0.75, ...}
    log = check_lock(A, "v4.lock.json", revise=args.revise)   # raises on silent drift
    # ... build, then write `log` into a Revisions tab

    py build_v4.py                          # first run: writes the lock
    py build_v4.py                          # unchanged: passes
    py build_v4.py                          # changed, no reason: FAILS loudly
    py build_v4.py --revise "raised InP exit rate to mgmt guided +100%, JPM 08-13"
"""
import hashlib, json
from datetime import datetime
from pathlib import Path


def _norm(a):
    """Stable representation so float noise and key order don't create false drift."""
    return json.dumps({k: (round(v, 10) if isinstance(v, float) else v)
                       for k, v in sorted(a.items())}, ensure_ascii=False)


def _hash(a):
    return hashlib.sha256(_norm(a).encode("utf-8")).hexdigest()[:16]


def check_lock(assumptions, lock_path, revise=None, quiet=False):
    """
    Compare `assumptions` to the lock. Returns the revision log (list of dicts).

    Raises SystemExit if anything changed and `revise` is None - that is the
    whole point. Passing --revise records the change instead of hiding it.
    """
    p = Path(lock_path)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    if not p.exists():
        p.write_text(json.dumps({
            "created": now, "hash": _hash(assumptions),
            "assumptions": assumptions,
            "revisions": [{"when": now, "reason": "initial lock", "changes": {}}],
        }, indent=1, ensure_ascii=False), encoding="utf-8")
        if not quiet:
            print(f"[lock] created {p.name} - {len(assumptions)} assumptions frozen")
        return [{"when": now, "reason": "initial lock", "changes": {}}]

    lock = json.loads(p.read_text(encoding="utf-8"))
    old = lock["assumptions"]
    changed = {k: (old.get(k, "<new>"), v) for k, v in assumptions.items()
               if k not in old or old[k] != v}
    dropped = [k for k in old if k not in assumptions]
    for k in dropped:
        changed[k] = (old[k], "<removed>")

    if not changed:
        if not quiet:
            print(f"[lock] {p.name} unchanged - {len(assumptions)} assumptions match")
        return lock["revisions"]

    if not revise:
        lines = [f"    {k}: {a}  ->  {b}" for k, (a, b) in sorted(changed.items())]
        raise SystemExit(
            f"\n[lock] BUILD BLOCKED - {len(changed)} assumption(s) changed since the lock:\n"
            + "\n".join(lines)
            + "\n\n  This is the check that would have caught the v3 TAM plug.\n"
              "  If the change is right, say why and it gets recorded in the workbook:\n"
              '      py <builder> --revise "why this changed, and what evidence moved it"\n'
              f"  To start over, delete {p}\n")

    entry = {"when": now, "reason": revise,
             "changes": {k: {"from": a, "to": b} for k, (a, b) in sorted(changed.items())}}
    lock["revisions"].append(entry)
    lock["assumptions"] = assumptions
    lock["hash"] = _hash(assumptions)
    p.write_text(json.dumps(lock, indent=1, ensure_ascii=False), encoding="utf-8")
    if not quiet:
        print(f"[lock] {len(changed)} change(s) RECORDED: {revise}")
        for k, (a, b) in sorted(changed.items()):
            print(f"        {k}: {a} -> {b}")
    return lock["revisions"]
