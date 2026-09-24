from pathlib import Path
import importlib.util, os
BASE = Path(__file__).resolve().parent
SKILL = Path('C:/Users/Felipe.monteiro/.codex/plugins/cache/openai-primary-runtime/documents/26.909.12148/skills/documents')
POP = Path('C:/Users/Felipe.monteiro/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin')
os.environ['PATH'] = str(POP) + os.pathsep + os.environ['PATH']
spec = importlib.util.spec_from_file_location('docx_renderer', SKILL/'render_docx.py')
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)
def word_pdf(doc_path,user_profile,convert_tmp_dir,stem,verbose):
    return str(BASE/'word_render.pdf'), 'Native Microsoft Word export; packaged LibreOffice unavailable on Windows.'
renderer.convert_to_pdf = word_pdf
renderer.rasterize(str(BASE.parents[3]/'_deliverables'/'CPU_market_share_2021_2030_2026-09-23.docx'), str(BASE/'render'), 125, False, True)
print('Rendered with packaged render_docx rasterization and native Word PDF conversion.')
