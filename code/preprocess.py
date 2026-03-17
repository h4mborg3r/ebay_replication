# -- Step 1 ---
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Load data
df = pd.read_csv('input/PaidSearch.csv')
df['date'] = pd.to_datetime(df['date'])
df['log_revenue'] = np.log(df['revenue'])

# -- Step 2 ---
#  Separate treated and untreated units and create pivot tables

# Filter into treated and untreated groups
treated = df[df['search_stays_on'] == 0]
untreated = df[df['search_stays_on'] == 1]

# Create treated pivot table
treated_pivot = treated.pivot_table(
    index='dma',
    columns='treatment_period',
    values='log_revenue',
    aggfunc='mean'
)
treated_pivot.columns = ['log_revenue_pre', 'log_revenue_post']
treated_pivot['log_revenue_diff'] = (
    treated_pivot['log_revenue_post'] - treated_pivot['log_revenue_pre']
)

# Create untreated pivot table
untreated_pivot = untreated.pivot_table(
    index='dma',
    columns='treatment_period',
    values='log_revenue',
    aggfunc='mean'
)
untreated_pivot.columns = ['log_revenue_pre', 'log_revenue_post']
untreated_pivot['log_revenue_diff'] = (
    untreated_pivot['log_revenue_post'] - untreated_pivot['log_revenue_pre']
)

# Save pivot tables
treated_pivot.to_csv('temp/treated_pivot.csv')
untreated_pivot.to_csv('temp/untreated_pivot.csv')


# -- Step 3 ---
#  Print summary statistics to the console

print("Treated DMAs:", treated['dma'].nunique())
print("Untreated DMAs:", untreated['dma'].nunique())
print(
    "Date range:",
    df['date'].min().date(),
    "to",
    df['date'].max().date()
)


# -- Step 4 ---
#  Reproduce Figure 5.2

# Group by date and treatment/control status, then compute mean revenue
avg_revenue = df.groupby(['date', 'search_stays_on'])['revenue'].mean().reset_index()

# Split into control and treatment series
control = avg_revenue[avg_revenue['search_stays_on'] == 1]
treatment = avg_revenue[avg_revenue['search_stays_on'] == 0]

# Create plot
plt.figure(figsize=(10, 5))
plt.plot(control['date'], control['revenue'], label='Control (search stays on)')
plt.plot(treatment['date'], treatment['revenue'], label='Treatment (search goes off)')

# Add treatment start line
plt.axvline(pd.to_datetime('2012-05-22'), linestyle='--')

# Labels and title
plt.xlabel('Date')
plt.ylabel('Revenue')
plt.title('Figure 5.2: Average Revenue by Group Over Time')
plt.legend()

# Save figure
plt.savefig('output/figures/figure_5_2.png', dpi=300, bbox_inches='tight')
plt.close()


# -- Step 5 ---
#  Reproduce Figure 5.3

# Group by date and treatment/control, compute mean log revenue
avg_log = df.groupby(['date', 'search_stays_on'])['log_revenue'].mean().reset_index()

# Pivot so each date has both control and treatment columns
pivot_log = avg_log.pivot(index='date', columns='search_stays_on', values='log_revenue')

# Compute difference: log(control) - log(treatment)
pivot_log['log_diff'] = pivot_log[1] - pivot_log[0]

# Plot the difference over time
plt.figure(figsize=(10, 5))
plt.plot(pivot_log.index, pivot_log['log_diff'])

# Add treatment start line
plt.axvline(pd.to_datetime('2012-05-22'), linestyle='--')

# Labels and title
plt.xlabel('Date')
plt.ylabel('log(rev_control) - log(rev_treat)')
plt.title('Figure 5.3: Log Revenue Difference Over Time')

# Save figure
plt.savefig('output/figures/figure_5_3.png', dpi=300, bbox_inches='tight')
plt.close()
