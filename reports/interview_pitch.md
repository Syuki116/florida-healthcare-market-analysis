# Two-Minute Interview Explanation

I built a Florida healthcare market-screening project to show that I can connect data work to a business decision. The fictional client is an outpatient healthcare organization that wants to narrow 67 Florida counties to a small number for further market research.

I used the County Health Rankings Florida workbooks, which compile data from sources including the Census Population Estimates Program, BRFSS, and the Area Health Resource File. I combined two annual releases to calculate population growth and extracted county-level age, diabetes, primary-care supply, other primary-care-provider supply, and household-income metrics. I standardized FIPS codes, checked duplicates and missing values, and produced one analysis-ready dataset with all 67 counties.

I then loaded the data into SQLite and wrote SQL for quality checks, median comparisons, CTEs, CASE statements, window-function ranking, and recommendation tiers. In Python, I converted six metrics to percentile scores and reversed the provider-supply measures so lower supply represented a larger potential opportunity. I created Balanced, Healthcare Need, and Growth scenarios to show how assumptions affect rankings.

Sumter, St. Lucie, and Flagler ranked highest in the Balanced model, while six counties stayed in the Top 10 across all three scenarios. I presented the findings in a Streamlit dashboard and an executive summary. I was careful not to call the score a profitability model; it is a transparent screening tool, and the next step would be adding local competitor, payer, staffing, real-estate, and travel-time data.
