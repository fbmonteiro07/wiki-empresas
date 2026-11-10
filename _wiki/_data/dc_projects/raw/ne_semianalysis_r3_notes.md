# ne_semianalysis_r3.csv — projects SemiAnalysis names that the registry lacked (2026-11-09)

Added on Felipe's request after the SemiAnalysis tab showed them missing. Source of the list: SemiAnalysis, "Everyone Says Datacenter Moratoriums Are Killing the US Buildout. We disagree", 2026-09-15 (New York EO 62 projects; the NorthPoint case study). Each row was then checked against public sources (SEC filings, press, trackers); conflicts are in the row notes.

| Rows | Project | MW in the row | Date basis |
|---|---|---|---|
| NY-ALABAMA-STREAMSTAMP-ALL | Stream U.S. Data Centers at STAMP, Genesee County | 340 IT (SemiAnalysis; Stream's 2025 hearing said ~250) | no public date; 2028-06 = year_only convention on SemiAnalysis's "2028-or-later" floor |
| NY-NIAGARAFALLS-URBACON-DC1..DC3 | Urbacon / NFR Niagara Digital Campus | 50 + 42.5 + 42.5 (135 total, basis unstated; the 85 MW split is even, Capstone) | tracker years 2029 / 2030 / 2031 (Baxtel) |
| NY-NIAGARAFALLS-BLOCKFUSION-CW1, CW2, EXP | Blockfusion Niagara Falls, CoreWeave anchor lease | 25 + 60 IT (85 MW committed), 215 IT expansion (low) | company: revenue Feb-2028 on the first 25 MW; all 85 MW by 2029; expansion 2031-06 estimate |
| NY-LANSING-TERAWULFCAYUGA-P1..P3 | TeraWulf Cayuga, Lansing | 138 / 162 / 100 gross (400 gross ≈ 320 IT, 10-Q 3Q26) | estimate: construction Q1-2028 (SemiAnalysis) + ~15 months, then a year per phase |
| NY-TONAWANDA-RIVERVIEW-ALL | Riverview Innovation & Technology Campus, Tonawanda | 300 (press; SemiAnalysis says 200) | undated; likelihood low (site plan tabled, town moratorium) |

**Convention:** for New York rows, `local_approval=pending` also carries a pending state (DEC) permit, because EO 62 is modeled through the engine's `new_license` channel and the schema has no state-permit column. Said in each row's notes.

**Not rowed:** NorthPoint "Project Hazelnut" (Hazle Township, Luzerne County, PA; 15 buildings on ~1,280 acres in Humboldt North Industrial Park; phases starting Q4-2026 / Q1-2028 / Q2-2029 per Baxtel; Amazon named as end user by Fortune, not confirmed by Amazon). No source gives a MW figure, and the schema needs one. The Hazle Township curative-amendment pause is already in `local_moratoria.json` (LOC-PA-000). SemiAnalysis's other two locally delayed projects (an AWS campus in Ohio, a site in Colorado) are unnamed in the public text.
