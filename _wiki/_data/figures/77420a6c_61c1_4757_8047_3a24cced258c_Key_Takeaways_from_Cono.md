# Figure transcription — Key_Takeaways_from_Conor_OMaras_recent_Management_Meetings_across_ASIA (1).pdf

Pages covered: 27, 28, 29, 30, 31, 33, 34, 35, 36, 37, 41.
Machine transcription of figure/exhibit pages (notes document embedding Jefferies-style exhibit cards; personal notes in Portuguese around them). Transcribed faithfully, no interpretation.

## p.27 — COMPUTEX INTEL: SHOWS 1:1 CPU TO GPU FOR INFERENCE 150K AGENT RACK

Exhibit card (embedded slide with three Intel Computex screenshots on right):
- **CPU APPROACHING PARITY.** Intel said "We are seeing the ratio of 1 CPU to 8 GPU or is coming closer to parity. Whereas AI inference a year ago was 7 to 1 GPU based, now with agents the CPU is near parity based on the workload shown below. This is a mix of efficiency and performance cores."
- **HIGHEST DENSITY RACK EVER.** "The impact is huge when we multiply this by millions of queries per day. Each Xeon 6 processor has up to 288 cores or 567 cores per 2 socket server. From a rack scale perspective that's over 36000 cores per 32Us of compute space."
- **CAN RUN 150K AGENTS.** Highest density per rack ever; this rack can run up to 150K agents.
- **GOOD ROI.** "This means the very expensive GPUs that you have bought CIOs can have higher utilization."
- Screenshot caption fragment: "...to 288 cores. That's 576 cores per two socket server." [Intel Computex presentation screenshots]
- No printed source line on the exhibit.

