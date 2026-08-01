import pandas as pd
from src.scoring import score_counties

def test_scores_and_eligibility():
    df = pd.DataFrame({
        'county_fips':['12001','12003'], 'county_name':['A','B'],
        'population':[100000,10000], 'population_growth_rate':[2,1],
        'percent_age_65_plus':[15,20], 'diabetes_prevalence':[10,12],
        'pcp_per_10000':[8,4], 'other_pcp_per_10000':[15,8],
        'median_household_income':[70000,50000]
    })
    out = score_counties(df)
    assert out['score_balanced'].between(0,100).all()
    assert out.loc[out.county_name=='A','eligible_market'].iloc[0]
    assert not out.loc[out.county_name=='B','eligible_market'].iloc[0]
