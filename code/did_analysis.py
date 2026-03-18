# did_analysis.py — DID Analysis Script
# Estimates the average treatment effect of turning off eBay's paid search.
# Method: Compare pre-post log revenue changes between treatment and control DMAs.
# Uses preprocessed pivot tables from preprocess.py.
# Output: LaTeX table in output/tables/did_table.tex
# Reference: Blake et al. (2014), Taddy Ch. 5

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

# Exponentiated (levels) results
gamma_hat_exp = np.exp(gamma_hat)
ci_lower_exp = np.exp(ci_lower)
ci_upper_exp = np.exp(ci_upper)

# -- Step 3 ---
# Print results to the console

print("DID Results (Log Scale)")
print("=======================")
print(f"Gamma hat: {gamma_hat:.4f}")
print(f"Std Error: {se:.4f}")
print(f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")

# -- Step 4 ---
# Write LaTeX table to file

latex = r"""\begin{table}[h]
\centering
\caption{Difference-in-Differences Estimate of the Effect of Paid Search on Revenue}
\begin{tabular}{lcc}
\hline
& Log Scale & Levels (exp) \\
\hline
Point Estimate ($\hat{\gamma}$) & $%.4f$ & $%.4f$ \\
Standard Error & $%.4f$ & --- \\
95\%% CI & $[%.4f, \; %.4f]$ & $[%.4f, \; %.4f]$ \\
\hline
\end{tabular}
\label{tab:did}
\end{table}""" % (
    gamma_hat,
    gamma_hat_exp,
    se,
    ci_lower,
    ci_upper,
    ci_lower_exp,
    ci_upper_exp
)

with open("output/tables/did_table.tex", "w") as f:
    f.write(latex)
