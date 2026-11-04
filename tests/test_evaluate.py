import unittest, sys
from pathlib import Path
from datetime import datetime, timezone
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from evaluate import screen
NOW=datetime(2026,11,4,tzinfo=timezone.utc)
def row():
    return {"symbol":"DEMO","sector":"Technology","price":100,"fairValue":150,"hasValidFairValue":True,
        "priceAsOf":"2026-11-03T00:00:00Z","fairValueAsOf":"2026-11-03T00:00:00Z",
        "fundamentalsAsOf":"2026-10-30T00:00:00Z",
        "metrics":{"roicPct":20,"operatingMarginPct":25,"fcfYieldPct":3,"revenueCagr3yPct":6,"netDebtToEbitda":1}}
class ResearchTests(unittest.TestCase):
    def test_six_signals(self):
        result=screen(row(),NOW)
        self.assertEqual(len(result["signals"]),6)
        self.assertTrue(all(s["state"]=="supporting" for s in result["signals"]))
        self.assertFalse(result["investment_advice"])
    def test_missing_not_zero(self):
        d=row();d["metrics"]["roicPct"]=None
        self.assertEqual(screen(d,NOW)["signals"][0]["state"],"unavailable")
    def test_invalid_fair_value(self):
        d=row();d["hasValidFairValue"]=False
        self.assertEqual(screen(d,NOW)["signals"][-1]["state"],"unavailable")
    def test_price_stale(self):
        d=row();d["priceAsOf"]="2026-01-01"
        self.assertEqual(screen(d,NOW)["signals"][-1]["state"],"unavailable")
    def test_financial_leverage(self):
        d=row();d["sector"]="Financial Services"
        self.assertEqual(screen(d,NOW)["signals"][4]["state"],"unavailable")
if __name__=="__main__":unittest.main()
