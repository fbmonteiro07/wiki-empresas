"""Regression checks for saved-workbook refresh and recoverable publication."""
import contextlib
import copy
import datetime as dt
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import xml.etree.ElementTree as ET

import build_ai_labs_revenue as b
import refresh_ai_labs_revenue as r


class ModelChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=b.DEFAULT_WB.read_bytes()

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='ai-labs-model-test-')
        self.root=Path(self.temp.name).resolve()
        self.data=self.root/'data';self.data.mkdir()
        for name in ('sources.json','legacy-wfs-2026-06-11.html'):
            shutil.copy2(b.DATA/name,self.data/name)
        self.old_data=patch.object(b,'DATA',self.data);self.old_data.start()
        self.wb=self.root/'AI Model.xlsx';self.wb.write_bytes(self.raw)
        os.utime(self.wb,(1792070132,1792070132))

    def tearDown(self):
        self.old_data.stop()
        assert self.root.parent==Path(tempfile.gettempdir()).resolve()
        self.temp.cleanup()

    def edit_cache(self,cell,value,error=False):
        with zipfile.ZipFile(io.BytesIO(self.raw)) as z:
            rels={x.get('Id'):x.get('Target') for x in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
            sheet=next(x for x in ET.fromstring(z.read('xl/workbook.xml')).find('s:sheets',b.NS) if x.get('name')=='ARR Tracker')
            target=rels[sheet.get(b.REL)];part=target.lstrip('/') if target.startswith('/') else 'xl/'+target
            xml=ET.fromstring(z.read(part));c=next(x for x in xml.findall('.//s:c',b.NS) if x.get('r')==cell)
            v=c.find('s:v',b.NS)
            if value is None:
                c.remove(v)
            else:
                v.text=str(value)
            if error: c.set('t','e')
            with zipfile.ZipFile(self.wb,'w',zipfile.ZIP_DEFLATED) as out:
                for item in z.infolist(): out.writestr(item,ET.tostring(xml) if item.filename==part else z.read(item.filename))
        os.utime(self.wb,(1792070132,1792070132))

    def build(self,asof='2026-10-15'):
        with contextlib.redirect_stdout(io.StringIO()):
            result=b.build(self.wb,asof,b.DEFAULT_TEMPLATE,self.root/'out',persist=False)
        r.validate(result);return result

    def test_all_bases_and_annual_totals(self):
        payload=self.build()
        for basis,total in [('reported',167532.88010503573),('net',158215.05548555258),('gross',169611.8300097019)]:
            self.assertAlmostEqual(payload['combined']['monthly'][basis]['points'][-1]['value'],total)
        self.assertAlmostEqual(next(x['value'] for x in payload['combined']['annual'] if x['period']=='CY26E'),93314.82994687735)

    def test_workbook_change_recomputes_both_affected_totals(self):
        baseline=self.build()
        old=next(s for s in baseline['series'] if s['id']=='openai_net')['points'][-4]['value']
        self.edit_cache('X7',old+100)
        changed=self.build('2026-11-01')
        for basis in ('reported','net'):
            first=next(x for x in baseline['combined']['monthly'][basis]['points'] if x['date']=='2026-09-01')['value']
            second=next(x for x in changed['combined']['monthly'][basis]['points'] if x['date']=='2026-09-01')['value']
            self.assertAlmostEqual(second-first,100)
        self.assertEqual(changed['checked'],'2026-10-15')
        html=(self.root/'out/index.html').read_text(encoding='utf-8')
        self.assertIn('news sources checked 2026-10-15',html)
        self.assertNotEqual(changed['workbook_sha256'],baseline['workbook_sha256'])

    def test_missing_component_is_not_zero(self):
        self.edit_cache('X7',None)
        payload=self.build()
        for basis in ('reported','net'):
            self.assertNotIn('2026-09-01',[p['date'] for p in payload['combined']['monthly'][basis]['points']])
        self.assertIn('2026-09-01',[p['date'] for p in payload['combined']['monthly']['gross']['points']])

    def test_invalid_cache_preserves_previous_files(self):
        self.build(); before=(self.root/'out/index.html').read_bytes()
        self.edit_cache('X7','#REF!',error=True)
        with self.assertRaises(ValueError): self.build()
        self.assertEqual((self.root/'out/index.html').read_bytes(),before)
        self.assertFalse((self.data/'model.json').exists())

    def test_wrong_sum_rejected(self):
        payload=self.build();payload['combined']['monthly']['net']['points'][0]['value']+=10
        with self.assertRaisesRegex(ValueError,'sum failed'): r.validate(payload)


class PublicationChecks(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='ai-labs-publish-test-')
        self.root=Path(self.temp.name).resolve();self.team=self.root/'team';self.origin=self.root/'origin.git'
        self.cmd('git','init','--bare','--initial-branch=main',str(self.origin))
        self.cmd('git','clone',str(self.origin),str(self.team))
        self.cmd('git','config','user.name','AI Labs test',cwd=self.team)
        self.cmd('git','config','user.email','test@example.invalid',cwd=self.team)
        self.cmd('git','config','core.autocrlf','false',cwd=self.team)
        (self.team/'ai-labs').mkdir()
        for name in r.FILES: (self.team/'ai-labs'/name).write_text('prior\n',encoding='utf-8')
        (self.team/'index.html').write_text('hub unchanged\n',encoding='utf-8')
        self.cmd('git','add','.',cwd=self.team);self.cmd('git','commit','-m','initial',cwd=self.team);self.cmd('git','push','origin','main',cwd=self.team)
        self.data=self.root/'data';self.data.mkdir();self.mirror=self.root/'mirror';self.mirror.mkdir();self.candidate=self.data/'candidate';self.candidate.mkdir()
        (self.candidate/'index.html').write_text('<html>new</html>\n\n',encoding='utf-8')
        (self.candidate/'revenue-data.json').write_text('{"new": true}\n',encoding='utf-8')
        self.pending={'fingerprint':'abc123testfingerprint','candidate':str(self.candidate),'artifact_hashes':{n:r.artifact_hash(self.candidate/n) for n in r.FILES}}
        self.state={'pending':self.pending}
        self.patches=[patch.object(r,'DATA',self.data),patch.object(r,'STATE',self.data/'state.json'),patch.object(r,'MIRROR',self.mirror),patch.object(b,'DATA',self.data)]
        for p in self.patches:p.start()

    def tearDown(self):
        for p in reversed(self.patches):p.stop()
        assert self.root.parent==Path(tempfile.gettempdir()).resolve()
        self.temp.cleanup()

    def cmd(self,*args,cwd=None):
        return subprocess.run(args,cwd=cwd,capture_output=True,text=True,check=True).stdout.strip()

    def test_publish_and_repeat_create_one_commit(self):
        first=r.publish(self.team,self.pending,self.state)
        second=r.publish(self.team,self.pending,self.state)
        self.assertEqual(first,second)
        self.assertEqual(self.cmd('git','rev-parse','main',cwd=self.origin),first)
        self.assertEqual((self.team/'index.html').read_text(),'hub unchanged\n')
        self.assertEqual(self.cmd('git','rev-list','--count','HEAD',cwd=self.team),'2')

    def test_unrelated_edits_are_preserved_and_block_publication(self):
        (self.team/'index.html').write_text('user edit\n')
        with self.assertRaisesRegex(RuntimeError,'other changes'):r.publish(self.team,self.pending,self.state)
        self.assertEqual((self.team/'ai-labs/index.html').read_text(),'prior\n')
        self.assertEqual((self.team/'index.html').read_text(),'user edit\n')

    def test_push_failure_resumes_without_duplicate_commit(self):
        original=r.git
        def failed_push(team,*args,**kwargs):
            if args[0]=='push':raise RuntimeError('simulated connection failure')
            return original(team,*args,**kwargs)
        with patch.object(r,'git',side_effect=failed_push):
            with self.assertRaisesRegex(RuntimeError,'connection failure'):r.publish(self.team,self.pending,self.state)
        first=self.cmd('git','rev-parse','HEAD',cwd=self.team)
        second=r.publish(self.team,self.pending,self.state)
        self.assertEqual(first,second)
        self.assertEqual(self.cmd('git','rev-list','--count','HEAD',cwd=self.team),'2')

    def test_no_change_skips_build_and_network(self):
        for name in r.FILES:shutil.copy2(self.team/'ai-labs'/name,self.mirror/name)
        self.state={'completed':{'fingerprint':'same','artifact_hashes':{n:r.artifact_hash(self.mirror/n) for n in r.FILES}}};r.save_state(self.state)
        args=type('Args',(),{'workbook':self.root/'unused.xlsx','team':self.team,'force':False,'check':False,'publish':True,'wait_seconds':0})()
        with patch.object(r,'input_identity',return_value=('same',{'workbook_sha256':'hash'})),patch.object(b,'build') as build,patch.object(r,'git') as git:
            self.assertEqual(r.run(args)['status'],'unchanged');build.assert_not_called();git.assert_not_called()


if __name__=='__main__':unittest.main(verbosity=2)
