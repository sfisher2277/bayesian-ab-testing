"""Bayesian statistical functions for A/B test analysis (Beta-Binomial model)."""
import numpy as np
from scipy import stats


def compute_beta_posterior(conversions, totals, alpha_prior=1, beta_prior=1):
    """Compute the Beta posterior for a group's conversion rate.
    
    Uses a Beta(alpha_prior, beta_prior) prior, updated with observed
    conversions/totals. Default prior is Beta(1,1), i.e. uninformed/flat.
    
    Returns a dict with the posterior's aplha, beta, mean, and 95% credible interval.
    """
    alpha_post = alpha_prior + conversions
    beta_post = beta_prior + (totals - conversions)

    mean = alpha_post / (alpha_post + beta_post)
    ci = stats.beta.ppf([0.025, 0.975], alpha_post, beta_post)

    return {
        'alpha': alpha_post,
        'beta': beta_post,
        'mean': mean,
        'ci': ci,
    }


def prob_a_greater_than_b(alpha_a, beta_a, alpha_b, beta_b, n_samples=100000, seed=42):
    """Estimate P(rate_a > rate_b) via Monte Carlo sampling from each posterior."""
    rng = np.random.default_rng(seed)
    samples_a = stats.beta.rvs(alpha_a, beta_a, size=n_samples, random_state=rng)
    samples_b = stats.beta.rvs(alpha_b, bets_b, size=n_samples, random_state=rng)
    return (samples_a > samples_b).mean()