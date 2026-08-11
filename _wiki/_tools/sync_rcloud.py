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
  • rótulo de fonte reescrito como "Capstone · réplica ... · snapshot <data>", seja qual for
    o que a origem tenha no <span class="src"> — a casa é Capstone, e o rótulo da origem já
    veio errado uma vez (nome de outra casa, herdado do template);
  • link "← Dashboard Principal" (href="index.html") re-rotulado: neste diretório o
    index.html é o hub de dashboards da wiki, não o hub da Fernanda;
  • links "../" (quebrados no destino) removidos — defensivo, hoje não há nenhum;
  • comentário de procedência injetado no topo.

Uso:  py "E:\Wiki Felipe empresas\_wiki\_tools\sync_rcloud.py"                 # só a réplica da wiki
      py "E:\Wiki Felipe empresas\_wiki\_tools\sync_rcloud.py" --publish-team  # + Capstone-Wiki (Pages)
Só stdlib.

--src PATH publica de OUTRO arquivo em vez do rcloud.html da Fernanda. Serve pra quando os
workbooks dela (AI Model.xlsx / TAM_Cloud.xlsb) já estão mais novos que o rcloud.html — aí a
gente reroda o atualizar_rcloud.py dela contra os workbooks e publica o resultado sem ter que
esperar/mexer no arquivo dela. Nesse caso passe também --origin "texto" descrevendo a
procedência real, senão o rótulo apontaria pra um caminho temporário e mentiria sobre a fonte.

