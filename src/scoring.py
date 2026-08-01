"""Transparent percentile scoring for Florida county market screening."""
from __future__ import annotations
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "florida_county_market_data.csv"
OUT_PATH = ROOT / "data" / "processed" / "florida_county_market_scores.csv"

SCENARIOS = {
    "Balanced": {
        "growth_score": .20, "age65_score": .15, "diabetes_score": .15,
        "pcp_shortage_score": .20, "other_pcp_shortage_score": .15, "income_score": .15,
    },
    "Healthcare Need Focus": {
        "growth_score": .10, "age65_score": .20, "diabetes_score": .25,
        "pcp_shortage_score": .25, "other_pcp_shortage_score": .15, "income_score": .05,
    },
    "Growth Focus": {
        "growth_score": .35, "age65_score": .15, "diabetes_score": .10,
        "pcp_shortage_score": .15, "other_pcp_shortage_score": .10, "income_score": .15,
    },
}


def percentile(series: pd.Series, reverse: bool = False) -> pd.Series:
    score = series.rank(method="average", pct=True) * 100
    return 100 - score if reverse else score


def score_counties(df: pd.DataFrame, min_population: int = 50_000) -> pd.DataFrame:
    out = df.copy()
    out["growth_score"] = percentile(out["population_growth_rate"])
    out["age65_score"] = percentile(out["percent_age_65_plus"])
    out["diabetes_score"] = percentile(out["diabetes_prevalence"])
    out["pcp_shortage_score"] = percentile(out["pcp_per_10000"], reverse=True)
    out["other_pcp_shortage_score"] = percentile(out["other_pcp_per_10000"], reverse=True)
    out["income_score"] = percentile(out["median_household_income"])
    out["eligible_market"] = out["population"] >= min_population

    for scenario, weights in SCENARIOS.items():
        slug = scenario.lower().replace(" ", "_")
        out[f"score_{slug}"] = sum(out[col] * weight for col, weight in weights.items())
        out[f"rank_{slug}"] = out[f"score_{slug}"].where(out["eligible_market"]).rank(ascending=False, method="min")

    rank_cols = [c for c in out.columns if c.startswith("rank_")]
    out["top10_scenarios"] = (out[rank_cols] <= 10).sum(axis=1)
    out["stable_top10"] = out["top10_scenarios"] == len(SCENARIOS)
    return out.sort_values("rank_balanced", na_position="last")


def main() -> None:
    df = pd.read_csv(DATA_PATH, dtype={"county_fips": str})
    scored = score_counties(df)
    scored.to_csv(OUT_PATH, index=False)
    print(scored[["county_name", "population", "score_balanced", "rank_balanced", "top10_scenarios"]].head(10).to_string(index=False))

if __name__ == "__main__":
    main()
