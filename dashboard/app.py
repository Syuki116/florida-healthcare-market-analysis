"""Streamlit dashboard for the Florida Healthcare Market Opportunity Analysis."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'processed' / 'florida_county_market_scores.csv'

st.set_page_config(page_title='Florida Healthcare Market Opportunity', layout='wide')
@st.cache_data
def load_data():
    return pd.read_csv(DATA, dtype={'county_fips': str})

df = load_data()
SCENARIOS = {
    'Balanced': ('score_balanced','rank_balanced'),
    'Healthcare Need Focus': ('score_healthcare_need_focus','rank_healthcare_need_focus'),
    'Growth Focus': ('score_growth_focus','rank_growth_focus'),
}

st.title('Florida Healthcare Market Opportunity Analysis')
st.caption('County-level screening tool for further outpatient-clinic market research — not a profitability forecast.')
scenario = st.sidebar.selectbox('Scoring scenario', list(SCENARIOS))
score_col, rank_col = SCENARIOS[scenario]
eligible = df[df['eligible_market']].sort_values(rank_col)

tab1, tab2, tab3, tab4 = st.tabs(['Executive Overview','County Ranking','County Comparison','Scenario Analysis'])
with tab1:
    top = eligible.head(3)
    cols = st.columns(3)
    for col, (_, r) in zip(cols, top.iterrows()):
        col.metric(r['county_name'], f"{r[score_col]:.1f}/100", f"Rank #{int(r[rank_col])}")
        col.write(f"Growth: {r['population_growth_rate']:.1f}% | 65+: {r['percent_age_65_plus']:.1f}%")
        col.write(f"Diabetes: {r['diabetes_prevalence']:.1f}% | PCPs: {r['pcp_per_10000']:.1f}/10k")
    st.info('Priority means “investigate next.” Real estate, payer mix, staffing costs, reimbursement, travel patterns, and local competitor capacity are not included.')
    fig = px.bar(eligible.head(10), x='county_name', y=score_col, title=f'Top 10 Counties — {scenario}', labels={score_col:'Opportunity score','county_name':'County'})
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    metric_options = {
    'Overall opportunity score': score_col,
    'Population growth': 'population_growth_rate',
    'Age 65+': 'percent_age_65_plus',
    'Diabetes prevalence': 'diabetes_prevalence',
    'PCP availability (lower may indicate gap)': 'pcp_per_10000',
    }

    metric_label = st.selectbox(
        'Rank by metric',
        list(metric_options.keys())
    )

    metric = metric_options[metric_label]
    
    asc = metric == 'pcp_per_10000'
    view = df.sort_values(metric, ascending=asc)
    st.dataframe(view[['county_name','population','population_growth_rate','percent_age_65_plus','diabetes_prevalence','pcp_per_10000','other_pcp_per_10000','median_household_income',score_col,rank_col]], use_container_width=True, hide_index=True)

with tab3:
    defaults = eligible.head(3)['county_name'].tolist()
    choices = st.multiselect('Select counties', sorted(df['county_name']), default=defaults, max_selections=5)
    comp = df[df['county_name'].isin(choices)]
    long = comp.melt(id_vars='county_name', value_vars=['population_growth_rate','percent_age_65_plus','diabetes_prevalence','pcp_per_10000','other_pcp_per_10000'], var_name='metric', value_name='value')
    st.plotly_chart(px.bar(long, x='metric', y='value', color='county_name', barmode='group', title='Selected County KPI Comparison'), use_container_width=True)
    st.dataframe(comp[['county_name','population','median_household_income',score_col,rank_col]], hide_index=True, use_container_width=True)

with tab4:
    rank_view = df[df['eligible_market']].copy()
    rank_long = rank_view.melt(id_vars='county_name', value_vars=['rank_balanced','rank_healthcare_need_focus','rank_growth_focus'], var_name='scenario', value_name='rank')
    rank_long = rank_long[rank_long['rank'] <= 10]
    st.plotly_chart(px.line(rank_long, x='scenario', y='rank', color='county_name', markers=True, title='Top-10 Rank Movement Across Scenarios'), use_container_width=True)
    st.dataframe(df.sort_values('rank_balanced')[['county_name','rank_balanced','rank_healthcare_need_focus','rank_growth_focus','top10_scenarios','stable_top10']].head(15), hide_index=True, use_container_width=True)

with st.expander('Methodology and limitations'):
    st.markdown('''Six metrics are converted to percentile scores. Lower provider supply is reversed to represent a larger potential access gap. The model uses a 50,000-person eligibility screen and three analyst-selected weight scenarios. County Health Rankings compiles the underlying Census, BRFSS, AHRF/AMA, and CMS/NPI measures. This is a screening model, not a site-selection or profitability model.''')
