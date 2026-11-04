import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from search_knowledge import search
from validate_knowledge import check

with (ROOT/"knowledge"/"atlas.json").open(encoding="utf-8") as f:
    atlas=json.load(f)

class AtlasTests(unittest.TestCase):
    def test_schema_and_source_rights(self):
        self.assertEqual(check(atlas),[])
    def test_sees_primary_deal(self):
        records=search(atlas,"See's Candies",kind="decision",limit=3)
        self.assertTrue(any(e["id"]=="sees-1972" for e in records))
        self.assertTrue(all(e["sources"] for e in records))
    def test_goldman_transaction(self):
        records=search(atlas,"Goldman Sachs preferred warrants 2008",kind="decision")
        self.assertEqual(records[0]["id"],"goldman-sachs-2008")
        self.assertTrue(any("sec.gov" in x["url"] for x in records[0]["sources"]))
    def test_mistakes_include_dexter(self):
        records=search(atlas,"Dexter Shoe",kind="mistake")
        self.assertEqual(records[0]["id"],"dexter-shoe-1993")
    def test_graham_not_attributed_to_buffett(self):
        records=search(atlas,"Intelligent Investor Benjamin Graham",kind="book")
        self.assertEqual(records[0]["id"],"book-intelligent-investor")
        self.assertIn("Benjamin Graham",records[0]["summary"])
        self.assertIn("Not written by Buffett",records[0]["limitations"])
    def test_four_short_attributed_buffett_quotes(self):
        quotes=[e for e in atlas["entries"] if e["kind"]=="statement"]
        self.assertEqual(len(quotes),4)
        self.assertTrue(all(e["speaker"]=="Warren E. Buffett" for e in quotes))
        self.assertTrue(all(len(e["verbatimExcerpt"].split())<=25 for e in quotes))
    def test_no_synthetic_sources(self):
        self.assertEqual(search(atlas,"zzzzznonexistentuniquequery"),[])
    def test_archive_index(self):
        refs={r["id"] for r in atlas["sources"]}
        self.assertIn("letter-1977",refs)
        self.assertIn("letter-2024",refs)
        self.assertIn("cnbc-meetings",refs)

if __name__=="__main__":unittest.main()
