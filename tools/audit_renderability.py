#!/usr/bin/env python3
import argparse,re,urllib.request
from html.parser import HTMLParser
class H(HTMLParser):
 def __init__(self): super().__init__(); self.skip=0; self.text=[]; self.title=[]; self.in_title=False; self.canon=[]; self.hreflang=[]; self.jsonld=0; self.landmarks=set()
 def handle_starttag(self,t,a):
  t=t.lower(); d=dict(a)
  if t in ('script','style','noscript','template'):
   if t=='script' and (d.get('type') or '').lower()=='application/ld+json': self.jsonld+=1
   self.skip+=1
  if t=='title': self.in_title=True
  if t in ('main','article','h1'): self.landmarks.add(t)
  if t=='link' and (d.get('rel') or '').lower()=='canonical' and d.get('href'): self.canon.append(d['href'])
  if t=='link' and (d.get('rel') or '').lower()=='alternate' and d.get('hreflang') and d.get('href'): self.hreflang.append((d['hreflang'],d['href']))
 def handle_endtag(self,t):
  t=t.lower()
  if t in ('script','style','noscript','template') and self.skip:self.skip-=1
  if t=='title': self.in_title=False
 def handle_data(self,d):
  if not self.skip and d.strip():
   self.text.append(d.strip())
   if self.in_title:self.title.append(d.strip())
def inspect_html(body,min_words=100):
 p=H(); p.feed(body); visible=' '.join(p.text); words=re.findall(r"\b[\w’'-]+\b",visible,flags=re.UNICODE); e=[]
 if len(words)<min_words:e.append(f'raw visible words below threshold: {len(words)} < {min_words}')
 if not p.title:e.append('missing raw HTML title')
 if len(p.canon)!=1:e.append(f'expected one raw canonical, got {len(p.canon)}')
 if 'main' not in p.landmarks and 'article' not in p.landmarks:e.append('missing raw main/article landmark')
 return {'words':len(words),'title':' '.join(p.title),'canonical':p.canon,'hreflang':len(p.hreflang),'jsonld':p.jsonld,'landmarks':sorted(p.landmarks),'errors':e}
def fetch(url,timeout=15):
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 RenderabilityAudit/1.0'}); r=urllib.request.urlopen(req,timeout=timeout); return r.geturl(),r.status,r.headers.get_content_type(),r.read().decode('utf-8','replace')
def main():
 a=argparse.ArgumentParser(); a.add_argument('url'); a.add_argument('--min-words',type=int,default=100); n=a.parse_args(); final,status,ctype,body=fetch(n.url); x=inspect_html(body,n.min_words)
 print(f'url={n.url} final={final} status={status} content_type={ctype} raw_words={x["words"]} canonical={len(x["canonical"])} hreflang={x["hreflang"]} jsonld={x["jsonld"]} landmarks={",".join(x["landmarks"])} errors={len(x["errors"])}')
 for e in x['errors']:print('ERROR',e)
 return 1 if x['errors'] or status!=200 or ctype!='text/html' else 0
if __name__=='__main__':raise SystemExit(main())
