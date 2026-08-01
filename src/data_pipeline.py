"""Build the Florida county healthcare market analysis dataset.

The pipeline reads the official County Health Rankings Florida workbooks,
which compile Census, BRFSS, AHRF/AMA, and CMS/NPI source measures.
"""
from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs" / "tables"


def _county_rows(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["FIPS"] = pd.to_numeric(out["FIPS"], errors="coerce")
    out = out[out["FIPS"].between(12001, 12133)].copy()
    out["county_fips"] = out["FIPS"].astype(int).astype(str).str.zfill(5)
    return out


def load_release(path: Path, release: int) -> pd.DataFrame:
    """Load the columns needed from one CHR Florida annual workbook."""
    selected = _county_rows(pd.read_excel(path, sheet_name="Select Measure Data", header=1))
    additional = _county_rows(pd.read_excel(path, sheet_name="Additional Measure Data", header=1))

    selected_cols = selected[[
        "county_fips", "County", "# Primary Care Physicians", "Primary Care Physicians Rate"
    ]].rename(columns={
        "County": "county_name",
        "# Primary Care Physicians": "primary_care_physicians",
        "Primary Care Physicians Rate": "pcp_per_100000",
    })

    add_cols = additional[[
        "county_fips", "% Adults with Diabetes", "Other Primary Care Provider Rate",
        "Median Household Income", "% 65 and Over", "Population"
    ]].rename(columns={
        "% Adults with Diabetes": "diabetes_prevalence",
        "Other Primary Care Provider Rate": "other_pcp_per_100000",
        "Median Household Income": "median_household_income",
        "% 65 and Over": "percent_age_65_plus",
        "Population": f"population_{release}",
    })

    result = selected_cols.merge(add_cols, on="county_fips", how="outer", validate="one_to_one")
    result["county_name"] = result["county_name"].str.strip()
    return result


def build_dataset() -> pd.DataFrame:
    """Merge 2024 and 2025 releases, calculate growth and per-10k rates."""
    current = load_release(RAW / "chr_2025_florida.xlsx", 2023)
    prior = load_release(RAW / "chr_2024_florida.xlsx", 2022)[["county_fips", "population_2022"]]
    df = current.merge(prior, on="county_fips", how="left", validate="one_to_one")

    numeric = [
        "population_2023", "population_2022", "diabetes_prevalence",
        "pcp_per_100000", "other_pcp_per_100000", "median_household_income",
        "percent_age_65_plus", "primary_care_physicians"
    ]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["population_growth_rate"] = (
        (df["population_2023"] - df["population_2022"]) / df["population_2022"] * 100
    )
    df["pcp_per_10000"] = df["pcp_per_100000"] / 10
    df["other_pcp_per_10000"] = df["other_pcp_per_100000"] / 10
    df["population"] = df["population_2023"]

    final_cols = [
        "county_fips", "county_name", "population", "population_2022", "population_2023",
        "population_growth_rate", "percent_age_65_plus", "diabetes_prevalence",
        "primary_care_physicians", "pcp_per_10000", "other_pcp_per_10000",
        "median_household_income"
    ]
    df = df[final_cols].sort_values("county_fips").reset_index(drop=True)
    return df


def write_quality_report(df: pd.DataFrame) -> pd.DataFrame:
    rows = [
        {"check": "final_row_count", "value": len(df), "status": "PASS" if len(df) == 67 else "REVIEW"},
        {"check": "unique_fips", "value": df["county_fips"].nunique(), "status": "PASS" if df["county_fips"].nunique() == 67 else "REVIEW"},
        {"check": "duplicate_fips", "value": int(df["county_fips"].duplicated().sum()), "status": "PASS" if not df["county_fips"].duplicated().any() else "FAIL"},
    ]
    for col in df.columns:
        rows.append({"check": f"missing_{col}", "value": int(df[col].isna().sum()), "status": "PASS" if df[col].notna().all() else "REVIEW"})
    report = pd.DataFrame(rows)
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    report.to_csv(OUTPUTS / "data_quality_report.csv", index=False)
    return report


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    df = build_dataset()
    df.to_csv(PROCESSED / "florida_county_market_data.csv", index=False)
    report = write_quality_report(df)
    print(f"Created {len(df)} county rows and {len(df.columns)} columns.")
    print(report.head(5).to_string(index=False))
    print(df.head().to_string(index=False))


if __name__ == "__main__":
    main()