Surrounding notes (author's, Portuguese): "a way to play cpu"; "apresentação / computex / intc"; "intel parece menos capacity constraint do que a amd (supresdo)"; "laptop e pc foi pro 18A (novo node)" — "liberou capacidade pros DC servers", "melhorou yield do 18A"; "acha que intel vai ganhar share em server"; "estao vendo momentum em quipment"; "esta mt bem no core business (nao em foundry)".

## p.28 — AI CPU TO GPU RATIO INCREASING INTEL EVEN SELLING LOWER SPEC CHIPS

Exhibit card (text bullets):
- **CPU IS ORCHESTRATION LAYER.** In recent months Intel have seen clear signs the CPU is reinserting itself as an indispensable foundation of the AI era. CPUs now serve as the orchestration layer and critical control plane for the entire AI stack. Evident in the demand profile for our products.
- **AI CPU TO GPU RATIO 1x2 or 1x1.** Intel says the ratio of CPU to GPU was 1 to 8 for training, now its 1 to 4 for inference and as you get into agentic and multi agent, it's one it. Going forward it's going to become a significant part of the AI TAM. Inspectrum say Vera Grace is already 1 CPU v 2 GPU. Hard to become 1 to 1. But ASICs were 1 v 8 then 1 v 4 and now 1v 2 due to inference and agentic AI demand.
- **XEON SERVER CPU DEMAND STRONG.** Intel demand continues to run ahead of supply especially for Xeon server; expects sustained momentum this year and next.
- **INTEL SELLING LOWER SPEC CHIPS.** Demand so strong customers are buying everything — including would-be scrap or low-expectation edge chips; Intel "bins" them down, labels as lower-spec SKU, and sells them anyway.
- **ODM GETTING MORE ALLOCATION FROM INTEL.** ODM said will be using more Intel as they are more aggressive on product offering and can expand capacity more. Their technical roadmap looking more attractive. Intel 5-7% up for Intel. Intel was 50% last year, 55% this year and 60% 2027.

Notes: "amd — mt shortage, tome cuidado com o print; pq provavelmente vao falar de mt backlog de demanda, mas podem guide light por conta dos shortage; o que eh kinsus e ITEQ?"

## p.29 — AMD CAPACITY CONSTRAINED TRYING TO ALLOCATE 4NM FOR GENOA

Exhibit card:
- **1M VENICE CPUS NO CAPACITY AT 3NM.** Sherman estimates Venice CPU's total volume under ASE's FoCoS to nearly reach 1mn. AMD
- **AMD CHANGING ITS PRODUCT MIX IN FAVOUR OF GENOA SERVERS.** Venice 2nm also tight. Allocation away from PC to 4nm Genoa server to increase allocation to server CPU.
- **KINSUS AMD 10% GROWTH.** Kinsus has 40% market share in AMD general servers and says it is seeing this business grow only at 10% suggesting capacity constraints.
- **ITEQ CAPACITY CONSTRAINED.** ITEQ has 60% market share from AMD CPU. Intel 30-40% share. Running 15-20% below. Should be running 90-95% utilization only at 75%.

Two embedded small exhibits (mostly too small to fully read):
- "Figure 17: AMD server CPU is better for Agentic AI workload compared to Intel" — table Intel (Diamond Rapids, Expected H2 2026, 192/192 core (SMT), Intel 18A, 16-ch DDR5 MRDIMM-12800 (target/speculated), PCIe6 + CXL 3.0 + accelerators (QAT/DLB/IAA/DSA), Strong IO/memory ambition but no SMT + no NVLink-class GPU link makes it middling for both) vs AMD (Venice Classic (SP7), Release Expected Q3 2026, 96/192 (SMT), TSMC N2, 16-ch DDR5 MRDIMM-12800, ~16TB/s [partially illegible], Infinity Fabric 1.8TB/s bidir to MI455X, 128+ PCIe6 + CXL 3.1, Reasoning-focused x86 head-node, high per-core + big per-core memory BW). Source: AVGO, Fubon Research [as printed].
- "Figure 16: CPU core count, ISA, Performance per watt are most important indicators" — table of metrics (Per-core performance Medium; Core count Critical; Memory bandwidth & capacity High; Cache design/size High; Performance per watt Critical [partially illegible]; PCIe generation & lane count High; ISA Critical; NUMA latency Medium) with explanations [small text, largely illegible]. Source: Vivek's Newsletter, Fubon Research [as printed].

Notes: "LENOVO DELL E HP sao quem tem os chips — os clientes normais sao empresas e pequenas hypersclers; mas as grandes hyperscalers estao indo atras delas. c ct vao continuar indo atras delas em 2026."

## p.30 — HYPERSCALERS WILL TAKE ANY SERVER CPUS THEY CAN GET + LENOVO + DELL + HP / GUC HAS SECURED MORE CAPACITY FOR GOOGLE CPU AT TSMC

Exhibit card 1:
- **CPU GROWTH MORE THAN 20% THIS YEAR AND NEXT. SUPPLY CHAIN WASN'T PREPARED FOR THIS.** Agentic AI has changed server growth expectations from mid single digit 6 months ago to over 20% now according to Inspectrum who can't remember the last time server CPU were in shortage; unit growth 20% this year and next. Hyperscalers scrambling for any kind of compute they can get.
- **INTEL SEEING STRONG UPTICK SERVER CAN DRIVE CONSUMER CPU ADOPTION OF 18A.** Intel shifting laptop CPUs for 18A. More customer requests on 18A could increase the yield. Should be giving more allocation to server. AMD in same situation giving more allocation to servers. Both are only fulfilling 80-90% of demand.
- **DELL AND LENOVO IN GOOD SHAPE AS HAVING CPU SERVER LTA ALLOCATION IS VALUABLE.** Traditional server makers all have LTAs; allocations very valuable now. Lenovo and Dell have LTAs with AMD and Intel. Hyperscalers will have to come to them for more CPUs. Positive for Lenovo and Dell.
- **QUALCOMM MEDIATEK AND GUC WILL NOT GIVE UP ALLOCATIONS AT TSMC FOR 2NM AND 3NM.** Not easy to squeeze Mediatek and Qualcomm for 3nm; both will have ASIC allocations they won't allow cuts. GUC also looking for allocations for Google CPU and working with Tesla on AI chips too. AMD will struggle to see upside in leading edge nodes from any decline in smartphone sales.
- **ANY COMPUTING POWER IS GOOD. AMAZON TRANIUM 4. QUALCOMM.** Anybody with any solution is in a good position; performance doesn't matter much. Tranium and Qualcomm have a good chance as they have allocations. HBM allocation is an issue, there may be shortages. Qualcomm not so clear if they have allocations for HBM. CPUs are very valuable components.

Exhibit card 2 — GUC HAS SECURED MORE CAPACITY FOR GOOGLE CPU AT TSMC:
- **GUC SEEING MORE UPSIDE IN TURNKEY FROM GOOGLE CPU.** More capacity secured for CPU projects; forecast currently remains at 2mn units. Main revenue driver will be the CPU turnkey. GM will be down from last year 25% dollar due to CPU. Turnkey were expecting 75% now but much stronger now on back of demand for Google CPU.
- **ALREADY PLANNING NEXT GENERATION CPU WITH TSMC.** Next CPU will tape out next year. GUC negotiated with TSMC for capacity. Google raised demand for 2026 from late 2025 — very late. Now negotiating wafer support for TSMC for 2027 this March. Demand for wafers will be double at least.
- **ALREADY SECURED CAPACITY FOR NEXT PROJECT.** For Google CPU revised up from 1m to 2mn units. Ratio of CPU to TPU revised up from 1:4 to 1:2; CPUs in severe shortage, clients want to secure as many as possible. For 2027 Fubon Google CPU shipment expected 3-6mn units based on different ratios and fulfill rates. Their 2027 assumption factors in 3mn units of Google CPU; reaching 6mn depends on GUC securing capacity. TSMC sees Google as very important customer. 3nm chip. Revenue late next year. Takes 12-18 months from NRE to turnkey.

## p.31 — HBM MARGINS WILL RISE FASTER THAN CONVENTIONAL MARGINS

Exhibit card:
- **HBM ISN'T FIRST PRIORITY ANYMORE FOR DRAM.** Conventional DRAM is the no 1 focus. Until end of last year for 3 years it was HBM. Agentic AI most important; HBM isn't the only topic for memory anymore. In April memory makers were thinking to continue to invest in TSV for HBM; now reduced TSV, all front end investment for wafer capacity.
- **HBM SPEEDS DON'T MATTER WHEN ALLOCATIONS ARE TIGHT.** Nvidia will take any speed of HBM just to make numbers; doesn't matter if 8GBps or 11Gbps, Inspectrum say.
- **CONVENTIONAL MARGINS HIGH BUT HBM WILL GO UP MORE.** Memory makers will raise contract prices on HBM prices. Q425 server DDR5 under 50 cents now $2 per gigabit. Early Q3 last year LTA was a different situation when server was $0.3. First time in past 3 years it's about conventional buyers, no longer about HBM conversion — it's the reverse. They are now pressuring.
- **SAMSUNG SAYS HBM AND DRAM MARGINS SHOULD BECOME SIMILAR IN 2027.** HBM wafer penalty more normalised. Need to drive LPDDR5; HBM margins could be similar. Conventional margin can grow next year but HBM better priced next year. Gap will narrow. Margin improvement is more in HBM.
- **THE SITUATION HAS INVERTED ITS NOW HBM CUSTOMERS STRUGGLING FOR ALLOCATIONS.** HBM buyers told if you don't pay more we will focus on conventional and not convert more to HBM as agentic AI demand is so strong. Q3 HBM this year is LTA still but will need to go up.
- **HBM4 PRICE WILL BE DOUBLE OF HBM 3E.** HM3e price can double this year and that is still low. HBM4 price should be 90-100% more compared to last year LTA. LTA still under negotiation.

Notes: "memory: 1- generalserver, 2- hbm"; "strctural bull case ⇒ LTA vai mudar a estrutura de longo prazo — ele nao concorda. LTA = call options: 5 anos de contrato, 1yer pre-pay contratc, volume fixed."

## p.33 — NO PUSHBACK FROM HYPERSCALERS ALLOCATION IS THE PRIORITY

Exhibit card:
- **PROCUREMENT MANAGERS CANT PUSH BACK ON PRICES.** All about allocations for servers, PC and phones. Nobody expected such a high price. Agentic AI and inference need to maximize computing power; purchasing managers focused on finding compute then allocating across needs.
- **SAMSUNG SAYS NO PUSHBACK FROM HYPERSCALERS.** Some articles suggest they are willing to spend up to 30-35% [of operating cashflow] on memory; Samsung says mid teens to 20% range right now. Still room for price increase, no pushback.
- **MEMORY MAKERS ARE ALLOCATING DRAM GB BUDGETS THEN HYPERSCALERS DECIDE THE MIX.** Memory makers allocate GB then hyperscalers decide which products within that. Hyperscalers allocate some 128GB, some 64GB, some could go down to 32GB.
- **$1.5-2TRN OF SALES NEXT YEAR.** Inspectrum see high 20s bit growth [this year] and mid teens next year in bit growth. But 2028 major concern is on the price. Can the whole world pay USD 1.5-2trn in memory combined DRAM NAND. This is why they need LTAs.

Notes: "cxmt — grande parte deve ir p hbm dentro da china; estao sold out; nao deve trazer problema de oversupply p US."

## p.34 — CXMT GAINING TRACTION BUT ALSO SOLD OUT

Exhibit card:
- **CXMT ALREADY SOLD OUT.** Inspectrum says CXMT is sold out already. Anybody with volumes does well. CXMT will continue to gain share. Ramp depends on government policy — have to make sure 70% domestic equipment supply. CXMT LP4X and LP5x to phones in China and PC DDR5 in China for a while. Also local module makers but size is small. Nobody care about quality or yield. They have Lenovo and HP also engaging. Dell working on this; CXMT may not need Dell now, already sold out.
- **ODM LOOKING AT CXMT FOR SOME SERVER MEMORY.** ODM expert says Samsung Hynix and Micron. Expecting shortage at least 2028. 20-30% shortage at least due to hyperscaler unpredicted demand from AI. TSMC isn't able to respond to the sudden demand. Wistron is looking at CXMT and trying to reconfigure the specs to fit the real supply. Some clients need the highest spec, some may split between 128GB and 64GB.
- **CXMT GETTING INTO SERVERS WITH HIGH YIELD.** ODM expert says he is using CXMT for server for Chinese hyperscalers. Some US hyperscalers will use low end CXMT. Within 1-2 years can use CXMT for servers. CXMT fails in long reliability 20-30K hours but passed all other tests. DDR4 is OK, DDR5 still under testing. CXMT memory yield is 98% already and they are maxed out at capacity. CXMT is 10% lower but its not about price — supply, financial stability and quality (suffered from low quality). US hyperscalers and government OK with having some memory from China. Same with PCB and power supplies. CPU and GPU are different, those are more concerns.
- **LIMITED IMPACT OF CXMT ON DRAM SAMSUNG THINKS.** Samsung acknowledges even CXMT is making good profits but their cost structure is totally different; still focused on legacy part of industry and dependent on demand; price is attractive for them to make it profitable. Significant margin differences. Price increases will be centred on servers, don't see them much in servers [as printed]. Not sure if China can become totally self sufficient in memory.

Notes: "nand — kioxia >> sandisk; produto da kioxia eh melhor p agentic."

## p.35 — SIMO THINKS NAND IN SHORTAGE UNTIL 2028 AT LEAST / KIOXIA GP SLC: AGENTIC AI LEADS TO SURGE IN I/O & LOWER LATENCY

Exhibit card 1 (SIMO):
- **SIMO GAINING SHARE ON OUTSOURCING FROM FLASH MAKERS.** Largest merchant, 20% of overall market; rest owned by flash makers who want to outsource more. Micron exited. Samsung outsourcing eMMC to SIMO with more share gains coming. Latest generation PCIe 5 SSD market share is 50% was 30%. PCIe5 more complicated, on 6nm gives best performance and lowest power vs Kioxia Transcend Sandisk Kingston. Sub 7 watts vs others 9-11 watts. 4 channel PCIe5 have 4 flash makers: Hynix Samsung TCL and QLC [as printed]. HBM and DRAM are the main focus of memory makers, they need to outsource more in NAND.
- **SIMO THINKS NAND IN SHORTAGE UNTIL 2028.** SIMO don't think NAND supply will alleviate until 2028. Outsourcing gives faster time to market with better solutions and cheaper. 6nm nano is $15-20m. Dedicated firmware engineers are 50, used to be 5-10. Performance much higher; NAND weaker as stack higher — with more QLC it gets weaker. SIMO understands QLC better than others.
- **SIMO HUGE INTEREST IN QLC ENTERPRISE SSD.** TCL and QLC NAND [as printed]. TLC for high performance, QLC high capacity to store and read for inference. Huge interest in QLC SSD. Waiting for next generation 3D NAND; need 2TB QLC NAND. Kioxia and Sandisk have it already; Samsung and Hynix late this year. QLC less robust if written a lot; mostly reading. Compute SSD is TLC NAND for more read write. Warm storage QLC perfect, lower cost higher capacity.
- **KVCACHE ICMS MORE COMPUTE SSD NEEDED.** Nvidia comments drove up QLC interest a lot. Had expected ramp 2H26 but got pulled forward to Q2. Still talking about 5-10% of sales, off a much bigger base. QLC bigger in 2027 2208 [as printed] as get more availability. 2 Tier 1 customers in the US and China flash maker storage solution provider or CSP. Some think Everpure. Have 6 customers. 5 CSPs deploying SSDs with SIMO — 2 in US, 3 in China have end customer validation.

Exhibit card 2 (KIOXIA GP SLC), with three Kioxia slide images on right:
- **AGENTIC AI NEEDS BETTTER LATENCY & I/O.** Agentic AI led to huge increase in iterative interfaces requiring granular and frequent data access; latency and I/O improvements crucial.
- **KIOXIA GP SERIES 10M 2006 100M 2027 [as printed].** Roadmap is 10M IOPs based on PCIe 6 in 2026 and 100M in 2027 based on PCIe 7. KIOXIA GP series announced March 2026 using KIOXIA XL-FLASH, developed for ultra low latency for NVIDIA Storage-NEXT architecture. Second generation sampling 2027. SSD with PCIe interface for direct connection to the GPU. Includes custom SOC for 512byte. Breakthrough in latency and granularity.
- **COMPLEMENT TO HBM.** SSD enables it to function as an extension to HBM.
- **KIOXIA THINKS BETTER THAN HBF.** Better solution than HBF, which is why it's not pushing it. Second generation should be mass production, will take time to gain share. Installing equipment for migration now.
- **THIS IS SLC FOR READ PERFORMANCE.** SLC based. Vector database on RAG need low latency and higher random read performance, optimal for SLC/MLC.
- Kioxia slide images: "Expansion of AI Inference Systems and Demands on SSD/NAND"; "KIOXIA GP Series — High Performance SSD with XL-Flash / Compatible with NVIDIA Storage-Next, Super High IOPS SSD (100M+ IOPS, ultra-fast and low-latency…)"; "KIOXIA's Path to 100 Million IOPS — 2025: 3M, 2026: 10M, 2027: 100M, Enabled by XL-FLASH."

## p.36 — YMTC RAMPING WITH LOTS OF INTEREST FROM NEW CUSTOMERS

Exhibit card:
- **SIMO SAYS YMTC RAMPING UP FAST.** Most aggressive in expanding capacity. 50-60% bit growth and next year the same; could overtake Samsung in the coming years. Smartphone OEMs Apple and Samsung have their own controllers; others are module makers using YMTC a lot. As Chinese capacity has increased, have seen a surge in Chinese module makers.
- **APPLE TALKING TO YMTC.** YMTC will gain share as ramping aggressively; supply demand tight so many brands including Apple are talking to them.
- **YMTC NAND MORE FLEXIBLE ON TERM AIMING TO GET INTO SSD.** ODM says YMTC offering is very flexible payment terms are different. YMTC mature products OK but new innovations can only do some small samples. Trying to get into eSSD AI servers and HPC but not ready yet. Price is much higher but quality and reliability is more important.
- **CHINESE FINE FOR GENERAL SERVERS.** Servers sold to Dell HP Lenovo no problem to use Chinese memory; AI servers is different. Chinese fine for general servers. Have done servers for 15-20 years, trying to use more Chinese more affordable sources. Must be qualified in advance. PCB memory passives using all of them.

Embedded chart: "Global NAND Market Share by Revenue (Q4 2024 – Q4 2025)" — stacked bars Q4 2024, Q1 2025, Q2 2025, Q3 2025, Q4 2025; legend: YMTC [top segment], SanDisk, KIOXIA, Micron, SK hynix, SAMSUNG. Legible values: YMTC ~8%/8%/9%/10%/11%; next segment 11%/13%/12%/12%/13%; 17%/17%/14%/16%/16% [partially illegible]; 13%/15%/13%/12%/15%; [SK hynix segment illegible]; Samsung 31%/31%/32%/32%/27%. Source: Counterpoint Research Memory Tracker and Forecast, Q4 2025 [as printed].

## p.37 — DAIFUKU ADDING CAPACITY AS TAIWAN KOREA CHINA ALL UP DOUBLE DIGITS

Exhibit card (screenshot banner: "You are viewing Conor O'Mara - Jefferies's screen"):
- **300BN IN ORDERS UP FROM 220BN TAIWAN & KOREAN CLIENTS DRIVING MOMENTUM.** Taiwanese and Korean customers driving orders this year and next. Customers scheduled for this year and next year with clear visibility that momentum continues into next. Demand will continue for at least 2 more years if not 3. Also seeing China still strong for memory and logic.
- Taiwan mainly logic Y103bn up from Y73bn. Y80bn from the front end; packaging Y20bn, last year packaging was Y23bn.
- South Korea Y74bn up from Y48bn +40% mostly Yongyin Fab 1.
- China Y100bn up from Y90bn.
- Size of one project is Y10bn.
- **CUSTOMERS BECOMING MORE CONFIDENT POSITIVE OUT TO MID 2028.** Daifuku implied sentiment for fab capex among major semiconductor industry customers has become better than three months ago. Customers keen to have more capacity.
- **INCREASING CAPACITY BY 30% MAY INCREASE MORE.** Daifuku completed construction of its new factory building for cleanroom systems for the semiconductor sector in April 2026, increasing domestic production capacity for the cleanroom business by 30%. Can get to sales of Y350bn after this capacity. Will boost growth of semis, may do a next round of investment (in planning stage). Want to complete installation end of 2028 or latest 2029 for more capacity. Have a Y1trn sales target of which semis are Y400bn. May also do acquisitions.
- **LABOUR HAS BEEN THE BOTTLENECK.** For Daifuku to deliver, it all depends on fab construction labour. Japan also has labour shortage. Construction taking more time in the US also.

Notes ("Sherman" section): CPU — raise pricing again no 2S26; ja auemntaram 15-20%; esperam mais 15-20% no 2S26; Intel ainda esta mt constraint; AMD esta consraint pela TSMC. 2027 — TSC vai priorizar AMD vs Intel; mas o gap da tsmc de supply vs demand vai aumentar em 2027; no consumer segment,

## p.41 — AMD MI450 STILL HAS ISSUES BUT HAS LARGE ORDER BACKLOG

Exhibit card:
- **AMD AGGRESIVELY BOOKING TSMC FOR 2027.** Sherman says AMD is aggressively booking TSMC's foundry capacity in 2027 to secure its supply for MI450 and MI500 series. AMD are making downpayments $10bn for Helios racks.
- **AMD 450 HELIOS STILL THERMAL ISSUES.** Titan thinks Helios mass production Q4 this year soonest. Still issues on switch thermal and power. Some channels say could be delayed to Q117 [as printed]. Wiwynn says everything is on schedule. CSP will decide the ODM, normally those with longer term relationships. Eg Microsoft should allocate to Hon Hai. META better with Wiwynn. Cost of MI450 Helios is over $5mn.
- **AMD AI RACKS ARE OK BUT STILL ISSUES.** ODM said 90% of shipments are Nvidia and 10% AMD. Have suffered a lot from MI300. Pushed AMD a lot of MI400 and MI450. Still some issues in hardware software integration and electrical but will be able to launch Helios on time. Specs and pricing of AMD is more attractive; performance slightly better and pricing lower; hyperscalers want to diversify sourcing. Also want to have ASICS and TPU.
- **SIGNIFICANT CUSTOMER INTEREST.** Counterpoint says beyond the known five-year 6GW partnerships with Meta and OpenAI (which involved AMD warrants), Anthropic has reportedly signed an agreement to use AMD's MI450 chips due to broader supply constraints.
- **AVC SAYS AMD STILL 30K BUT COULD BE LATE.** Very aggressive forecast from Q4; forecasts still in place. Doing a reference design. More conservative on whether their ramp will be smooth. Not seeing any thermal issues. Methodology easy to get right, hard to get all components right the first time. Orders for next year stable at 30K; hyperscalers want another supplier. Sovereign AI don't have chip capabilities, their contracts would come via Oracle.

Notes: "LTAs; prepayement, deposits, etc. vai pra um banco ou vai direo pras cias de memoira? qual %? — 1year pre-payment ou 2; deve ir p uma conta antes; pq n aparece no balance sheet? — tao so começando"; "cpu narrative weak post — price hike driven por demand e supply".
