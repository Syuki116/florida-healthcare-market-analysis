# Data Acquisition Plan

**Simplified scope:** four primary data sources, matched to the seven core
metrics in `docs/metric_framework.md`. Earlier drafts of this plan broke
facility and provider data into many sub-categories (ASCs, RHCs, FQHCs,
specialty-level provider taxonomies); that detail was archived along with
the rest of the over-engineered scoring framework — see
`docs/archive/scoring_governance_ARCHIVED.md`. Nothing below has been
downloaded yet; Phase 2 will verify each source against the live page and
update this document with what was actually found.

Status legend:
- 🔧 API/programmatic access likely possible (to be tested in Phase 2)
- 📥 Manual download likely required
- 🔍 Needs investigation in Phase 2 to confirm best source/table

## 1. U.S. Census Bureau / ACS — population, growth, age, income

| Metric | Source | Access | Notes |
|---|---|---|---|
| Total population | Census Population Estimates Program (PEP) | 🔧 Census API | Free API, key recommended: https://api.census.gov/data/key_signup.html |
| Population growth rate | Census PEP (multi-year) | 🔧 Census API | Vintage/years confirmed in Phase 2 |
| % population age 65+ | ACS 5-Year, Table S0101 | 🔧 Census API | 5-year chosen so all 67 counties are covered (1-year estimates exclude small counties) |
| Median household income | ACS 5-Year, Table S1901 | 🔧 Census API | |
| Manual fallback | data.census.gov | 📥 | Search "ACS 5-year subject tables county Florida" or "Census PEP county Florida" if API access is blocked |

## 2. CDC PLACES — diabetes prevalence

| Metric | Source | Access | Notes |
|---|---|---|---|
| Diabetes prevalence, county level | CDC PLACES | 🔧 Socrata API, or 📥 bulk CSV | https://www.cdc.gov/places — exact measure field name confirmed against the live release in Phase 2, not assumed in advance |

## 3. Primary-care provider counts

| Metric | Source | Access | Notes |
|---|---|---|---|
| PCPs per 10,000 residents, county level | HRSA Area Health Resource File (AHRF) | 📥 (full national file, filter to Florida) | Search "HRSA Area Health Resource File county download". If AHRF's primary-care breakdown isn't usable, CMS NPPES (taxonomy-filtered) is the fallback, flagged as a heavier lift |

## 4. Relevant healthcare facility counts

| Metric | Source | Access | Notes |
|---|---|---|---|
| Facilities per 10,000 residents, county level | CMS Hospital General Information / Provider of Services (POS) file | 📥 likely, 🔧 possibly via data.cms.gov | Search "CMS Hospital General Information dataset" or "CMS Provider of Services file download". Scope (hospitals only vs. hospitals + other outpatient facility types) confirmed once the actual file is reviewed in Phase 2, and documented in `data/data_dictionary.md` |

## 5. FIPS Code Reference

County FIPS codes are needed as the join key across all four sources.
Source: U.S. Census Bureau FIPS reference list — 🔧 readily available,
Florida state FIPS = 12.

## 6. What Happens in Phase 2

For each source above:
1. Try programmatic access first; report immediately if a domain isn't
   reachable from this environment.
2. If manual download is required, provide the exact page name, filter
   ("State = Florida", correct year), expected file format, and where to
   save it (`data/raw/<source_name>/`).
3. Record source, URL, pull/download date, data vintage, and fields used in
   `data/data_dictionary.md`.
4. Never fabricate a placeholder value as real data — synthetic/demo data,
   if used at all to test pipeline code, is clearly labeled and replaced
   before any real analysis.

## 7. Anticipated Manual-Download Items

* CDC PLACES bulk CSV (if the API proves impractical)
* HRSA AHRF (distributed as a full national file, not a simple API)
* CMS Hospital General Information / POS file

Confirmed vs. actually needed once connectivity is tested in Phase 2.
