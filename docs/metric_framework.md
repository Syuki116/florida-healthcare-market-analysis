# Metric Framework

**Revision note:** This project went through two rounds of increasing
methodological complexity (Phase 1.1 fixed double-counting across
components; a Phase 1.2 draft started adding dependency mapping,
correlation governance, and leave-one-out testing). That level of rigor is
appropriate for a research paper, not for an entry-level analyst portfolio
project — so the framework was simplified back down. The Phase 1.1
double-counting fixes are kept (they were genuinely necessary and easy to
explain in an interview). The Phase 1.2 governance apparatus was archived,
not implemented — see `docs/archive/scoring_governance_ARCHIVED.md`.

This is now a **simple, transparent screening model**: a small number of
interpretable metrics, converted to percentile scores, combined with
analyst-assigned weights. It is explicitly a first-pass **market screening
tool**, not a validated predictive model.

---

## 1. The Seven Core Metrics

| # | Metric | What it captures | Direction | Likely Source |
|---|---|---|---|---|
| 1 | Total population | Market size (context, not scored directly — see below) | n/a | Census Population Estimates Program (PEP) |
| 2 | Population growth rate | Whether the market is getting bigger | Higher = more opportunity | Census PEP |
| 3 | % population age 65+ | Demand for outpatient/chronic care | Higher = more opportunity | ACS 5-Year (Table S0101) |
| 4 | Diabetes prevalence (%) | Chronic disease burden | Higher = more opportunity | CDC PLACES (exact field name confirmed in Phase 2) |
| 5 | Primary-care providers per 10,000 residents | Existing PCP supply | **Lower = more opportunity** (reversed) | HRSA Area Health Resource File (AHRF), or similar county-level provider source |
| 6 | Relevant healthcare facilities per 10,000 residents | Existing facility supply | **Lower = more opportunity** (reversed) | CMS Hospital General Information / Provider of Services, or comparable source |
| 7 | Median household income | Local economic / commercial context | Higher = more opportunity (context indicator, see limitations) | ACS 5-Year (Table S1901) |

This list is intentionally short. Every metric on it is easy to explain in
one sentence in an interview, which matters more for this project than
covering every dimension of a real due-diligence study.

**Total population is not scored directly.** It's used as:
* A descriptive KPI shown throughout the dashboard and county profiles
* An optional minimum-eligibility screen (so a county of a few thousand
  people doesn't rank #1 purely on a high prevalence rate) — the actual
  threshold will be chosen after looking at the real population
  distribution in Phase 2/3, not decided in advance
* Context for interpreting the other six metrics (e.g., a facility
  shortage matters more in a large county than a tiny one)

---

## 2. Provisional Scoring Model

Every scored metric (2–7) is converted to a **0–100 percentile score**
across Florida's 67 counties (`percentile_rank × 100`). Percentile rank was
chosen over min-max normalization because it's simple to explain ("this
county is in the 80th percentile for diabetes prevalence") and isn't
distorted by one or two extreme counties the way min-max can be.

For the two supply metrics (PCP per 10,000 and facilities per 10,000), the
percentile is **reversed** (`100 − percentile`) so that low existing supply
produces a high opportunity score.

```
Overall Opportunity Score =
    0.20 × Population Growth Score
  + 0.15 × Age 65+ Score
  + 0.15 × Diabetes Prevalence Score
  + 0.20 × PCP Shortage Score        (reversed supply)
  + 0.15 × Facility Shortage Score   (reversed supply)
  + 0.15 × Median Household Income Score
```

**These weights are analyst-selected assumptions for an initial screening
model — not empirically validated or objectively "correct."** They reflect
a simple judgment call: provider shortage and growth matter most, followed
by disease burden, facility shortage, and income. Reasonable people could
weight this differently, which is exactly why a sensitivity check (Section
3) is included.

Missing data handling: if a county is missing a value for one of the six
scored metrics, that metric is excluded from that county's score and the
remaining weights are re-normalized to sum to 100% for that county, with
the exclusion flagged in the output (not silently treated as zero).

---

## 3. Sensitivity Check (3 Scenarios)

To show that the ranking depends on the weights chosen — not to prove one
weighting is "right" — the dashboard lets the user switch between three
scenarios:

| Scenario | Growth | Age 65+ | Diabetes | PCP Shortage | Facility Shortage | Income |
|---|---|---|---|---|---|---|
| **Balanced** (default) | 20% | 15% | 15% | 20% | 15% | 15% |
| **Healthcare Need Focus** | 10% | 20% | 25% | 25% | 15% | 5% |
| **Growth Focus** | 35% | 15% | 10% | 15% | 10% | 15% |

For each scenario, the Top 10 ranking is recomputed. Counties that stay in
the Top 10 across all three scenarios are the more defensible
recommendations; counties that only appear under one scenario are flagged
as weight-sensitive rather than presented as equally strong.

---

## 4. Eligibility Screen (Simple Version)

Before ranking, counties below a minimum population threshold are excluded
from the "recommended" list (though still shown in the full data table).
The exact threshold is chosen in Phase 2/3 after looking at Florida's real
county population distribution — the intent is just to stop a very small
county from topping the ranking purely because a single prevalence value
is high, not to build an elaborate screening framework.

---

## 5. Service-Line Note (Kept Simple)

The original scope considered a full specialty-by-specialty service-line
model (cardiology, endocrinology, OB/GYN provider counts, etc.). That level
of detail isn't necessary for a screening-level project and depends on
provider data that may not be reliably available at that granularity. If
time allows after the core dashboard is done, a simple, clearly-labeled
"illustrative service mix" note may be added (e.g., "high diabetes
prevalence + relatively low PCP supply suggests primary care and diabetes
management as an initial service focus") — but this is a stretch goal, not
a core deliverable, and will be labeled as a directional observation, not a
validated recommendation.

---

## 6. Limitations

* This is a **market-screening exercise**, not a complete site-selection
  study and not a profitability forecast.
* County-level analysis masks variation within large counties (a county can
  have both underserved rural areas and saturated urban centers).
* Provider/facility counts measure *supply*, not actual wait times,
  capacity, or willingness to accept new patients.
* Median household income is a **commercial/economic context indicator**,
  not a direct measure of unmet healthcare need — a high-income county
  isn't necessarily "worse" for need, it's a different kind of opportunity
  (more likely to be commercially viable, less likely to be a safety-net
  gap).
* Diabetes prevalence is one chronic-disease indicator, used as a simple,
  reliably-available proxy for overall chronic disease burden — not a
  complete clinical needs assessment.
* The score does **not** include real estate/rent, labor costs, payer mix,
  reimbursement rates, patient travel patterns, actual clinic capacity,
  health-system strategy, or projected revenue/profitability. These would
  all be required before a real investment decision.
* Weights are analyst judgment calls, disclosed as such, and stress-tested
  with the 3-scenario sensitivity check — not claimed to be objectively
  optimal.
