"""Create a portable SQLite database and run project SQL scripts."""
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / 'data' / 'processed' / 'florida_healthcare.sqlite'

def main() -> None:
    market = pd.read_csv(ROOT/'data/processed/florida_county_market_data.csv', dtype={'county_fips':str})
    scores = pd.read_csv(ROOT/'data/processed/florida_county_market_scores.csv', dtype={'county_fips':str})
    with sqlite3.connect(DB) as con:
        market.to_sql('county_market', con, if_exists='replace', index=False)
        scores.to_sql('county_scores', con, if_exists='replace', index=False)
        con.execute('CREATE INDEX IF NOT EXISTS idx_market_fips ON county_market(county_fips)')
        con.execute('CREATE INDEX IF NOT EXISTS idx_scores_rank ON county_scores(rank_balanced)')
    print(f'Created {DB}')
if __name__ == '__main__': main()
