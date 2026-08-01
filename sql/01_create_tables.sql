-- Tables are loaded from the processed CSVs by src/build_database.py.
-- These statements document the core schema for recruiters reviewing the SQL.
CREATE TABLE IF NOT EXISTS county_market (
  county_fips TEXT PRIMARY KEY, county_name TEXT, population INTEGER,
  population_2022 INTEGER, population_2023 INTEGER, population_growth_rate REAL,
  percent_age_65_plus REAL, diabetes_prevalence REAL,
  primary_care_physicians REAL, pcp_per_10000 REAL,
  other_pcp_per_10000 REAL, median_household_income REAL
);
CREATE TABLE IF NOT EXISTS county_scores AS SELECT * FROM county_market WHERE 0;
