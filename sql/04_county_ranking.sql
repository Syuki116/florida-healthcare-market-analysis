-- Business purpose: surface priority counties and rank changes across scenarios.
WITH ranked AS (
  SELECT county_name, population, score_balanced, rank_balanced,
         rank_healthcare_need_focus, rank_growth_focus, top10_scenarios,
         DENSE_RANK() OVER (ORDER BY score_balanced DESC) AS sql_dense_rank
  FROM county_scores WHERE eligible_market = 1
)
SELECT *, CASE WHEN top10_scenarios = 3 THEN 'Stable priority'
               WHEN top10_scenarios >= 1 THEN 'Scenario-sensitive'
               ELSE 'Lower priority' END AS recommendation_tier
FROM ranked ORDER BY rank_balanced;
