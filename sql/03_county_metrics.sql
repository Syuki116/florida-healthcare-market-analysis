-- Business purpose: identify counties with above-median growth/need and below-median PCP supply.
WITH medians AS (
  SELECT
    (SELECT AVG(population_growth_rate) FROM (SELECT population_growth_rate FROM county_market ORDER BY population_growth_rate LIMIT 2 - (SELECT COUNT(*) FROM county_market) % 2 OFFSET (SELECT (COUNT(*) - 1) / 2 FROM county_market))) AS med_growth,
    (SELECT AVG(diabetes_prevalence) FROM (SELECT diabetes_prevalence FROM county_market ORDER BY diabetes_prevalence LIMIT 2 - (SELECT COUNT(*) FROM county_market) % 2 OFFSET (SELECT (COUNT(*) - 1) / 2 FROM county_market))) AS med_diabetes,
    (SELECT AVG(pcp_per_10000) FROM (SELECT pcp_per_10000 FROM county_market ORDER BY pcp_per_10000 LIMIT 2 - (SELECT COUNT(*) FROM county_market) % 2 OFFSET (SELECT (COUNT(*) - 1) / 2 FROM county_market))) AS med_pcp
)
SELECT m.county_name, m.population, m.population_growth_rate, m.diabetes_prevalence, m.pcp_per_10000,
       CASE WHEN m.population_growth_rate > x.med_growth THEN 'Above median' ELSE 'At/below median' END AS growth_position,
       CASE WHEN m.diabetes_prevalence > x.med_diabetes THEN 'Above median need' ELSE 'At/below median need' END AS need_position,
       CASE WHEN m.pcp_per_10000 < x.med_pcp THEN 'Below median supply' ELSE 'At/above median supply' END AS supply_position
FROM county_market m CROSS JOIN medians x
ORDER BY m.population_growth_rate DESC;
