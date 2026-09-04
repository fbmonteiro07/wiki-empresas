# Theme — Data Infrastructure & Observability in the AI stack

_Wiki · generated 2026-09-03 · cross-company theme · sources: equity calls (`_equity_calls`), briefing roll-ups (`_briefings`), earnings transcripts (CSCO, MSFT, PANW, NOW, ARM, MU, ORCL), research library (`relatórios bons`), Stratechery, wiki company pages. Company pages: [../00_INDEX.md](../00_INDEX.md) · themes index: [00_THEMES.md](00_THEMES.md)._

> **Reference exhibit.** This page was built off a pasted "AI stack" diagram (layers: Cybersecurity · Application Intelligence/LLMs · Application Software · Middleware · **Data Infrastructure** · Cloud IaaS · Compute/Memory/Networking, with **Observability** as a vertical column). The diagram names **SNOW · Databricks · MDB · PostgreSQL · Redis · ESTC** in the Data Infrastructure row and **DDOG · DT · Splunk · New Relic · Grafana** in the Observability column. ⚠️ **The source of the diagram was not confirmed** (it reads like a sell-side sector primer). Per house rule, the exhibit's source is to be confirmed by the user before it is cited as a broker view; nothing below is attributed to it.
>
> **Coverage note.** None of the eleven names has its own wiki page. Everything below is built from the corpus (broker calls, briefings, transcripts, buy-side letters). Where the corpus is thin (New Relic, Grafana, Redis) the page says so explicitly rather than filling the gap from memory. **2026-09-03 update:** 35 earnings-call transcripts (2024-11 → 2026-09) were archived for SNOW, MDB, DDOG, DT and ESTC (see §7) and the five newest prints are folded into each name's section below; sell-side reactions to the September prints are not yet in the corpus.

---

## 1. What it is / why it matters

The AI stack's economics are being argued at the top (frontier labs) and the bottom (GPUs, HBM, power). The two layers this page covers sit in the middle and get paid whether or not any particular model wins: **data infrastructure** is where the enterprise's proprietary context lives and gets served to models and agents, and **observability** is how the enterprise sees what those models and agents are doing, what it costs, and whether it is safe.

Four framings from the corpus set up the thesis:

