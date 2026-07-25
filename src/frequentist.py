"""Frequentist statistical functions for A/B test analysis."""
import numpy as np
from statsmodels.stats.proportion import proportions_ztest, proportion_confint


def run_two_proportion_ztest(conversions_a, totals_a, conversions_b, totals_b):
        """Run a two-proportion z-test comparing conversion rates between two groups.
        
        Returns a dict with the z-statistic, p-value, and each group's rate and 95% CI.
        """

        count = np.array([conversions_a, conversions_b])
        nobs = np.array([totals_a, totals_b])
        z_stat, p_value = proportions_ztest(count, nobs)

        ci_a = proportion_confint(conversions_a, totals_a, alpha=0.05)
        ci_b = proportion_confint(conversions_b, totals_b, alpha=0.05)

        return{
                'z_stat': z_stat,
                'p_value': p_value,
                'rate_a': conversions_a / totals_a,
                'rate_b': conversions_b / totals_b,
                'ci_a': ci_a,
                'ci_b': ci_b,
        }