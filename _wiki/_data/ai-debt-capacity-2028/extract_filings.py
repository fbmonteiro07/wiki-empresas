from html.parser import HTMLParser
from pathlib import Path
import re, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent / "sources"
OUT.mkdir(exist_ok=True)
class Extract(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]; self.skip=0
    def handle_starttag(self,tag,attrs):
        if tag in ("script","style","ix:header"): self.skip+=1
        if not self.skip and tag in ("p","tr","h1","h2","h3","h4"): self.parts.append("\n")
    def handle_endtag(self,tag):
        if tag in ("script","style","ix:header") and self.skip: self.skip-=1
        if not self.skip:
            if tag in ("p","tr","h1","h2","h3","h4"): self.parts.append("\n")
            elif tag in ("td","th"): self.parts.append(" | ")
    def handle_data(self,data):
        if not self.skip: self.parts.append(data)
for ticker in ["MSFT","AMZN","GOOG","META","ORCL","CRWV","NBIS","SPCX","NSCALE"]:
    directory=ROOT/ticker
    for p in directory.glob("*.html"):
        if not any(x in p.name for x in ("10-K_2026","10-Q_2026","20-F_2026","S-1","6-K_2026","ex991")): continue
        parser=Extract(); parser.feed(p.read_text(encoding="utf-8",errors="replace"))
        lines=[re.sub(r"\s+"," ",line).strip(" |") for line in "".join(parser.parts).splitlines()]
        target=OUT/(p.stem+".txt")
        target.write_text("\n".join(line for line in lines if line),encoding="utf-8")
        print(p.relative_to(ROOT),"->",len(lines),"lines")
