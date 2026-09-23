import argparse,json
from pathlib import Path
from html.parser import HTMLParser
class P(HTMLParser):
 def __init__(self): super().__init__(); self.tags=[]; self.text=[]; self.skip=0
 def handle_starttag(self,t,a):
  self.tags.append(t)
  if t in {'script','style','noscript','template'}: self.skip+=1
 def handle_endtag(self,t):
  if t in {'script','style','noscript','template'} and self.skip: self.skip-=1
 def handle_data(self,d):
  if not self.skip and d.strip(): self.text.append(d.strip())
def audit(path):
 p=P();p.feed(Path(path).read_text(encoding='utf-8')); text=' '.join(p.text); first=' '.join(text.split()[:80])
 return {"word_count":len(text.split()),"has_h1":"h1" in p.tags,"has_table":"table" in p.tags,"list_count":p.tags.count('ul')+p.tags.count('ol'),"question_marks":text.count('?'),"first_80_words":first}
def main():
 q=argparse.ArgumentParser();q.add_argument('html');a=q.parse_args();print(json.dumps(audit(a.html),indent=2,ensure_ascii=False))
if __name__=='__main__':main()
