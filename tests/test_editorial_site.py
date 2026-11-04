"""Offline structural checks for the editorial redesign, with no network requests."""
import json
import unittest
from pathlib import Path
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parents[1]
SITE="https://kkfir13.github.io/warren-buffett-brain/"
SLUGS=["sees-candies-1972","geico-1951-to-1996","coca-cola-1988",
       "dexter-and-general-re","goldman-sachs-2008","bnsf-2009",
       "graham-munger-influences","textiles-to-insurance"]

class Parse(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[];self.meta=[];self.ids=[];self.h1=0;self.h2=0
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=="a":self.links.append(d.get("href",""))
        if tag in ("link","meta"):self.meta.append(d)
        if d.get("id"):self.ids.append(d["id"])
        if tag=="h1":self.h1+=1
        if tag=="h2":self.h2+=1

def parse(rel):
    p=Parse()
    p.feed((ROOT/rel).read_text(encoding="utf-8"))
    return p

class EditorialWebsiteTest(unittest.TestCase):
    def test_google_verification_preserved(self):
        html=parse("index.html")
        self.assertTrue(any(m.get("name")=="google-site-verification" and
            m.get("content")=="CBNlfOrfx2IRjtciDrvJpWVZi97fcX7Rd0hj95JxQ_o" for m in html.meta))
    def test_homepage_controls_and_static_links(self):
        html=parse("index.html")
        self.assertEqual(html.h1,1)
        for ident in ("main","search","search-form","cards","query","more","years","sources"):
            self.assertIn(ident,html.ids)
        for slug in SLUGS:
            self.assertIn("./cases/"+slug+"/",html.links)
        self.assertIn("https://github.com/kkfir13/warren-buffett-brain/blob/main/CHATGPT.md",html.links)
        self.assertTrue(any(m.get("rel")=="canonical" and m.get("href")==SITE for m in html.meta))
    def test_case_study_toc_sources_and_canonicals(self):
        for slug in SLUGS:
            with self.subTest(slug=slug):
                html=parse("cases/"+slug+"/index.html")
                self.assertEqual(html.h1,1)
                self.assertIn("article-main",html.ids)
                self.assertGreater(html.h2,1)
                self.assertTrue(any(m.get("rel")=="canonical" and
                    m.get("href")==SITE+"cases/"+slug+"/" for m in html.meta))
                self.assertTrue(any(h.startswith("https://www.berkshirehathaway.com/")
                    or "sec.gov/" in h for h in html.links))
                for href in html.links:
                    if href.startswith("#"):self.assertIn(href[1:],html.ids)
    def test_case_collection(self):
        html=parse("cases/index.html")
        self.assertEqual(html.h1,1)
        for slug in SLUGS:self.assertIn("./"+slug+"/",html.links)
    def test_homepage_css_and_search_script(self):
        css=(ROOT/"styles.css").read_text(encoding="utf-8")
        script=(ROOT/"app.js").read_text(encoding="utf-8")
        self.assertIn("--paper:#f7f6f0",css)
        self.assertIn("Newsreader",css)
        self.assertIn("reading-grid",css)
        self.assertNotIn("radial-gradient",css)
        self.assertIn("data-example",script)
        self.assertIn("./knowledge/atlas.json",script)
    def test_source_count_unchanged(self):
        atlas=json.loads((ROOT/"knowledge/atlas.json").read_text(encoding="utf-8"))
        self.assertEqual(len(atlas["entries"]),55)
        self.assertEqual(len(atlas["sources"]),60)
        self.assertEqual((ROOT/"sitemap.xml").read_text(encoding="utf-8").count("<loc>"),13)

if __name__=="__main__":unittest.main()
