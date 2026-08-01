# Case Framing: Hospital Market Expansion & Operational Strategy

## 1. Client (fictional, for portfolio purposes)

**Client:** A healthcare organization considering a new outpatient clinic
somewhere in Florida.

> This is a portfolio project built on public data. No real health system,
> investor, or client is involved. The "client" framing gives the analysis
> a decision-making context, which is standard in consulting-style case
> studies.

## 2. Business Question (simplified)

> "Based on population growth, healthcare need, existing healthcare supply,
> and local economic context, which Florida counties should be prioritized
> for further market research into a new outpatient clinic?"

This is a **market-screening exercise** — a first-pass filter to narrow 67
counties down to a short list worth investigating further, not a complete
site-selection study and not a profitability forecast.

## 3. The Decision This Analysis Supports

1. Screen all 67 Florida counties on a small set of transparent metrics.
2. Identify **three priority counties** worth further investigation.
3. Explain, in plain business terms, why those counties look promising.
4. State clearly what additional data and analysis a real investment
   decision would still require.

## 4. What This Analysis Is NOT

* Not a real estate site-selection study (no parcel-level, traffic, or
  lease data)
* Not a financial pro forma or ROI/NPV model (no reimbursement rates, payer
  mix, staffing costs, or capital costs)
* Not a causal study of what drives healthcare utilization
* Not a substitute for local due diligence, licensure/CON research, or
  competitor-specific intelligence

## 5. Unit of Analysis & Scope

**Florida county** (5-digit FIPS code; Florida state FIPS = 12), covering
all **67 counties**. County level was chosen because the public datasets
used here (Census, CDC PLACES, HRSA, CMS) are reliably available at that
level. This does mask variation within large counties — a real
site-selection process would eventually need to drill into ZIP codes or
drive-time radii within whichever county is chosen.

## 6. Working Hypothesis

> Florida counties with above-average population growth, an above-average
> share of population aged 65+, above-average diabetes prevalence, and
> below-average provider/facility supply per capita are likely to be worth
> prioritizing for further outpatient-market research.

This will be tested against real data, not assumed true. It's entirely
possible the data shows high-growth counties already have adequate supply,
or that low-supply counties also have low income/commercial viability —
both would be legitimate findings.

## 7. Success Criteria (as a portfolio piece)

A hiring manager should be able to see, within a few minutes, that the
candidate can:

* Pull and join real public data via SQL/Python
* Build a small number of clear, business-relevant KPIs
* Build a transparent, easy-to-explain scoring model (not a black box)
* Show a basic sensitivity check rather than presenting one ranking as fact
* Communicate findings to a non-technical, executive audience
* Be upfront about what the data can and can't support