- **"The token path is data."** Jefferies' Brent Thill, after his own firm's CIO said *"you have to put your data somewhere to create AI, you can't have data all over the place,"* concluded that Databricks and Snowflake are *"crushing it because they're in the token path — you're bringing the data in and then you're running AI analytics on top of that data"* (Jefferies · Brent Thill / Samad Samana, AI call, 2026-06-01). The same call extends the path to observability: *"if you look at Snowflake, Datadog, even Dynatrace at some point when AI comes to the enterprise that will help."*
- **Agents run on databases, not just GPUs.** Micron's Arcuri-hosted memory session laid out the mechanics: in an agentic workflow the agents *"are actually running on CPUs,"* with one agent querying structured databases (ERP, supply chain) and a RAG agent querying *"vector databases… looking for a similarity match,"* while the accelerator supplies the reasoning (UBS · Tim Arcuri, Micron memory call, 2026-05-15). Jassy's version at Amazon: *"post-training RL and agent tool use run mostly on CPUs, not accelerators… plus storage and vector databases"* (AMZN Q2'26 call, 2026-07-30, via [../AMZN.md](../AMZN.md)).
- **RAG is a database revenue line.** Morgan Stanley's GenAI-ROIC work names four hyperscaler monetization paths, the third being *"RAG — connecting open models to proprietary data… driving STORAGE AND DATABASE REVENUE"* (Morgan Stanley · Brian Nowak, 2026-08-12, via [../AMZN.md](../AMZN.md)). An AWS expert put databases at ~20–30% of AWS core revenue (expert estimate, not disclosed; Capstone expert call, 2026-08, via [../AMZN.md](../AMZN.md)).
- **Context, not model, is the next unlock.** UBS: *"the next leap forward for AI performance could come via the exposure to corporate IP, to corporate data, to context as everybody is now saying"* (UBS · Karl Keirstead, State of AI Software call, 2026-08-31). Google Cloud's Kurian built the whole cross-cloud lakehouse + Knowledge Catalog pitch on the same idea: *"most organizations have thousands of databases, teaching the model which system has what information… you need a system that builds that semantic graph"* (Stratechery interview with Thomas Kurian, 2026-04-23).

The buy-side scoreboard already reflects it. Infra-data software has been *"a fan favorite all year as Snowflake, Datadog, and JFrog shares are up 50 to 80% year to date. MongoDB has had a monster move off the April lows, Elastic has ripped"* (UBS · Keirstead, 2026-08-31). Jefferies' 200-response client survey ranked **Database, Cybersecurity, ServiceNow-style system-of-record and Datadog** as the software categories *least* at threat from AI (Jefferies · William Beavington, Global Software Client Survey, 2026-05-20).

---

## 2. Data Infrastructure — the layer, then the names

### 2.1 How the layer splits

The six names in the diagram are not one market. They cover three sub-layers that AI touches differently:

| Sub-layer | Names | What AI does to it |
|---|---|---|
| **Analytical platform** (warehouse / lakehouse / catalog) | Snowflake, Databricks | Becomes the *AI data repository*: enterprises consolidate data there to build custom agents; text-to-SQL and agent products bill on top. Highest observed pull-through. |
| **Operational database** (transactional, document, key-value) | MongoDB, PostgreSQL, Redis | Becomes agent *memory* and *state*: session state, tool outputs, embeddings, cache. Pull-through is real but contested (Postgres taking the new-app share). |
| **Search / index** | Elastic | Becomes the *permission-aware context plane*: the indexed copy of enterprise information that agents retrieve from. Optionality, not yet an inflection. |

Two hyperscaler analogues matter for reading each: Microsoft describes **Cosmos DB as "a memory layer for the AI agent"** (the MongoDB Atlas / DynamoDB / Firestore comparable) and **Azure PostgreSQL as the store for "structured data — orders, customer records, inventory"** that agents retrieve, and **Fabric as its answer to "Snowflake, Databricks, traditional data warehouse, data lakes, all of it combined"** (BofA MSFT 4QFY26 callback, 2026-07-30).

### 2.2 Snowflake (SNOW) — the AI data repository that turned into an AI winner

**Role in the AI stack.** Cloud data warehouse that is now positioning as the place enterprises land data *specifically to build AI on it*. UBS's field checks are the clearest statement of the mechanism: Kraft Heinz declined Workday's HR AI suite and instead plans to *"migrate that Workday-generated HR data into Snowflake and use AI tools on top to build proprietary HR AI solutions"*; a CFO at UBS's Cursor dinner is migrating finance data *"into a dedicated Snowflake data warehouse instance and then build AI apps/agents on top."* Keirstead's read: *"a real role as an AI data repository layer, driving usage"* (UBS · Keirstead, 2026-08-31).

**Product hooks.** Cortex Code (agentic coding/pipeline automation, hosts an Anthropic model; described by FundaAI as the fastest-growing product in SNOW's history — @fundaai, 2026-05-27), Snowflake Intelligence, Cortex Analyst (text-to-SQL, which FundaAI says Snowflake and Databricks have made *"a standard data-warehouse feature"* — FundaAI, 2026-08-05, via [tokenmaxxing.md](tokenmaxxing.md)). Sell-side: Cortex Code *"sells itself — automates pipelines in natural language, compresses sales cycles"* (Investor Day read-across, briefing 2026-06-03).

**Numbers (F1Q27, reported 2026-05-27).** Product revenue **$1.33B vs cons $1.27B, +34% y/y (accelerated from +30%)**, record net-new product revenue; FY27 product-revenue guide raised to **+31% from +27%**; **$6B, 5-year AWS agreement** for Graviton access. Stock **+32–37%** next day (briefing 2026-05-28). Investor Day (2026-06-02): **FY31 TAM $460B; GAAP EPS positive by 4Q FY28 (Jan-2028)** (MS · Sanjit Singh, OW PT $300; DB · Brad Zelnick, Buy PT $300; Barclays · Raimo Lenschow, OW; UBS · Keirstead, Buy — briefing 2026-06-03).

**Where the Street stands.** MS PT $245→$300 OW *"joining the ranks of select AI winners"*; Barclays PT $192→$272 EW; UBS Buy *"Cortex Code drives material upside"* (all 2026-05-28). Bernstein **Market-Perform, PT $250**, on 17.6x/13.2x/10.4x EV/Sales 2026–28 (Bernstein Gen-AI Handbook ticker table, prices 2026-06-16). Into the F2Q27 print UBS's bar was *"36–37% revs growth in July, exiting the year at close to 40 — I think those are doable"* (UBS · Keirstead, 2026-08-31). Sentiment ordering flipped from **DDOG > MDB > SNOW** pre-print to **SNOW > DDOG > MDB** post-print (Barclays desk · Jeffrey Rand, 2026-06-09; JPM · Mark Schilsky, 2026-05-29).

**The bear.** Redburn (Sousa) went to **Sell** on a proprietary dataset showing SNOW *"losing material market share to Databricks"* (briefing 2026-05-19); an R&Co specialist framed *"terminal risk"* — SNOW lost ~10% share in the Python developer ecosystem, Databricks +50% YTD average daily activity vs SNOW +8% (briefing 2026-05-26). Jefferies' rebuttal to the "Snowflake is the Splunk of AI" line: *"I don't see that… when Databricks has a $140+ billion valuation, I still think Snowflake's undervalued"* (Jefferies · Thill, 2026-06-01). UBS explicitly tested the bigger structural bear — that frontier models get so good at data tasks customers bypass data software — across 7 partners/customers and *"concluded that VERY FEW ENTERPRISES ARE DIRECTLY HARNESSING THE DATA CAPABILITIES OF LLMs IN A WAY THAT IS CURTAILING SPEND ON SNOWFLAKE, PALANTIR OR DATABRICKS"* (UBS · Keirstead, SNOW preview, 2026-08-31, via [../PLTR.md](../PLTR.md)).

**Buy-side voice.** Octahedron holds SNOW as a top-3 public position, calls the F1Q27 reacceleration the start of a move *"into the mid-high 30s"* with Cortex Code layering on (Octahedron 2Q26 LP call, 2026-07-15). BofA's Fenske: SNOW and MDB are *"along the right side of AI… you have to be future-proof"* (BofA · Brian Fenske, 2026-04-16).

**F2Q27 (reported 2026-09-02, company transcript on disk).** Product revenue **$1.49B, +37% y/y** (accelerated again from +34%), *"second consecutive quarter of record sequential dollar growth"*; NRR **126%**; **828 customers above $1M** trailing spend (48 added in the quarter), 65 above $10M; RPO **$9B, +30%**; 692 net new customers (+32% y/y); use cases deployed +89% y/y; non-GAAP operating margin **15%** (+400bp). Guide: **FY27 product revenue $6.07B, +36%** (was +31%), Q3 **$1.588–1.593B, +37–38%**, FY27 operating margin **14.5%** (from 13.5%), FCF margin 23% reiterated (SNOW Q2 FY27 call — Sridhar Ramaswamy / Brian Robins, 2026-09-02). ➜ UBS's *"36–37% in July, exiting near 40"* bar was met and the full-year guide now sits at the top of it. **The AI cost of it:** non-GAAP product gross margin fell to **74%** *"because we have increased our guidance so much"* (Robins, answering Keirstead on whether a mix shift from frontier to cheaper models helps margins); Ramaswamy on model neutrality: *"We are absolutely seeing a lot of interest in being able to switch between different models and also to optimize cost"* — the token-routing debate from [tokenmaxxing.md](tokenmaxxing.md) now shows up inside Snowflake's gross margin (SNOW Q2 FY27 call Q&A, 2026-09-02). ⚠️ Sell-side reactions to this print are not yet in the corpus.

### 2.3 Databricks (private) — the lakehouse that wants to be the "agentic system of record"

**Role in the AI stack.** Started as the Spark/lakehouse data-engineering layer (ETL, pipelines, ML), added a data warehouse, a catalog/semantic layer (Unity Catalog), model serving and now agent tooling (Genie text-to-SQL, Mosaic). Octahedron's description of why it wins in the agent era: *"the whole infrastructure and management layer, the whole data catalog and indexing and semantic layer on top of that, and then more recently the intelligence layer on top of your data enabling people to access and use it in natural language… and the inference and serving for all of that"* (Octahedron 2Q26 LP call, 2026-07-15). Deutsche Bank's one-line takeaway from Data + AI Summit 2026: *"ambition to become the agentic system of record for the enterprise"* — echoed by Jefferies (DB · Brad Zelnick; Jefferies · Thill via Favuzza, briefing 2026-06-17).

**Scale (all third-party; no public filings).**
| Datapoint | Value | Source |
|---|---|---|
| Revenue growth | *"accelerating revenues to 80%"* | Octahedron 2Q26 LP call, 2026-07-15 |
| Data warehouse (SNOW-competing) | **$1.5B annualized, ~100% y/y** | Octahedron, 2026-07-15; "sales doubled" per briefing 2026-06-16 |
| Same product, 18 months earlier | $600M ARR, >150% y/y | Octahedron Databricks deck, 2024-12-10 |
| Revenue scale | >$4bn CY25E, >$11bn CY28E (>40% CAGR) | Octahedron deck, 2024-12-10 (fund estimates) |
| Penetration | >60% of Fortune 500 | Octahedron deck, 2024-12-10 (Databricks disclosure) |
| Valuation | $140B+ (Jefferies, 2026-06-01); *"Databricks at $175B"* (desk note, briefing 2026-06-09); round price $92.50/sh, EV $59bn at Dec-2024 | as cited |

⚠️ The deck numbers are Octahedron's own projections from December 2024 for an LP audience; carry them as a fund's bull case, not as company guidance.

**Why it is a short thesis for others.** Octahedron (Databricks is its largest position, so read accordingly) argued that Databricks' core advantage — *"we use data existing in your data lake at low cost, and we turn it into an extremely high-performance data warehouse, database, data analytics store"* — is being pointed at adjacent categories: **LakeWatch (SIEM)** that *"completely takes out the economics from the old providers like Splunk,"* a customer-data platform, and a lake-based **database** offering *"scaling at not yet publicly announced numbers"* (Octahedron, 2026-07-15). The Panther acquisition (security data platform) landed the same week as the Summit (DB · Zelnick, briefing 2026-06-17). Databricks' Postgres offering exists but is **not in the corpus** — do not quote a number for it.

**How the sell-side uses it.** As the reason for a SNOW Sell (Redburn), as the private comp that makes SNOW look cheap (Jefferies), and as one of the *"front-end procurement engines"* that rev-rec OpenAI/Anthropic model access — a quality-of-growth caveat Keirstead applies to Azure *"as well as Databricks and others"* (UBS · Keirstead, MSFT callback, 2026-07-30). Archera's cloud-strategy expert argued Meta *"needs to buy Databricks… a real front end with a sales team"* if it wants to rent capacity as a cloud (Archera expert call, 2026-07-13) — an opinion, not a report of talks.

**Internal.** The 2026-08-24 weekly floated *"Databricks/Snowflake as the data-layer middle path that operates both"* open-weight and frontier models — the neutral layer if enterprises adopt AI outside the clouds ([internal-weekly-meeting.md](internal-weekly-meeting.md), 2026-08-24).

### 2.4 MongoDB (MDB) — the cleanest usage meter, and the most debated

**Role in the AI stack.** Document database (Atlas = cloud DBaaS) positioned as agent memory: *"agents repeatedly read/write session state, tool outputs, permissions, application data, intermediate results and prior actions. Atlas monetizes the hot working set — memory, CPU, throughput and availability — so agent activity can transmit directly into consumption revenue"* — Citrini's *"cleanest automatic usage meter"* (Citrini Semis, "All Along the AI Watchtower," 2026-07-20, via [ai-builder-toolkit.md](ai-builder-toolkit.md)). Microsoft's Cosmos DB is the direct comparable (BofA MSFT callback, 2026-07-30). Vector search is native; JPM framed the F1Q27 print as *"The Anthropic Quarter — Anthropic AI workloads driving MDB Atlas vector DB demand"* (JPM · Mark Schilsky, 2026-05-26).

**Numbers (F1Q27, reported 2026-05-28).** Revenue **$688M, +25% y/y** ($23M ahead); **Atlas +29.4%** (from +27%); Enterprise Advanced +20%; Q2 guide +24%; FY27 midpoint raised to **+19.5%** (from +17%); Atlas FY27 **+23–25%** (from +21–23%). Management *"finally turning constructive on AI tailwinds… from both enterprise and AI-native customers"* (briefing 2026-05-29). Citrini: Atlas reaccelerated from ~26% to 29%+, crossing a **$2B annualized run-rate** (Citrini, 2026-07-20). AI-native logos named at the CEO HQ visit: Base44, ElevenLabs; Voyage embeddings *"differentiated"* (Barclays · Rand, 2026-06-09).

**Where the Street stands.** MS OW PT $335→$380; Barclays OW $370→$387; UBS Neutral $275→$350; GS Buy (briefing 2026-05-29). Bernstein **Outperform, PT $449**, 10.4x/8.5x/7.1x EV/Sales 2026–28 (Bernstein, prices 2026-06-16). BofA's Koji Ikeda: *"buy-rated Datadog and buy-rated MongoDB… a very healthy debate on MongoDB right now with the key question: will the AI tailwinds come a year from now, or potentially sooner?"* (BofA conference wrap, 2026-06-08). Trades at a *"5–8x discount to DDOG/SNOW"* (GS desk · Peter Callahan, 2026-05-29).

**The bear, and it is specific.** UBS (Keirstead, 2026-08-31): *"I'm not hearing similar AI pull-through anecdotes that would point to real growth acceleration. The operational database layer overall is not seeing as material a pull-through as elsewhere. And when I do hear of database capacity needs rising, it's almost always for Postgres-based databases."* His posture: patient, not negative — *"Atlas growth of 29, maybe 30% is impressive. And the stock at around 10 times forward revenues is not outrageous."* The same house's earlier note read hyperscaler checks naming *"Redis and Postgres"* at the database layer as *"MongoDB facing material competition for AI workloads"* (UBS · Keirstead/Arcuri, 2026-07-22, via [tokenmaxxing.md](tokenmaxxing.md)). Citrini's own bear: *"new AI apps may default to Postgres ecosystems such as Supabase/Neon/pgvector instead of MongoDB; hyperscalers and labs may internalize agent memory"* (Citrini, 2026-07-20). Barclays called the Postgres bear *"dormant"* in June (Rand, 2026-06-09) — UBS's August checks say it is not.

**M&A angle.** Jefferies lists MDB among the four public infra-software assets left after IBM bought Confluent (Datadog, Dynatrace, Elastic, Mongo, GitLab), but *"that would probably take $40 billion… highly unlikely"* (Jefferies · Thill, 2026-06-01).

**F2Q27 (reported 2026-09-01, company transcript on disk).** Revenue **$772M, +30% y/y** — *"the highest level of quarterly growth since fiscal 2024"*; **Atlas ~+29% for the fifth straight quarter**, ~300bp above guide, record **$127M sequential dollar add**; **EA & other +36%** on the Q2 launch of search and vector search on Enterprise Advanced; net ARR expansion **122%** (from 121%); RPO **$1.52B, +91%**; ~3,000 customers above $100K ARR (+17%); **48% of $100K+ Atlas customers use two or more features**, *"driven largely by vector and text search adoption"* (from 42%); non-GAAP operating margin **24%** (from 15%). Guide raised: **FY27 revenue $2.99–3.03B, +21–23%** (was +19.5%); **Atlas FY27 ~27%** (was +23–25%), Q3 Atlas ~26%; EA & other FY27 ~+11% (was mid-single digit); Q3 revenue $756–761M, +20–21%; FCF conversion at the upper end of 80–100% (MDB Q2 FY27 call — CJ Desai / Mike Berry, 2026-09-01). CEO: *"We are seeing AI workloads land on MongoDB across all of them."* **The Postgres head-to-head, from the company:** an AI lab *"uses us for inference and chat workloads after moving away from PostgreSQL due to performance lags and outages… migrated their chat memory system onto Atlas in just four weeks and now run at 10x faster reads than PostgreSQL"*; labs also store *"experimental results, evaluation data, and training artifacts"* on Atlas — *"still early, and engagement varies lab by lab"* (MDB Q2 FY27 call, 2026-09-01). ⚠️ Company-sourced anecdote, one lab; it is the direct rebuttal to UBS's *"almost always Postgres,"* not a refutation of it. ➜ Against UBS's bear: Atlas did **not** accelerate past 29%, but total revenue did (EA), the guide raise was larger than the beat, and the vector-search attach number is the first hard AI-feature datapoint the company has given. ⚠️ Sell-side reactions not yet in the corpus.

### 2.5 PostgreSQL — an open-source project, monetized by everyone except itself

**What it is.** PostgreSQL is not a company; it is the open-source relational database that has become the default store for new AI applications (pgvector for embeddings, Supabase/Neon as serverless Postgres). The revenue accrues to whoever hosts it.

**Who is monetizing it in the corpus.**
- **Microsoft:** *"PostgreSQL revenue grew 55%, accelerating for the third consecutive quarter"*; *"PostgreSQL-with-Foundry customers +80%"* (MSFT 4QFY26 call, 2026-07-29; JPM · Samik Chatterjee, 2026-08-13; BofA callback, 2026-07-30 — via [../MSFT.md](../MSFT.md)). Microsoft's own segmentation: Postgres = the structured business data agents retrieve, Cosmos = the memory they write.
- **AWS:** Aurora/RDS inside the ~20–30% database share of AWS core revenue (expert estimate, [../AMZN.md](../AMZN.md)); *"a variety of Postgres-based databases (Supabase, Databricks)"* named in the same expert's competitive map.
- **The Street's read-through:** UBS's *"almost always Postgres"* line is the single most important datapoint on this sub-layer — it is where operational-database AI demand is showing up, and it is why MDB's AI story is contested (UBS · Keirstead, 2026-08-31).

**Read for the diagram.** Postgres is the deflationary force in operational data: it is free, it runs everywhere, and the hyperscalers are happy to sell it at compute margins. The public-equity way to own it is MSFT/AMZN/GOOG database lines — and, negatively, MDB's new-app share.

### 2.6 Redis (private) — the cache tier; thin corpus

**Role in the AI stack.** In-memory key-value store used as cache, session store, message broker and increasingly vector store / semantic cache. In agent architectures it is the low-latency short-term memory and the layer where *answer caching* would live — UBS's CFO dinner named *"answer caching"* alongside model routing and usage caps as the token-efficiency levers in play (UBS · Keirstead, 2026-08-31). ⚠️ That the caching happens in Redis is this page's inference, not the source's statement.

**Corpus evidence (sparse).** (1) UBS hyperscaler checks: database capacity needs rising for *"Redis and Postgres"* (UBS, 2026-07-22). (2) Arm's Performix launch *"with support from Microsoft, MongoDB, Redis, and SAP, helping developers and AI agents analyze and optimize workloads running on Arm-based infrastructure"* (ARM Q1 FY27 call, 2026-07-29). (3) AWS's managed Redis named in the AWS competitive map ([../AMZN.md](../AMZN.md)). (4) An anecdote: a Claude Code agent found *"3 unused Redis instances ($104/mo)"* and cleaned them up with approvals — a small illustration of agents managing infra spend (@godofprompt, 2026-05-26, briefing). **No broker has written on Redis in the corpus; it is private (Redis Ltd.).**

### 2.7 Elastic (ESTC) — search that became a context plane, plus observability and security

**Role in the AI stack.** Elastic *"creates its own searchable indices and ranks information by semantic relevance, keywords, metadata, permissions, recency and operational signals"* — Citrini's *"permission-aware enterprise context plane,"* i.e. the indexed copy of enterprise information agents retrieve from (Citrini, 2026-07-20, via [ai-builder-toolkit.md](ai-builder-toolkit.md)). It is the one name in the diagram that straddles both layers: the same index underpins Elastic Observability and Elastic Security. WFC's cloud expert grouped it with Datadog and Dynatrace as observability platforms that have *"stretched into security"* with *"AI baked into their platform"* (WFC cloud/MSFT expert call, 2026-04-14).

**Numbers.** FY26/Q4 growth 17%/16%; FY27 guide ~14%; cRPO/RPO +20%/+28%; more than one-third of $100k+ customers using Elastic AI capabilities; ~19% guided operating margin (Citrini, 2026-07-20). Bernstein comps chart put ESTC at 0.44x EV/revenue/growth on CY25E (Octahedron deck, comps as of 2024-11-25). Microsoft cites Elastic as a customer running on its Cobalt Arm CPUs (MSFT Q4 FY24 call; BofA callback 2026-07-30).

**Q1 FY27 (reported 2026-08-27, company transcript on disk).** Revenue **$478M, +15%**; sales-led subscription **$399M, +18%**; cRPO **$1.2B, +21%** (20% cc, second straight quarter at 20%), RPO **$1.9B, +27%**; >1,800 customers above $100K ACV, now 90% of sales-led subscription revenue; **over 37% of $100K+ customers using Elastic for AI, from ~21% a year ago**; non-GAAP operating margin 16.2%; adjusted FCF margin 30%. Guide: Q2 revenue $486–487M (~+15%), OM ~19%; **FY27 revenue $1.998–2.010B, +15.2%** (above the ~14% Citrini cited in July), OM ~19.4%, FCF margin 21.5% (ESTC Q1 FY27 call — Ash Kulkarni / Navam Welihinda, 2026-08-27). ➜ Management calls it *"validation for our acceleration trajectory"*; on UBS's *"nothing is really inflecting"* the numbers say a one-point acceleration, not an inflection.

**Where the Street stands.** UBS's Roddy Sultan on the *"multiple dispersion"* debate: *"GitLab and Elastic that are more than doubled off the bottom, but still trade at four to five times sales, or do you own a high flyer like JFrog or Datadog at 14 times sales… I still lean more in the latter camp… GitLab and Elastic could be under pressure over the next few months as fundamentally things sound stable but nothing is really inflecting"* (UBS · Roddy Sultan, 2026-08-31). Citrini's scorecard: *"ESTC monetizes the indexed copy of enterprise information… positive; inexpensive AI-search optionality against ~14% FY27 guide."* Jefferies lists it as one of the assets IBM *"could really buy"* (Jefferies · Thill, 2026-06-01).

---

## 3. Observability — what AI changes, then the names

### 3.1 Three demand vectors and one deflation risk

Observability (logs, metrics, traces, APM) is billed on data volume and hosts. AI changes it in three ways, each visible in the corpus:

1. **AI-native customers are the fastest-growing cloud spenders, and they need monitoring.** Datadog's AI-native cohort grew an estimated **~114% y/y in 1Q26** (from 169% in 4Q25), two large research-lab deals were announced (*"likely OpenAI / Anthropic adjacent"*), and the desk read was *"AI-native cloud spend not slowing; observability + AI-DC monitoring is durable"* (briefing 2026-05-08). Keirstead reads Azure's broad-based core demand as *"a positive read-through to all of the infra data exposed names that are tethered to AWS/Azure growth, such as Datadog and Snowflake"* (UBS, MSFT callback, 2026-07-30).
2. **A new category — LLM / agent observability and evals.** Dynatrace bought Arize; UBS's checks *"assess there's a real moat around the harness and workflow that Arize has doing eval"* (UBS · Roddy Sultan, 2026-08-31). Cisco announced *"observability for AI"* and *"agent behavior monitoring"* via the Galileo and Astrix acquisitions (CSCO Q3/Q4 FY26 calls, 2026-05-13 / 2026-08-12). ServiceNow's rule: *"no agent goes live without clearing governance, risk, value validation, and observability"* (NOW Q2'26 call, 2026-07-22). Microsoft's Agent Framework ships *"compliance, observability"* as defaults (MSFT Q1 FY26 call, 2025-10-29). The category is real; who owns it is open.
3. **Convergence with security.** The WFC cloud expert's most pointed claim: *"the bigger threat to security vendors… is observability and the broadening that they have encompassed… Datadog's stretched into security. Dynatrace has stretched into security. Splunk and Cisco are still trying to figure out what they're doing"* — and Palo Alto's Chronosphere purchase *"tells you that's a pretty important category"* (WFC expert call, 2026-04-14). Jefferies: *"clearly observability is firing as you've seen with Datadog and with Chronosphere within Palo"* (Jefferies RTYA call, 2026-06-08).

**The deflation risk.** Log economics are the soft underbelly. Palo Alto's Arora justified Chronosphere by saying incumbent observability is *"not designed for the AI era… a third of the cost"* (PANW Q1 FY26 call, 2025-11-19). Octahedron says Databricks' LakeWatch *"completely takes out the economics from the old providers like Splunk"* (Octahedron, 2026-07-15). Both are challengers talking, but the mechanism — cheap lake storage replacing premium log indexing — is the same one that hit the warehouse market.

**Sizing.** Cisco's Investor Day put the **Observability TAM at $51B by 2027** inside a $575B total, growing faster than networking (Security & Observability modeled at 15–17% vs Networking 2–5%) (CSCO Investor Day, 2024-06-04, via [../CSCO.md](../CSCO.md)).

### 3.2 Datadog (DDOG) — "From Observability Leader to AI Winner"

**Role in the AI stack.** Cloud-native observability platform (infrastructure, APM, logs, plus security and now LLM observability via Bits AI). The corpus treats it as the cleanest public proxy for AI-native cloud consumption.

**Numbers (1Q26, reported 2026-05-07).** Revenue **+32% y/y** (~5% above cons), strongest usage growth since 1Q22, record net-new ARR; Q2 guide high-end **+31% vs cons +20%**; FY26 high-end **+27% vs cons +20%** (a normal beat cadence implies ~36%); core ex-AI-natives accelerated for a third straight quarter to **mid-20s**; AI-native revenue **~+114%**. Stock **+29–30%**. MS PT $180→$225 OW *"From Observability Leader to AI Winner"* (Sanjit Singh / Keith Weiss); UBS 2026 revenue growth 27%→33% (Keirstead); JPM raised to a Street-high target, *"Hyperscalers' AI Labs Fetching New Workloads"* (Mark Murphy) (briefing 2026-05-08).

**Positioning.** Datadog replaced MongoDB as the *"Most Crowded Name in Software"* (JPM · Schilsky, 2026-05-26); R&Co specialist *"AI Winner"* at 13x '27 EV/S; DDOG's market cap ran to +37% above SNOW's at **13.5x vs 7.25x CY27 EV/S** (Schilsky, 2026-05-19). BofA's Ikeda: *"I don't hear a lot of bears on Datadog. That is something to think about"* (2026-06-08). UBS's Sultan owns it in the *"high flyer at 14 times sales with the hope of more estimate revisions"* camp (2026-08-31). Barclays desk: *"DDOG clear favorite in infra"* (Rand, 2026-05-22).

**AI on the P&L, both sides.** The Archera expert used Datadog to explain how established software vendors run agents: *"Datadog on Bits AI does care if it has negative margins"* — so it runs a router with proprietary frontier models *and* an owned, fine-tuned open-source model in the stack, for margin, IP and vendor diversity (Archera expert call, 2026-07-13). The Jefferies survey put Datadog among the four categories least at threat from AI (Jefferies · Beavington, 2026-05-20).

**2Q26 (reported 2026-08-06, company transcript on disk).** Revenue **$1.12B, +36% y/y**, above the high end of guidance; **+11% q/q, the highest since Q2 2022**, record **$115M sequential dollar add**; **non-AI customers accelerated to the high-20s%** (from mid-20s, from 18% a year ago); ~4,720 customers above $100K ARR (from ~3,850), 91% of ARR; 58% of customers on four or more products (from 52%), 13% on ten or more (from 7%); RUM above $200M ARR growing 50%+; RPO **$3.47B, +43%**, cRPO ~+40%; operating margin **23%**; FCF $279M (25% margin). Guide: Q3 **$1.135–1.145B, +28–29%**; **FY26 $4.45–4.47B, +30%** (the May high end was +27%), operating margin 23% (DDOG Q2 2026 call — Olivier Pomel / David Obstler, 2026-08-06). ⚠️ Sell-side reactions not yet in the corpus.

### 3.3 Dynatrace (DT) — the cheaper way in, now with an AI-observability asset

**Role in the AI stack.** Enterprise APM/observability with a causal-AI engine (Davis) and a Grail data lakehouse; historically strong in large, complex enterprise estates. Has *"stretched into security"* (WFC expert, 2026-04-14).

**What changed in 2026.** UBS **assumed coverage at Buy (from Neutral)** on 2026-06-16 (stock +2.5% premarket, briefing 2026-06-16). By 2026-08-31 it was Roddy Sultan's best risk/reward in his coverage: *"Dynatrace, I think is an interesting candidate. Still a reasonable multiple, cheaper than Elastic, for in my view, better growth and a higher quality business. We're in the midst of doing a bunch of checks around the Arize acquisition in AI observability. Checks assess there's a real moat around the harness and workflow that Arize has doing eval"* (UBS · Sultan, 2026-08-31). ⚠️ Deal terms for Arize are **not in the corpus**. BofA hosted DT's CPO and CFO for an observability webinar into the quiet period (BofA · Koji Ikeda, 2026-06-08). Bernstein comps chart: 0.51x EV/rev/growth on CY25E, in line with SNOW/WDAY (Octahedron deck comps, 2024-11-25).

**Q1 FY27 (reported 2026-08-05, company transcript on disk).** ARR **$2.14B, +17%**; net new ARR **$85M, +66%** (41% organic excluding the $13M ARR BindPlane acquisition); revenue **$555M, +15%**, 100bp above the high end; NRR 110% (TTM); average land ~$285K, new-logo ARR growth >160%; average ARR per customer >$500K; **logs the fastest-growing category, growing well above 100% to ~$200M annualized consumption** (*"nearly doubling since surpassing the $100 million milestone just two quarters ago"*); non-GAAP operating margin 29%; adjusted FCF 28% of revenue TTM. Guide: cc ARR growth **15.5–16.5%** maintained, revenue growth 14.5–15% (FX now a $14M ARR / $4M revenue headwind), OM high end 29.75%, EPS $1.97–1.99; Q2 revenue +15–16% (DT Q1 FY27 call — Rick McConnell / Jim Benson, 2026-08-05). ⚠️ Arize is not mentioned on this call; UBS's 08-31 reference to *"the Arize acquisition in AI observability"* therefore post-dates it or was announced off-call — terms remain unsourced here.

**M&A.** One of the two names Jefferies thinks IBM *"could really buy"* (with Elastic) as it works through the shrinking list of public infra-software assets (Jefferies · Thill, 2026-06-01).

### 3.4 Splunk (Cisco) — the incumbent log platform, mid-transition, under cost attack

**Role in the AI stack.** Log analytics / SIEM / observability, acquired by Cisco ($28B, closed 2024). Inside Cisco it reports mostly in **Security** with pieces in **Observability**; Cisco's pitch is that agentic AI *"is expanding the threat landscape driving demand for our security and observability solutions to help monitor agent behavior"* (CSCO Q4 FY26 call, 2026-08-12).

**Operating record.** Cisco Observability grew **+41% (Q4 FY24) and +36% (Q1 FY25)** on Splunk consolidation (CSCO calls, 2024-08-14 / 2024-11-13). Since then the story is the **on-prem → cloud subscription transition**: *"creating a near-term drag on revenue growth… we saw another 2 or 3 points [of mix shift] during the quarter"* (Chuck Robbins, Q3 FY26, 2026-05-13); Security was flat in Q3 FY26 and down 4% in Q2 FY26 partly on it. It swung to **Security +14% in Q4 FY26 on "sizable Splunk on-premise deals"** (MS · Meta Marshall, 2026-08-13), which Cisco itself warned not to extrapolate; **F1Q27 is the last hard Splunk compare**, and FY27 color has observability growing only low single digits (JPM relay, 2026-08-14, via [../CSCO.md](../CSCO.md)). Logos: **>1,000 new Splunk logos in FY26 (target met), 280+ in Q4, highest competitive-win quarter of the year** (CSCO Q4 FY26). Splunk is now folded into "whole portfolio agreements" and Cisco Cloud Control (single management plane, *"unified data layer for all Cisco products built for humans and agents,"* ~4,500 enterprises signed up since June) (CSCO Q4 FY26). JPM notes Security growth running single digits vs the 15–17% Investor-Day target, *"implying share loss despite the acquisitions"* (JPM, 2025-12-15, via [../CSCO.md](../CSCO.md)).

**The AI-era threat is cost.** Databricks' LakeWatch is explicitly aimed at Splunk's economics (Octahedron, 2026-07-15); Palo Alto's *"a third of the cost"* line is aimed at the same incumbency (PANW, 2025-11-19); and *"the Splunk of AI"* is now a pejorative investors apply to other names (Jefferies, 2026-06-01). WFC's expert: *"Splunk and Cisco are still trying to figure out what they're doing"* (2026-04-14). Cisco's counter is distribution and bundling, plus adjacent M&A (Galileo, Astrix closed Q4 FY26).

### 3.5 New Relic (private) — zero corpus coverage

New Relic is the APM pioneer taken private by Francisco Partners and TPG in 2023; it is not on any broker's public-comp list in the corpus and no call, briefing or note mentions it. ⚠️ **Nothing below is sourced from the corpus:** its role is full-stack observability with consumption pricing and a bundled AI-monitoring module, competing head-on with Datadog and Dynatrace for mid-to-large enterprise. Treat it as a competitive datapoint (pricing pressure on the public names) rather than an investable read, and note that Jefferies' IBM-target list of public infra names necessarily omits it (Jefferies · Thill, 2026-06-01).

### 3.6 Grafana Labs (private) — the open-source default, especially for GPU fleets

**Corpus evidence (thin).** Grafana Labs appeared on Morgan Stanley's NYC Software Bus Tour alongside **DDOG, CRWV, MDB and VRNS** (Jun 2–4, 2026; briefings 2026-05-27/29) — the only private on a public-infra-software itinerary, which is the tell for how the Street thinks of it. SemiAnalysis's cloud-security thread listed *"Multi-tenant Grafana"* among the controls it audits at neoclouds (@SemiAnalysis_, 2026-08-30, via [../CRWD.md](../CRWD.md) / [../PANW.md](../PANW.md)).

⚠️ **Outside the corpus:** Grafana is the visualization layer of the open-source observability stack (Prometheus metrics, Loki logs, Tempo traces) and is the de-facto dashboard for GPU cluster telemetry at AI labs and neoclouds. That makes it a substitution risk for the paid platforms at exactly the AI-native customers Datadog is growing fastest in — and it is why the CoreWeave/Grafana pairing on the bus tour is worth noting.

### 3.7 Adjacent owners of observability the diagram omits

- **Palo Alto Networks / Chronosphere:** $3.35B for ~$160M ARR growing triple digits (announced 2025-11-19); ARR **>$300M** by Q3 FY26 (PANW call, 2026-06-02). This is the security platform buying its way into the observability column.
- **Cisco:** Splunk plus Galileo, Astrix, ThousandEyes, AppDynamics; observability TAM $51B (2027).
- **ServiceNow:** AI Control Tower as the governance/observability gate for agents; Workflow Data Fabric integrating Databricks and Snowflake, framed as doubling the TAM to $500B (NOW Q3'24 call, 2024-10-23; Q2'26 call, 2026-07-22).
- **Microsoft / Google / AWS:** first-party monitoring and agent frameworks with observability built in; the same hyperscalers are the distribution partners (SNOW's $6B AWS deal, Elastic on Cobalt, Datadog on the marketplaces).

---

## 4. Key debates

- **Bull / where the money is.** *"Software's going to win, but you have to be in the token path. The token path is data"* (Jefferies · Thill, 2026-06-01). The mechanism is consumption: agents generate machine work that databases, indices and monitoring pipelines bill automatically, while seat-based apps do not (Citrini, 2026-07-20). BofA heard *"no infrastructure software company signaling any sort of incremental demand headwinds"* at its June conference (Ikeda, 2026-06-08). UBS's checks found the LLM-disintermediation bear absent *today* (Keirstead, 2026-08-31).
- **Bear 1 — Postgres eats the operational layer.** Where database capacity is rising it is *"almost always Postgres"* (UBS, 2026-08-31); MSFT's +55% Postgres line is the proof; MDB is the public name that wears it.
- **Bear 2 — the platform is a pass-through.** Some infra-data growth is rev-rec of frontier-model access, which Keirstead flags for Azure *"as well as Databricks and others"* (UBS, 2026-07-30). Growth quality matters when multiples are 13–14x sales.
- **Bear 3 — Databricks as the deflator.** Private, growing ~80%, and now shipping into warehouse (vs SNOW), SIEM (vs Splunk), CDP and database (Octahedron, 2026-07-15). Redburn's SNOW Sell rests on it (2026-05-19). Counter: Octahedron is Databricks' largest holder, and UBS's own SNOW checks were positive into the print.
- **Bear 4 — log economics.** Cheap lake storage vs premium log indexing (Arora's *"a third of the cost,"* LakeWatch). The incumbents most exposed are the ones with the largest per-GB pricing: Splunk first, then the public observability names if AI-native log volumes force price-per-GB down faster than volumes rise.
- **Bear 5 — crowding.** Sentiment rotated DDOG → SNOW → back; MDB was *"most crowded"* then fell 22% on a print (JPM · Schilsky, 2026-05-26). Bogeys *"have inched up"* and *"each of these stocks has set-up problems, just given richer multiples, more crowded positioning"* (UBS · Keirstead, 2026-08-31).
- **Timeline / inflection points.** MDB F2Q27 (2026-09-01) and SNOW F2Q27 (2026-09-02) prints — both post-corpus; DDOG 3Q26 (Nov); Cisco F1Q27 (Nov, last hard Splunk comp); UBS's pending Arize checks on DT; a Databricks 2026 IPO was Octahedron's base assumption in Dec-2024 (not confirmed anywhere in the corpus).

---

## 5. Who's exposed (companies)

| Name | Layer | AI role | Latest corpus datapoint | Street stance (latest) | Key risk |
|---|---|---|---|---|---|
| **SNOW** | Analytical | AI data repository; Cortex Code / Intelligence / Analyst | **F2Q27 (09-02): product rev $1.49B +37%, FY27 guide raised to +36%, NRR 126%, RPO $9B +30%** | MS OW $300 · DB Buy $300 · Barclays EW $272 · UBS Buy · Bernstein M $250 · Redburn Sell (all pre-print) | Databricks share loss; crowded; post-print Street reaction not in corpus |
| **Databricks** (pvt) | Analytical + everything adjacent | Lakehouse → "agentic system of record"; DW $1.5B ~100% | Revenue growth ~80%, $140–175B valuation (Jun–Jul 2026) | n/a — private; DB/Jefferies/UBS all attended Summit | Private marks; rev-rec of model access; concentration of thesis in one holder's letters |
| **MDB** | Operational | Agent memory / hot working set; Atlas vector | **F2Q27 (09-01): rev $772M +30%, Atlas ~+29% (5th qtr), EA +36%, FY27 raised to +21–23%, Atlas FY27 ~27%** | Bernstein O $449 · MS OW $380 · Barclays OW $387 · UBS Neutral $350 (all pre-print) | Postgres taking new-app share; Atlas flat at 29% despite total accel. |
| **PostgreSQL** (OSS) | Operational | Default store for new AI apps; pgvector | MSFT Azure Postgres +55%, 3rd qtr of acceleration; Postgres+Foundry customers +80% | Owned via MSFT/AMZN/GOOG database lines | Deflationary to MDB; no pure-play |
| **Redis** (pvt) | Operational / cache | Low-latency state, semantic cache | UBS hyperscaler checks: "Redis and Postgres" capacity rising (07-22); Arm Performix partner | None in corpus | Corpus gap |
| **ESTC** | Search / index + obs + sec | Permission-aware context plane | **Q1 FY27 (08-27): rev $478M +15%, cRPO +21%, 37% of $100K+ customers on AI (from 21%), FY27 guide +15.2%** | UBS: "stable, nothing inflecting," 4–5x sales · Citrini positive optionality | Low growth vs group; IBM-target optionality only |
| **DDOG** | Observability | AI-native cloud consumption proxy; Bits AI | **2Q26 (08-06): rev $1.12B +36%, non-AI customers high-20s, RPO +43%, FY26 guide +30%** | MS OW $225 · UBS Buy · JPM OW Street-high · BofA Buy (all pre-print) | 13–14x sales, most crowded; post-print Street reaction not in corpus |
| **DT** | Observability | Enterprise APM + logs + Arize AI-observability/evals | **Q1 FY27 (08-05): ARR $2.14B +17%, net new ARR $85M +66% (41% organic), logs ~$200M growing >100%, NRR 110%**; UBS Buy since 06-16 | UBS Buy | Arize terms unknown in corpus; FX headwind to ARR |
| **Splunk** (CSCO) | Observability + SIEM | Log incumbent inside Cisco; agent-behavior monitoring pitch | Q4 FY26 Security +14% on Splunk on-prem; >1,000 FY26 logos; F1Q27 last hard comp | Via CSCO: JPM OW $150 · MS OW $135 · Barclays EW $123 · UBS Buy $132 | Cloud-transition drag; LakeWatch/Chronosphere cost attack |
| **New Relic** (pvt) | Observability | Full-stack APM, consumption pricing | **None in corpus** | n/a | Pricing pressure on public peers |
| **Grafana Labs** (pvt) | Observability | Open-source dashboards; GPU-fleet default | MS bus tour with DDOG/CRWV/MDB (Jun 2–4) | n/a | Substitution at AI-native accounts |

_Adjacent: [PANW](../PANW.md) (Chronosphere), [CSCO](../CSCO.md) (Splunk, Galileo, Astrix), [NOW](../NOW.md) (AI Control Tower, Workflow Data Fabric), [MSFT](../MSFT.md) (Fabric, Cosmos, Postgres), [AMZN](../AMZN.md) (Aurora/DynamoDB, Bedrock RAG attach), [ORCL](../ORCL.md) (multicloud DB, AI Vector Search), [PLTR](../PLTR.md) (ontology; UBS's preferred fresh-money name in the category)._

---

## 6. What to verify next (corpus gaps)

1. ~~MDB F2Q27 and SNOW F2Q27~~ — **RESOLVED 2026-09-03** from the company transcripts (§2.2, §2.4). Still open: the sell-side reaction notes and PT changes to both prints.
2. ~~DDOG 2Q26~~ — **RESOLVED 2026-09-03** from the company transcript (§3.2). Sell-side reactions still open.
3. **Dynatrace / Arize** — deal terms, ARR, close date; UBS said more checks were coming (2026-08-31). The Q1 FY27 call (2026-08-05) names only the BindPlane acquisition ($13M ARR), so Arize post-dates that call or was not discussed on it.
4. **Databricks Postgres (Lakebase) and LakeWatch traction** — only Octahedron's qualitative claims; no numbers.
5. **New Relic, Grafana, Redis** — no broker material. If the team wants these covered, an expert call is the only route.
6. **Confirm the source of the stack diagram** before it is cited.

---

## 7. Transcript archive (added 2026-09-03)

Full diarized earnings-call transcripts (MarketBeat / Quartr feed) now on disk, indexed for `search.py -t <TICKER> -k transcript`. Company folders were created for this purpose; none of the five has a wiki page yet.

| Ticker | Folder | Calls on disk | Newest |
|---|---|---|---|
| SNOW | [../../SNOW/transcripts/](../../SNOW/transcripts/) | 7 — Q3 FY25 (2024-11-20) → Q2 FY27 | 2026-09-02 |
| MDB | [../../MDB/transcripts/](../../MDB/transcripts/) | 8 — Q3 FY25 (2024-12-09) → Q2 FY27 | 2026-09-01 |
| DDOG | [../../DDOG/transcripts/](../../DDOG/transcripts/) | 7 — Q4 2024 (2025-02-13) → Q2 2026 | 2026-08-06 |
| DT | [../../DT/transcripts/](../../DT/transcripts/) | 6 — Q4 FY25 (2025-05-14) → Q1 FY27 | 2026-08-05 |
| ESTC | [../../ESTC/transcripts/](../../ESTC/transcripts/) | 7 — Q3 FY25 (2025-02-27) → Q1 FY27 | 2026-08-27 |

Not archived: Databricks, Redis, New Relic, Grafana Labs (private, no calls); Splunk (inside Cisco since 2024 — see [../CSCO.md](../CSCO.md) and `CSCO/transcripts/`). Fiscal calendars: SNOW and MDB end January, DT ends March, ESTC ends April, DDOG is calendar.

---

## Sources

- UBS · Karl Keirstead / Taylor McGinnis / Roger Boyd / Roddy Sultan — "The State of AI & Software" call, 2026-08-31 — [source](../../relat%C3%B3rios%20bons/2026_08_31_ubs_the_state_of_ai_software.html)
- UBS · Keirstead — MSFT 4QFY26 callback, 2026-07-30 — [source](../../relat%C3%B3rios%20bons/2026_07_30_callback_2q26_msft_ubs.html)
- BofA — MSFT 4QFY26 callback (Cosmos/Postgres/Fabric/Foundry), 2026-07-30 — [source](../../relat%C3%B3rios%20bons/2026_07_30_msft_2q26_callback_bofa.html)
- BofA · Koji Ikeda et al — Global Technology Conference wrap, 2026-06-08 — [source](../../_equity_calls/Overall/2026-06-08_BofA_conference-wrap.md)
- Jefferies · Brent Thill / Samad Samana — AI call, 2026-06-01 — [source](../../relat%C3%B3rios%20bons/2026_06_01_brent_jeff_ai_1_jun_26.html)
- Jefferies — RTYA rebalance call, 2026-06-08 — [source](../../relat%C3%B3rios%20bons/2026_06_08_jeff_rtya_rebal_8_jun_26.html)
- Octahedron Capital — 2Q26 LP call, 2026-07-15 — [source](../../relat%C3%B3rios%20bons/2026_07_15_octahedron_2q_review.html); Databricks investment deck, 2024-12-10 — [source](../../relat%C3%B3rios%20bons/Octahedron_on_DataBricks.html)
- Citrini Semis — "All Along the AI Watchtower," 2026-07-20 — via [ai-builder-toolkit.md](ai-builder-toolkit.md)
- Bernstein — "Scaling Intelligence: The Generative AI Handbook," ticker table as of 2026-06-16 — [figure transcription](../_data/figures/Bernstein_on_Gen_AI_Software.md)
- WFC — cloud / MSFT expert call, 2026-04-14 — [source](../../relat%C3%B3rios%20bons/2026_04_14_wfc_cloud_msft_14_apr_2026.html)
- Archera — cloud-strategy expert call, 2026-07-13 — [source](../../relat%C3%B3rios%20bons/2026_07_13_archera_13_jul_26.html)
- BofA · Brian Fenske, 2026-04-16 — [source](../../relat%C3%B3rios%20bons/2026_04_16_fenske_16_apr_26.html); Morgan Stanley · Tom Wigg, 2026-05-06 — [source](../../relat%C3%B3rios%20bons/2026_05_06_wigg_6_may_26.html)
- UBS · Tim Arcuri — Micron memory call (agentic workflow mechanics), 2026-05-15 — [source](../../_equity_calls/Semis/2026-05-15_Arcuri-Micron_memory.md)
- Stratechery — interview with Google Cloud CEO Thomas Kurian, 2026-04-23
- Briefings: 2026-05-08 (DDOG 1Q26), 2026-05-19 / 05-26 (SNOW-vs-Databricks share data, Redburn Sell), 2026-05-28 / 05-29 (SNOW + MDB prints), 2026-06-03 (SNOW Investor Day), 2026-06-09 (Barclays ranking), 2026-06-16 / 06-17 (DT upgrade, Databricks Summit), 2026-08-24 (internal weekly)
- Company transcripts archived 2026-09-03 (§7): SNOW Q2 FY27 (2026-09-02) · MDB Q2 FY27 (2026-09-01) · DDOG Q2 2026 (2026-08-06) · DT Q1 FY27 (2026-08-05) · ESTC Q1 FY27 (2026-08-27), plus 30 earlier calls back to 2024-11
- Transcripts: CSCO Q4 FY24 → Q4 FY26 (Splunk/Observability); PANW Q1 FY26 + Q3 FY26 (Chronosphere); NOW Q3'24 + Q2'26; MSFT Q4 FY24 / Q3 FY25 / Q1 FY26 / Q4 FY26; ARM Q1 FY27 (Performix); MU Q4 FY25 (vector DB / KV-cache NAND); AMZN Q2'26 (via AMZN page)
- Wiki pages: [../CSCO.md](../CSCO.md), [../MSFT.md](../MSFT.md), [../AMZN.md](../AMZN.md), [../ORCL.md](../ORCL.md), [../PLTR.md](../PLTR.md), [../PANW.md](../PANW.md), [tokenmaxxing.md](tokenmaxxing.md), [ai-builder-toolkit.md](ai-builder-toolkit.md), [internal-weekly-meeting.md](internal-weekly-meeting.md)

## Changelog
- 2026-09-03 (later) — 35 earnings-call transcripts archived to `SNOW/`, `MDB/`, `DDOG/`, `DT/`, `ESTC/` `transcripts/` folders (MarketBeat/Quartr; search index rebuilt); §2.2, §2.4, §2.7, §3.2, §3.3 and the scorecard gained the five newest prints; §6 items 1–2 marked resolved; §7 added. Superseded scorecard "latest datapoint" values (kept here): SNOW F1Q27 product rev +34% / FY27 guide +31% → F2Q27 +37% / +36%; MDB F1Q27 Atlas +29.4% / FY27 +19.5% → F2Q27 Atlas ~29% / FY27 +21–23%; DDOG 1Q26 +32% / FY26 high-end +27% → 2Q26 +36% / FY26 +30%; ESTC FY27 guide ~14% (Citrini, 07-20) → +15.2% (company, 08-27).
- 2026-09-03 — page created from the corpus on request (reference: pasted AI-stack diagram, source unconfirmed). All figures additive; no prior wiki number, rating, PT or thesis superseded. Known post-corpus events not reflected at creation: MDB F2Q27 (09-01), SNOW F2Q27 (09-02), DDOG 2Q26 (Aug).
