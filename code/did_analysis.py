# DID Analysis Script
# Estimates the average treatment effect of turning off eBay's paid search.
# Uses preprocessed pivot tables from preprocess.py.
# Output: LaTeX table in output/tables/did_table.tex

# -- Step 1 ---
import pandas as pd
import numpy as np
# Load pivot tables saved by preprocess.py
treated_pivot = pd.read_csv('temp/treated_pivot.csv', index_col='dma')
untreated_pivot = pd.read_csv('temp/untreated_pivot.csv', index_col='dma')

# -- Step 2 ---
# Compute DID estimate, standard error, and 95% confidence interval

# Mean pre-post log revenue difference for each group
r1_bar = treated_pivot['log_revenue_diff'].mean()
r0_bar = untreated_pivot['log_revenue_diff'].mean()

# DID estimate
gamma_hat = r1_bar - r0_bar

# Sample sizes
n_treated = len(treated_pivot)
n_untreated = len(untreated_pivot)

# Standard error using sample variances
se = np.sqrt(
    treated_pivot['log_revenue_diff'].var() / n_treated
    + untreated_pivot['log_revenue_diff'].var() / n_untreated
)

# 95% confidence interval
ci_lower = gamma_hat - 1.96 * se
ci_upper = gamma_hat + 1.96 * se

# -- Step 3 ---
# Print results to the console

print("DID Results (Log Scale)")
print("=======================")
print(f"Gamma hat: {gamma_hat:.4f}")
print(f"Std Error: {se:.4f}")
print(f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")

# -- Step 4 ---
# Write LaTeX table to file

latex = f"""\\begin{{table}}[h]
\\centering
\\caption{{Difference-in-Differences Estimate of the Effect of Paid Search on Revenue}}
\\begin{{tabular}}{{lc}}
\\hline
& Log Scale \\\\
\\hline
Point Estimate ($\\hat{{\\gamma}}$) & {gamma_hat:.4f} \\\\
Standard Error & {se:.4f} \\\\
95\\% CI & [{ci_lower:.4f}, \\; {ci_upper:.4f}] \\\\
\\hline
\\end{{tabular}}
\\label{{tab:did}}
\\end{{table}}
"""

with open('output/tables/did_table.tex', 'w') as f:
    f.write(latex)
