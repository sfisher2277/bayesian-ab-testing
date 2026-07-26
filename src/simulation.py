"""Sequential monitoring ("peeking") simulation for A/B test analysis."""
import numpy as np
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest

from bayesian import compute_beta_posterior, prob_a_greater_than_b


def run_peeking_simulation(data_a, data_b, step=200, seed=42):
    """Simulate sequential monitoring by recomputing frequentist and Bayesian
    metrics at increasing sample sizes.
    
    Parameters
    ----------
    data_a, data_b : array-like of 0/1 outcomes, already shuffled to simulate
        arrival order (e.g. a shuffled pandas Series of 'converted' values)
    step : int, sample size increment betweem checkpoints
    seed : int, random seed for the Bayesian Monte Carlo sampling
    
    Returns a DataFrame with one row per checkpoint: n, p_value, prob_a_better
    """
    max_n = min(len(data_a), len(data_b))
    sample_sizes = np.arange(step, max_n, step)

    rng = np.random.default_rng(seed)
    results = []

    for n in sample_sizes:
        subset_a = data_a[:n]
        subset_b = data_b[:n]

        conv_a = subset_a.sum()
        conv_b = subset_b.sum()

        #Frequentist p-value at this checkpoint
        count = np.array([conv_a, conv_b])
        nobs = np.array([n, n])
        _, p_val = proportions_ztest(count, nobs)

        #Bayesian posterior probability at this checkpoint
        posterior_a = compute_beta_posterior(conv_a, n)
        posterior_b = compute_beta_posterior(conv_b, n)
        prob_a_better = prob_a_greater_than_b(
            posterior_a['alpha'], posterior_a['beta'],
            posterior_b['alpha'], posterior_b['beta'],
            n_samples=5000, seed=int(rng.integers(0, 1_000_000))
        )

        results.append({'n': n, 'p_value': p_val, 'prob_a_better': prob_a_better})

    return pd.DataFrame(results)  