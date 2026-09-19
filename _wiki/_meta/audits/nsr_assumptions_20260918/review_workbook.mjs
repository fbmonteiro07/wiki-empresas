import fs from 'node:fs/promises';
import path from 'node:path';
import { FileBlob, SpreadsheetFile } from '@oai/artifact-tool';
const root = 'E:/Wiki Felipe empresas';
const audit = path.join(root, '_wiki/_meta/audits/nsr_assumptions_20260918');
const original = path.join(root, '_wiki/models/NSR_AI_Capex_4tn_2030_vs_Capstone_2026-09-18.xlsx');
const outputDir = path.join(root, 'outputs/01a0b62e-bd83-7e72-8352-284471642a9b');
const mode = process.argv[2] || 'inspect';
const wb = await SpreadsheetFile.importXlsx(await FileBlob.load(original));
if (mode === 'inspect') {
 console.log((await wb.inspect({kind:'sheet',include:'id,name',maxChars:2500})).ndjson);
 console.log((await wb.inspect({kind:'computedStyle',sheetId:'Comparison',range:'I44:I50',maxChars:2000})).ndjson);
 for (const [sheetName,range,file] of [['Comparison','A44:I50','before_cpu.png'],['Summary','A10:I19','before_summary.png']]) {
  const preview = await wb.render({sheetName,range,scale:1,format:'png'});
  await fs.writeFile(path.join(audit,file),new Uint8Array(await preview.arrayBuffer()));
 }
 console.log('Baseline previews saved.');
} else {
 const edits = JSON.parse((await fs.readFile(path.join(audit,'review_edits.json'),'utf8')).replace(/^\uFEFF/,''));
 wb.comments.setSelf({displayName:'Felipe Monteiro'});
 for (const edit of edits.cells) {
  const sh = wb.worksheets.getItem(edit.sheet);
  sh.getRange(edit.cell).values = [[edit.text]];
  if (edit.rowHeight) sh.getRange(edit.cell).format.rowHeight = edit.rowHeight;
 }
 for (const note of edits.comments) wb.comments.addThread({cell:wb.worksheets.getItem(note.sheet).getRange(note.cell)},note.text);
 wb.recalculate();
 console.log((await wb.inspect({kind:'table',range:'Comparison!F48:I50',include:'values,formulas',tableMaxRows:3,tableMaxCols:4,maxChars:2500})).ndjson);
 console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:25},summary:'Final error scan',maxChars:2000})).ndjson);
 await fs.mkdir(outputDir,{recursive:true});
 const out = path.join(outputDir,path.basename(original));
 await (await SpreadsheetFile.exportXlsx(wb)).save(out);
 for (const [sheetName,range,file] of [['Comparison','A44:I50','after_cpu.png'],['Summary','A10:I19','after_summary.png'],['Comparison','A119:I129','after_cash.png']]) {
  const preview = await wb.render({sheetName,range,scale:1,format:'png'});
  await fs.writeFile(path.join(audit,file),new Uint8Array(await preview.arrayBuffer()));
 }
 console.log(JSON.stringify({out,comments:edits.comments.length,textEdits:edits.cells.length}));
}
