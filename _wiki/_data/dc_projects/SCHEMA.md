# US data-center project registry — schema (v1, 2026-11-06)

One row = one **campus phase / building** with its own energization date. Built from public sources
(wiki corpus + web), laid out so an Aterio project export can replace or validate it later.
Raw regional files: `raw/<region>.csv` → merged by `_wiki/_tools/build_dc_delay.py` into `projects.csv`.

## Columns (CSV, UTF-8, header row exactly as below, RFC-4180 quoting)

```
project_id,campus,phase,developer,tenant,city,county,state,lat,lon,mw,mw_basis,campus_status,phase_status,likelihood,cod_base,cod_source,power_path,grid,utility,air_permit,air_permit_date,interconnection,local_approval,local_approval_date,local_moratorium,source,source_date,notes
```

| column | values / format | meaning |
|---|---|---|
| project_id | `ST-CITYSLUG-CAMPUSSLUG-PHASE`, upper-case, unique | e.g. `TX-ABILENE-STARGATE-B3` |
| campus | text | campus / project name as commonly reported (e.g. "Stargate Abilene (Crusoe/Lancium)") |
| phase | text | phase or building label; `all` if the source gives no split |
| developer | text | who builds / owns the shell (Crusoe, QTS, Vantage, Meta self-build …) |
| tenant | text or blank | end user if public (OpenAI/Oracle, Microsoft, Meta, Anthropic, xAI, CoreWeave …) |
| city, county, state | text, text, 2-letter | nearest city/town, county (or parish), state |
| lat, lon | decimal degrees, 3 dp | site if known, else city centroid |
| mw | number | capacity of THIS row |
| mw_basis | `IT` \| `facility` \| `grid` \| `gen` \| `unknown` | what the source's MW means: critical IT load, total facility, utility load request / interconnection, on-site generation nameplate. Record the source's basis — never convert silently |
| campus_status | `operating_expanding` \| `under_construction` \| `announced` | status of the campus as a whole |
| phase_status | `energized` \| `under_construction` \| `not_started` | status of this row |
| likelihood | `high` \| `medium` \| `low` | Aterio's tiers (GS call 2026-10-20): high = negotiated power + land + financing or hyperscaler/lab capex commitment (>80% materialise); medium = some of those (~50-60%); low = announcement only (<40%) |
| cod_base | `YYYY-MM` | expected energization of this row on the latest PRE-pause schedule. Year-only sources → `YYYY-06` with cod_source `year_only` |
| cod_source | `company` \| `filing` \| `press` \| `analyst` \| `year_only` \| `estimate` | where cod_base comes from |
| power_path | `grid` \| `btm_gas` \| `hybrid` \| `nuclear` \| `other` | grid-only; behind-the-meter gas prime power; grid + on-site gas/bridge; nuclear PPA/co-location; other |
| grid | `ERCOT` \| `PJM` \| `MISO` \| `SPP` \| `SERC` \| `WECC` \| `NYISO` \| `ISO-NE` \| `CAISO` \| `other` | balancing area / ISO |
| utility | text | serving utility (Oncor, Dominion, AEP Ohio, Georgia Power, Entergy …) |
| air_permit | `n/a` \| `issued` \| `pending` \| `not_filed` \| `unknown` | STATE air permit for on-site prime/bridge generation (e.g. TCEQ NSR/standard permit). `n/a` = grid-only with ordinary backup gensets |
| air_permit_date | `YYYY-MM` or blank | issue date (if issued) or filing date (if pending) |
| interconnection | `energized` \| `agreement` \| `study` \| `unknown` | large-load grid connection status |
| local_approval | `approved` \| `pending` \| `denied` \| `n/a` \| `unknown` | zoning / site plan / building permit; `n/a` = no construction approval required (added 2026-11-09; not for Texas). This field is what the engine's `new_license` channel tests, so in states where a pause holds STATE approvals it carries them: New York rows record the DEC permit EO 62 holds; Texas rows record state construction approvals (TCEQ construction stormwater / water) that the TCEQ freeze and the pledged Hinojosa ban would hold, with county abatements and city zoning in the notes only |
| local_approval_date | `YYYY-MM` or blank | |
| local_moratorium | text or blank | name of a local moratorium that covers the site (jurisdiction + dates if known) |
| source | `;`-separated URLs or corpus paths (relative to `E:\Wiki Felipe empresas`) | every row needs ≥1 |
| source_date | `YYYY-MM-DD` | date of the most recent source used for the row |
| notes | short text | conflicts between sources, basis caveats; never invent |

## Scope
- US only. Campuses with total planned capacity ≥100 MW (≥50 MW if part of a hyperscaler / AI-lab program).
- Rows with cod_base 2026-01 … 2030-12, plus phases already energized during 2026 (they feed the "already energized" bucket). Phases energized before 2026 are out.
- Unknown is a valid answer: leave the field blank or `unknown`. Permit status is NEVER guessed — the engine applies explicit, scenario-tagged defaults to unknowns.

## Rules file (`state_rules.json`) and local moratoria (`local_moratoria.json`)
Written by hand from the rules research (`raw/state_local_rules.md`); each instrument carries scope, start, end by scenario, grandfathering, lead time after reopening, and source + date. See the engine docstring for the bucket logic.
