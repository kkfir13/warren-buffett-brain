# Buffett Brain numerical evidence methodology

This is a ValuEdge-designed *educational* six-metric screen, not Warren Buffett's proprietary formula. It does not evaluate moat, character or the user's own investment suitability.

- ROIC (roicPct, percentage points): >=15 supporting; 10–<15 review; <10 challenging.
- Operating margin (operatingMarginPct, percentage points): >=15 supporting; 5–<15 review; <5 challenging. Compare with industry norms.
- FCF yield (fcfYieldPct, percentage points): >0 supporting, <=0 challenging. A positive one-year FCF is not proof of durable free cash flow.
- Revenue three-year CAGR (revenueCagr3yPct, percentage points): >=5 supporting; 0–<5 review; <0 challenging. Growth is not automatically quality.
- Net debt / EBITDA (netDebtToEbitda, multiple): <=1.5 supporting; <=3 review; >3 challenging. Mark unavailable for financial services; inspect debt schedules.
- Price vs model (price, fairValue, quote currency): margin of safety = 100*(fairValue-price)/fairValue; >=20 supporting; 0–<20 review; <0 challenging. Requires valid model and dated price.

Missing metrics always produce "unavailable", never zero. Fundamentals older than 180 days are not assessed. Valuation requires a positive price and positive fair value, hasValidFairValue=true, priceAsOf within 10 days and fairValueAsOf within 45 days. Missing/future dates mean unavailable. The original ValuEdge screener index stores ROIC, margins and FCF yield as percentage points, revenue CAGR as a decimal fraction; the website API multiplies that CAGR by 100.

Economic moats, management integrity, share-class differences, cyclicality and valuation confidence require human diligence and filings. A valuation model is uncertain and a modeled discount is not a trade recommendation. Report price, fundamental and valuation timestamps separately. Do not call cached quotes live.
