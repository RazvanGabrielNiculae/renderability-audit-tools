import json,subprocess,sys,tempfile,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1];T=R/'tools/audit_extractability.py'
class Extractability(unittest.TestCase):
 def test_example(self):
  r=subprocess.run([sys.executable,str(T),str(R/'examples-answer.html')],capture_output=True,text=True);self.assertEqual(r.returncode,0);self.assertTrue(json.loads(r.stdout)['has_h1'])
 def test_script_noise_excluded(self):
  f=tempfile.NamedTemporaryFile('w',suffix='.html',delete=False);f.write('<script>'+('noise '*100)+'</script><h1>Real</h1>answer');f.close()
  r=subprocess.run([sys.executable,str(T),f.name],capture_output=True,text=True);self.assertLess(json.loads(r.stdout)['word_count'],10)
if __name__=='__main__':unittest.main()
