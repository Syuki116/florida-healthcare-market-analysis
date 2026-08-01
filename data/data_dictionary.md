# Data Dictionary

The analytical dataset is derived from the **2025 and 2024 County Health Rankings Florida Data** workbooks. CHR compiles the underlying measures from Census, BRFSS, AHRF/AMA, CMS/NPI, and other official sources.

| Field | Definition | Unit | Underlying source / vintage | Transformation / limitation |
|---|---|---:|---|---|
| county_fips | Florida county FIPS | text | Federal FIPS | Zero-padded 5 digits |
| county_name | County name | text | CHR | Trimmed |
| population | Resident population | people | Census PEP 2023 | CHR 2025 release |
| population_2022 | Prior-year resident population | people | Census PEP 2022 | CHR 2024 release |
| population_growth_rate | Change from 2022 to 2023 | percent | Calculated | `(2023-2022)/2022*100` |
| percent_age_65_plus | Population age 65+ | percent | Census PEP 2023 | County average |
| diabetes_prevalence | Adults with diagnosed diabetes | percent | BRFSS 2022 | Age-adjusted estimate |
| primary_care_physicians | PCP count | clinicians | AHRF/AMA 2021 | Registered supply |
| pcp_per_10000 | PCP supply | per 10,000 | AHRF/AMA 2021 | CHR per-100k rate divided by 10 |
| other_pcp_per_10000 | Other primary-care-provider supply | per 10,000 | CMS NPI 2024 | Includes non-physician primary-care providers; rate divided by 10 |
| median_household_income | Median household income | dollars | SAIPE/ACS, 2023 | Nominal dollars |
| score_* | Scenario opportunity score | 0–100 | Calculated | Weighted percentile score |
| rank_* | Eligible-county scenario rank | rank | Calculated | Population >= 50,000 |
