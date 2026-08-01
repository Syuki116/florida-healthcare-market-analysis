-- Business purpose: verify that every county appears once and required KPIs are populated.
SELECT COUNT(*) AS rows, COUNT(DISTINCT county_fips) AS unique_counties FROM county_market;
SELECT county_fips, COUNT(*) AS records FROM county_market GROUP BY county_fips HAVING COUNT(*) > 1;
SELECT
  SUM(CASE WHEN population IS NULL THEN 1 ELSE 0 END) AS missing_population,
  SUM(CASE WHEN population_growth_rate IS NULL THEN 1 ELSE 0 END) AS missing_growth,
  SUM(CASE WHEN diabetes_prevalence IS NULL THEN 1 ELSE 0 END) AS missing_diabetes,
  SUM(CASE WHEN pcp_per_10000 IS NULL THEN 1 ELSE 0 END) AS missing_pcp
FROM county_market;