--publish-team espelha em Capstone-Wiki/rcloud/index.html e JÁ DÁ commit+push no main.
O push não é opcional por segurança: a rotina das 09:45 roda `git reset --hard origin/main`
naquele clone, então arquivo não-commitado ali é destruído no dia seguinte. Mesmo padrão do
publish_team() do refresh_memoria.py.
"""

import os
import re
import shutil
import subprocess
import sys
from datetime import date

sys.stdout.reconfigure(encoding="utf-8")

SRC = r"P:\Fernanda Neves\MarketData_PYTHON_CODES\Dashboards\Oficiais\rcloud.html"
OUT = r"E:\Wiki Felipe empresas\_wiki\_dashboards\rcloud.html"
TEAM = r"P:\Felipe Monteiro\US Equities\Capstone-Wiki"      # clone vivo do Pages do time
TEAM_REL = "rcloud/index.html"

NAV_OLD = '<a href="index.html">← Dashboard Principal</a>'
NAV_NEW = '<a href="index.html">← Wiki dashboards</a>'
# no Capstone-Wiki o dashboard vira rcloud/index.html, então "index.html" apontaria pra ele
# mesmo — o link do hub tem que virar "../" (idem refresh_memoria.py)
NAV_TEAM = '<a href="../">← Capstone Wiki</a>'


def _argval(flag):
    """Valor de '--flag valor' em sys.argv, ou None."""
    if flag in sys.argv:
        i = sys.argv.index(flag)
        if i + 1 < len(sys.argv):
            return sys.argv[i + 1]
        sys.exit(f"[ERRO] {flag} exige um valor.")
    return None


def main():
    src = _argval("--src") or SRC
    origin = _argval("--origin")
    if not os.path.exists(src):
        sys.exit(f"[ERRO] origem não encontrada (P: montado?): {src}")
    if src != SRC and not origin:
        sys.exit("[ERRO] --src sem --origin: o rótulo de fonte ficaria apontando pro caminho\n"
                 "       temporário. Passe --origin \"descrição da procedência real\".")

    snapshot = date.fromtimestamp(os.path.getmtime(src)).isoformat()
    with open(src, "r", encoding="utf-8-sig") as f:      # utf-8-sig tira o BOM
        h = f.read()

    # ── guarda: a réplica precisa continuar auto-suficiente ───────────────────
    ext = re.findall(r'(?:src|href)="(?:https?:)?//[^"]*"', h)
    if ext:
        sys.exit("[ERRO] origem passou a depender de recurso externo — inline antes de publicar:\n  "
                 + "\n  ".join(sorted(set(ext))[:10]))

    # ── rótulo de fonte ──────────────────────────────────────────────────────
    # Reescreve o <span class="src"> qualquer que seja o conteúdo (não casa string literal:
    # a origem muda o rótulo de vez em quando e já trouxe nome de casa errado).
    label = (f"Capstone · réplica do rcloud.html (Fernanda Neves) · snapshot {snapshot} · uso interno"
             if origin is None else
             f"Capstone · réplica do rcloud.html (Fernanda Neves) · {origin} · uso interno")
    src_old = re.search(r'<span class="src">([^<]*)</span>', h)
    h, n = re.subn(r'(<span class="src">)[^<]*(</span>)', rf"\g<1>{label}\g<2>", h, count=1)
    if n == 0:
        print('  [AVISO] <span class="src"> não encontrado — réplica sai sem rótulo de snapshot.')
    else:
        print(f'  rótulo de fonte: "{src_old.group(1)}"\n               -> "{label}"')

    # ── navegação ────────────────────────────────────────────────────────────
    if NAV_OLD in h:
        h = h.replace(NAV_OLD, NAV_NEW)
    else:
        print("  [AVISO] link '← Dashboard Principal' não encontrado — confira o nav.")
    h = re.sub(r'[ \t]*<a href="\.\./[^"]*"[^>]*>[\s\S]*?</a>\n?', "", h)   # links '../' quebram aqui

    # ── procedência ──────────────────────────────────────────────────────────
    stamp = (f"<!-- RÉPLICA gerada por _wiki/_tools/sync_rcloud.py em {date.today().isoformat()}.\n"
             f"     Origem: {src}\n"
             + (f"     Procedência: {origin}\n" if origin else "")
             + f"     Snapshot dos dados: {snapshot} (mtime da origem).\n"
             f"     Não editar aqui — edite na origem e rode o sync de novo.\n"
             f"     Os dados vêm do atualizar_rcloud.py da Fernanda (AI Model.xlsx +\n"
             f"     TAM_Cloud.xlsb sheet 'Mercado'); esse pipeline não está portado pra wiki,\n"
             f"     então a réplica não se auto-atualiza. -->")
    h = h.replace("<!DOCTYPE html>", "<!DOCTYPE html>\n" + stamp, 1)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        f.write(h)
    print(f"rcloud.html escrito ({len(h):,} chars) · snapshot {snapshot}\n  -> {OUT}")

    if "--publish-team" in sys.argv:
        publish_team(h)


def _run(args, cwd=None):
    return subprocess.run(args, cwd=cwd).returncode


def publish_team(h):
    """Espelha em Capstone-Wiki/rcloud/index.html e commita+pusha main se mudou."""
    if not os.path.isdir(os.path.join(TEAM, ".git")):
        print(f"  [AVISO] clone do Capstone-Wiki não encontrado em {TEAM} — team copy pulada.")
        return
    if NAV_NEW in h:
        h = h.replace(NAV_NEW, NAV_TEAM)
    else:
        print("  [AVISO] link do hub não encontrado — team copy pode ter link quebrado.")

    dest = os.path.join(TEAM, *TEAM_REL.split("/"))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8", newline="") as f:
        f.write(h)

    _run(["git", "add", TEAM_REL], cwd=TEAM)
    if subprocess.run(["git", "diff", "--cached", "--quiet", "--", TEAM_REL], cwd=TEAM).returncode == 0:
        print("  team copy sem mudança — nada a commitar.")
        return
    msg = ("rcloud: Revenue das Clouds (réplica do dashboard da Fernanda)\n\n"
           "Decomposição da receita das clouds — resultado, RPO (split OpenAI/Anthropic),\n"
           "projeções Capstone vs consenso vs bogey, exposição aos labs, EBIT e capex/FCF.\n"
           "Snapshot dos dados da origem; publicado por _wiki/_tools/sync_rcloud.py.\n\n"
           "Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>")
    if _run(["git", "commit", "-m", msg], cwd=TEAM) == 0:
        _run(["git", "push", "origin", "main"], cwd=TEAM)
        print("  team copy publicada -> https://fbmonteiro07.github.io/Capstone-Wiki/rcloud/")


if __name__ == "__main__":
    main()
