# Read-through map — supply chain & substitutes

_Generated 2026-07-03 · curated high-confidence edges from `_data/graph.json` (177 supply links, 22 compete links). A datapoint on a **supplier** reads through to its **customers** (and vice-versa). Edit the JSON to extend; rebuild: `py _wiki/_tools/build_readthrough.py`._

| Ticker | ⬆ Suppliers (upstream) | ⬇ Customers (downstream) | ⚔ Competes |
|---|---|---|---|
| **AAOI** | AIXA (MOCVD tools) | AMZN (optical transceivers), MSFT (optical transceivers) | — |
| **AAPL** | ARM (IP), TSM (foundry) | — | — |
| **ADI** | — | NVDA (power (Empower)) | — |
| **ADVANTEST** | — | SAMSUNG (ATE test), TSM (ATE test) | — |
| **AGX** | — | AMZN (EPC gas power) | — |
| **AIXA** | — | AAOI (MOCVD tools), COHR (MOCVD tools), LITE (MOCVD tools) | — |
| **AKAM** | — | — | NET (edge/CDN) |
| **ALAB** | TSM (foundry) | AMZN (PCIe/CXL), MSFT (scale-up fabric), NVDA (retimers/fabric) | — |
| **AMAT** | — | INTC (WFE), MU (WFE), SAMSUNG (WFE), SKHYNIX (WFE), SMIC (WFE), TSM (WFE) | LRCX (WFE overlap) |
| **AMD** | ARM (IP), CDNS (EDA), MU (HBM), SAMSUNG (HBM), SKHYNIX (HBM), SNPS (EDA/IP), TSM (foundry) | CRWV (MI GPUs), META (MI GPUs), MSFT (MI GPUs), OPENAI (MI GPUs), ORCL (MI GPUs), SANM (ZT rack integration) | INTC (server CPU), NVDA (AI accelerators) |
| **AMZN** | AAOI (optical transceivers), AGX (EPC gas power), ALAB (PCIe/CXL), AVGO (networking), CEG (nuclear PPA), CIEN (DCI/optical), COHR (optical), CRDO (AEC/connectivity), DELL (AI servers), ETN (electrical/switchgear), GEV (grid/power equip), GLW (optical fiber), HPE (AI servers), KIOXIA (NAND), LITE (optical), MRVL (custom ASIC (Trainium)), NVDA (GPUs), PWR (grid construction), SANM (EMS integration), SMCI (rack integration), SNDK (NAND/SSD), STX (nearline HDD), TLN (nuclear PPA), VST (merchant power), WDC (nearline HDD), WMB (gas midstream) | ANTHROPIC (AWS Trainium compute) | — |
| **ANET** | COHR (optical), LITE (optical) | — | CSCO (AI networking) |
| **ANTHROPIC** | AMZN (AWS Trainium compute), GOOG (TPU compute), NVDA (GPUs) | — | OPENAI (frontier models) |
| **AOSL** | — | NVDA (power MOSFET (800V)) | — |
| **APH** | — | NVDA (interconnect/busbar) | — |
| **ARM** | CDNS (EDA), SNPS (EDA) | AAPL (IP), AMD (IP), AVGO (IP), MEDIATEK (IP), NVDA (CPU IP), QCOM (CPU IP) | — |
| **ASML** | — | INTC (litho), MU (litho), SAMSUNG (litho), SKHYNIX (litho), SMIC (DUV), TSM (EUV/DUV litho) | — |
| **AVGO** | ARM (IP), CDNS (EDA), MU (HBM), SKHYNIX (HBM), SNPS (EDA/IP), TSM (foundry) | AMZN (networking), GOOG (custom ASIC (TPU)), META (custom ASIC), MSFT (custom ASIC), ORCL (networking) | MRVL (custom ASIC), NVDA (merchant vs custom ASIC) |
| **BE** | — | GOOG (on-site fuel cells), NBIS (fuel cells) | — |
| **BESI** | — | INTC (advanced packaging), TSM (hybrid bonding) | — |
| **CDNS** | — | AMD (EDA), ARM (EDA), AVGO (EDA), INTC (EDA), NVDA (EDA), QCOM (EDA), TSM (EDA) | SNPS (EDA) |
| **CEG** | — | AMZN (nuclear PPA), MSFT (nuclear PPA) | VST (merchant power) |
| **CIEN** | — | AMZN (DCI/optical), GOOG (DCI/optical), MSFT (DCI/optical) | — |
| **COHR** | AIXA (MOCVD tools) | AMZN (optical), ANET (optical), GOOG (optical), MSFT (optical), NVDA (optical/InP) | LITE (optical/InP) |
| **CRDO** | TSM (foundry) | AMZN (AEC/connectivity), MSFT (connectivity), NVDA (AEC/SerDes) | — |
| **CRWV** | AMD (MI GPUs), NVDA (GPUs) | MSFT (neocloud compute), OPENAI (neocloud compute) | — |
| **CSCO** | — | — | ANET (AI networking) |
| **DELL** | NVDA (GPUs) | AMZN (AI servers), MSFT (AI servers) | HPE (AI servers), SMCI (AI servers) |
| **DISCO** | — | SAMSUNG (dicing/grinding), TSM (dicing/grinding) | — |
| **ETN** | — | AMZN (electrical/switchgear), MSFT (electrical) | — |
| **FLEX** | — | NVDA (power/EMS + cooling) | — |
| **FSLY** | — | — | NET (edge/CDN) |
| **GEV** | — | AMZN (grid/power equip) | — |
| **GLW** | — | AMZN (optical fiber), META (optical fiber (LTA)), NVDA (optical fiber) | — |
| **GOOG** | AVGO (custom ASIC (TPU)), BE (on-site fuel cells), CIEN (DCI/optical), COHR (optical), MRVL (optical DSP), NVDA (GPUs), SNDK (NAND/SSD), STX (nearline HDD), WDC (nearline HDD) | ANTHROPIC (TPU compute) | — |
| **HPE** | NVDA (GPUs) | AMZN (AI servers) | DELL (AI servers) |
| **IFX** | — | NVDA (power semis (800V)) | — |
| **INTC** | AMAT (WFE), ASML (litho), BESI (advanced packaging), CDNS (EDA), KLAC (process control), LRCX (WFE), SNPS (EDA/IP) | — | AMD (server CPU), TSM (foundry) |
| **KIOXIA** | — | AMZN (NAND), MSFT (NAND), NVDA (NAND (Super IO)) | SNDK (NAND) |
| **KLAC** | — | INTC (process control), MU (process control), SAMSUNG (process control), SMIC (process control), TSM (process control) | — |
| **LITE** | AIXA (MOCVD tools) | AMZN (optical), ANET (optical), MSFT (optical), NVDA (optical) | COHR (optical/InP) |
| **LRCX** | — | INTC (WFE), MU (NAND/HBM WFE), SAMSUNG (etch/dep), SKHYNIX (WFE), TSM (etch/dep) | AMAT (WFE overlap) |
| **MEDIATEK** | ARM (IP), TSM (foundry) | — | — |
| **META** | AMD (MI GPUs), AVGO (custom ASIC), GLW (optical fiber (LTA)), NVDA (GPUs), SNDK (NAND/SSD), STX (nearline HDD), WDC (nearline HDD) | — | — |
| **MP** | — | NVDA (rare-earth magnets) | — |
| **MRVL** | TSM (foundry) | AMZN (custom ASIC (Trainium)), GOOG (optical DSP), MSFT (custom ASIC (Maia)) | AVGO (custom ASIC) |
| **MSFT** | AAOI (optical transceivers), ALAB (scale-up fabric), AMD (MI GPUs), AVGO (custom ASIC), CEG (nuclear PPA), CIEN (DCI/optical), COHR (optical), CRDO (connectivity), CRWV (neocloud compute), DELL (AI servers), ETN (electrical), KIOXIA (NAND), LITE (optical), MRVL (custom ASIC (Maia)), NVDA (GPUs), SMCI (rack integration), SNDK (NAND/SSD), STX (nearline HDD), WDC (nearline HDD) | OPENAI (Azure compute) | — |
| **MU** | AMAT (WFE), ASML (litho), KLAC (process control), LRCX (NAND/HBM WFE), TOKYOELEC (WFE) | AMD (HBM), AVGO (HBM), NVDA (HBM/LPDDR) | SKHYNIX (HBM) |
| **NBIS** | BE (fuel cells), NVDA (GPUs) | OPENAI (neocloud compute) | — |
| **NET** | — | — | AKAM (edge/CDN), FSLY (edge/CDN) |
| **NVDA** | ADI (power (Empower)), ALAB (retimers/fabric), AOSL (power MOSFET (800V)), APH (interconnect/busbar), ARM (CPU IP), CDNS (EDA), COHR (optical/InP), CRDO (AEC/SerDes), FLEX (power/EMS + cooling), GLW (optical fiber), IFX (power semis (800V)), KIOXIA (NAND (Super IO)), LITE (optical), MP (rare-earth magnets), MU (HBM/LPDDR), NVT (power+cooling (CDU)), NVTS (GaN/SiC (800V)), ON (SiC power), POET (optical engine/CPO), POWI (power-conversion ICs (800V)), SAMSUNG (HBM/foundry), SKHYNIX (HBM), SNPS (EDA/IP), TEL (connectors), TSM (foundry N3/N2 + CoWoS), TXN (power), VRT (power+cooling (800VDC)), WOLF (SiC (800V)) | AMZN (GPUs), ANTHROPIC (GPUs), CRWV (GPUs), DELL (GPUs), GOOG (GPUs), HPE (GPUs), META (GPUs), MSFT (GPUs), NBIS (GPUs), OPENAI (GPUs), ORCL (GPUs), SMCI (GPUs), TSLA (GPUs) | AMD (AI accelerators), AVGO (merchant vs custom ASIC) |
| **NVT** | — | NVDA (power+cooling (CDU)) | — |
| **NVTS** | — | NVDA (GaN/SiC (800V)) | — |
| **ON** | — | NVDA (SiC power) | — |
| **OPENAI** | AMD (MI GPUs), CRWV (neocloud compute), MSFT (Azure compute), NBIS (neocloud compute), NVDA (GPUs), ORCL (OCI compute) | — | ANTHROPIC (frontier models) |
| **ORCL** | AMD (MI GPUs), AVGO (networking), NVDA (GPUs) | OPENAI (OCI compute) | — |
| **POET** | — | NVDA (optical engine/CPO) | — |
| **POWI** | — | NVDA (power-conversion ICs (800V)) | — |
| **PWR** | — | AMZN (grid construction) | — |
| **QCOM** | ARM (CPU IP), CDNS (EDA), SNPS (EDA/IP), TSM (foundry) | — | — |
| **SAMSUNG** | ADVANTEST (ATE test), AMAT (WFE), ASML (litho), DISCO (dicing/grinding), KLAC (process control), LRCX (etch/dep), TOKYOELEC (WFE) | AMD (HBM), NVDA (HBM/foundry) | SKHYNIX (HBM/DRAM), TSM (foundry) |
| **SANM** | AMD (ZT rack integration) | AMZN (EMS integration) | — |
| **SKHYNIX** | AMAT (WFE), ASML (litho), LRCX (WFE), TOKYOELEC (WFE) | AMD (HBM), AVGO (HBM), NVDA (HBM) | MU (HBM), SAMSUNG (HBM/DRAM) |
| **SMCI** | NVDA (GPUs) | AMZN (rack integration), MSFT (rack integration) | DELL (AI servers) |
| **SMIC** | AMAT (WFE), ASML (DUV), KLAC (process control) | — | TSM (foundry) |
| **SNDK** | — | AMZN (NAND/SSD), GOOG (NAND/SSD), META (NAND/SSD), MSFT (NAND/SSD) | KIOXIA (NAND) |
| **SNPS** | — | AMD (EDA/IP), ARM (EDA), AVGO (EDA/IP), INTC (EDA/IP), NVDA (EDA/IP), QCOM (EDA/IP), TSM (EDA/IP) | CDNS (EDA) |
| **STX** | — | AMZN (nearline HDD), GOOG (nearline HDD), META (nearline HDD), MSFT (nearline HDD) | WDC (nearline HDD) |
| **TEL** | — | NVDA (connectors) | — |
| **TLN** | — | AMZN (nuclear PPA) | VST (merchant power) |
| **TOKYOELEC** | — | MU (WFE), SAMSUNG (WFE), SKHYNIX (WFE), TSM (WFE) | — |
| **TSLA** | NVDA (GPUs) | — | — |
| **TSM** | ADVANTEST (ATE test), AMAT (WFE), ASML (EUV/DUV litho), BESI (hybrid bonding), CDNS (EDA), DISCO (dicing/grinding), KLAC (process control), LRCX (etch/dep), SNPS (EDA/IP), TOKYOELEC (WFE) | AAPL (foundry), ALAB (foundry), AMD (foundry), AVGO (foundry), CRDO (foundry), MEDIATEK (foundry), MRVL (foundry), NVDA (foundry N3/N2 + CoWoS), QCOM (foundry) | INTC (foundry), SAMSUNG (foundry), SMIC (foundry) |
| **TXN** | — | NVDA (power) | — |
| **VRT** | — | NVDA (power+cooling (800VDC)) | — |
| **VST** | — | AMZN (merchant power) | CEG (merchant power), TLN (merchant power) |
| **WDC** | — | AMZN (nearline HDD), GOOG (nearline HDD), META (nearline HDD), MSFT (nearline HDD) | STX (nearline HDD) |
| **WMB** | — | AMZN (gas midstream) | — |
| **WOLF** | — | NVDA (SiC (800V)) | — |

## How to use

- A **supplier beat/miss** (e.g. an HBM price step at MU/SKHYNIX) reads through to its **customers** (NVDA/AMD/AVGO) — margin/BOM.
- A **customer capex change** (hyperscaler) reads back to its **suppliers** (NVDA → TSM/SKHYNIX/COHR → ASML/AMAT).
