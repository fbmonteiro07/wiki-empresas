r"""
sync_rcloud.py
--------------
Publica a réplica do dashboard "Revenue Clouds — Decomposição" (rcloud.html) da Fernanda
em _wiki/_dashboards, do mesmo jeito que build_ai_dashboards.py faz com economics_1gw.html
e como_flui_capacidade.html — mas SEM repatchar dados.

Diferença de fundo vs build_ai_dashboards.py: aquele reconstrói as consts a partir do
"AI Model (comentado)" do Felipe (openpyxl). O rcloud.html tem os dados reescritos pelo
atualizar_rcloud.py da Fernanda a partir do TAM_Cloud.xlsb (sheet 'Mercado') — pipeline que
NÃO está portado pra cá. Então esta réplica é um SNAPSHOT: os números são os que a Fernanda
tinha publicado na data de modificação do arquivo de origem (vai no rótulo de fonte).
Rodar de novo re-sincroniza do original.

O arquivo é auto-suficiente (Chart.js inline, zero recurso externo) — o script confere isso
e aborta se a Fernanda introduzir um CDN, senão a página quebraria atrás do proxy TLS.

Adaptações aplicadas (as mesmas de clean_links() no build_ai_dashboards.py, + as daqui):
  • BOM removido (as réplicas já existentes não têm BOM);
  • rótulo de fonte "AI Model 25-06.xlsx · Tork Capital · uso interno" -> rótulo de réplica
    com a data do snapshot. "Tork Capital" é rótulo legado do template da origem;
  • link "← Dashboard Principal" (href="index.html") re-rotulado: neste diretório o
    index.html é o hub de dashboards da wiki, não o hub da Fernanda;
  • links "../" (quebrados no destino) removidos — defensivo, hoje não há nenhum;
  • comentário de procedência injetado no topo.

Uso:  py "E:\Wiki Felipe empresas\_wiki\_tools\sync_rcloud.py"
Só stdlib.
"""

import os
import re
import sys
from datetime import date

sys.stdout.reconfigure(encoding="utf-8")

SRC = r"P:\Fernanda Neves\MarketData_PYTHON_CODES\Dashboards\Oficiais\rcloud.html"
OUT = r"E:\Wiki Felipe empresas\_wiki\_dashboards\rcloud.html"

SRC_LABEL_OLD = "AI Model 25-06.xlsx · Tork Capital · uso interno"
NAV_OLD = '<a href="index.html">← Dashboard Principal</a>'
NAV_NEW = '<a href="index.html">← Wiki dashboards</a>'


def main():
    if not os.path.exists(SRC):
        sys.exit(f"[ERRO] origem não encontrada (P: montado?): {SRC}")

    snapshot = date.fromtimestamp(os.path.getmtime(SRC)).isoformat()
    with open(SRC, "r", encoding="utf-8-sig") as f:      # utf-8-sig tira o BOM
        h = f.read()

    # ── guarda: a réplica precisa continuar auto-suficiente ───────────────────
    ext = re.findall(r'(?:src|href)="(?:https?:)?//[^"]*"', h)
    if ext:
        sys.exit("[ERRO] origem passou a depender de recurso externo — inline antes de publicar:\n  "
                 + "\n  ".join(sorted(set(ext))[:10]))

    # ── rótulo de fonte ──────────────────────────────────────────────────────
    label = f"réplica · rcloud.html (Fernanda Neves) · snapshot {snapshot} · uso interno"
    if SRC_LABEL_OLD in h:
        h = h.replace(SRC_LABEL_OLD, label)
    else:
        # rótulo mudou na origem: substitui o conteúdo do <span class="src"> seja ele qual for
        h, n = re.subn(r'(<span class="src">)[^<]*(</span>)', rf"\g<1>{label}\g<2>", h, count=1)
        if n == 0:
            print('  [AVISO] <span class="src"> não encontrado — réplica sai sem rótulo de snapshot.')
        else:
            print(f'  [AVISO] rótulo de fonte da origem mudou (não era "{SRC_LABEL_OLD}") — reescrito.')

    # ── navegação ────────────────────────────────────────────────────────────
    if NAV_OLD in h:
        h = h.replace(NAV_OLD, NAV_NEW)
    else:
        print("  [AVISO] link '← Dashboard Principal' não encontrado — confira o nav.")
    h = re.sub(r'[ \t]*<a href="\.\./[^"]*"[^>]*>[\s\S]*?</a>\n?', "", h)   # links '../' quebram aqui

    # ── procedência ──────────────────────────────────────────────────────────
    stamp = (f"<!-- RÉPLICA gerada por _wiki/_tools/sync_rcloud.py em {date.today().isoformat()}.\n"
             f"     Origem: {SRC}\n"
             f"     Snapshot dos dados: {snapshot} (mtime do original).\n"
             f"     Não editar aqui — edite na origem e rode o sync de novo.\n"
             f"     Os dados vêm do atualizar_rcloud.py da Fernanda (TAM_Cloud.xlsb, sheet 'Mercado');\n"
             f"     esse pipeline não está portado pra wiki, então a réplica não se auto-atualiza. -->")
    h = h.replace("<!DOCTYPE html>", "<!DOCTYPE html>\n" + stamp, 1)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        f.write(h)
    print(f"rcloud.html escrito ({len(h):,} chars) · snapshot {snapshot}\n  -> {OUT}")


if __name__ == "__main__":
    main()
