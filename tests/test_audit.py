import importlib.util,pathlib,unittest
Q=pathlib.Path(__file__).parents[1]/'tools'/'audit_renderability.py'; s=importlib.util.spec_from_file_location('m',Q);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
GOOD='<html><head><title>T</title><link rel="canonical" href="https://x/"><script type="application/ld+json">{}</script></head><body><main><h1>H</h1><p>'+('word '*120)+'</p></main></body></html>'
class T(unittest.TestCase):
 def test_good_raw_html(self): self.assertEqual(m.inspect_html(GOOD)['errors'],[])
 def test_script_text_not_counted(self): self.assertTrue(m.inspect_html('<html><title>T</title><link rel="canonical" href="x"><main>x</main><script>'+('word '*500)+'</script></html>')['errors'])
 def test_missing_canonical(self): self.assertTrue(any('canonical' in x for x in m.inspect_html('<html><title>T</title><main>'+('w '*120)+'</main></html>')['errors']))
if __name__=='__main__':unittest.main()
