import streamlit as st
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

st.set_page_config(page_title="A/B Test Calculator", layout="centered")
st.title("Bayesian vs. Frequentist A/B Test Calculator")

def frequentist_two_proportion_test(conv_a, n_a, conv_b, n_b):
    """Teo-proportion z-test. Returns rates, z-statistics, and p-value."""
    p_a = conv_a / n_a
    p_b = conv_b /n_b
    p_pool = (conv_a + conv_b) / (n_a + n_b)
    se = np.sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b))
    z = (p_b - p_a) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return {
        "rate_a": p_a,
        "rate_b": p_b,
        "z_stat": z,
        "p_value": p_value,
    }


def bayesian_beta_binomial(cov_a, n_a, conv_b, n_b, prior_alpha=1, prior_beta=1,
                          n_samples=100_000):
    """Beta-Binomial posterior comparison via Monte Carlo sampling."""
    post_a = np.random.beta(prior_alpha + conv_a,
                           prior_beta + (n_a - conv_a),
                           n_samples)
    post_b = np.random.beta(prior_alpha + conv_b,
                           prior_beta + (n_b - conv_b),
                           n_samples)
    prob_b_better = np.mean(post_b > post_a)
    return {
        "post_a": post_a,
        "post_b": post_b,
        "prob_b_better": prob_b_better,
    }

col1, col2 = st.columns(2)

with col1:
    st.subheader("Variant A")
    conv_a = st.number_input("Conversions (A)", min_value=0, value=120, step=1)
    n_a = st.number_input("Total visitors (A)", min_value=1, value=2000, step=1)

with col2:
    st.subheader("Variant B")
    conv_b = st.number_input("Conversions (B)", min_value=0, value=150, step=1)
    n_b = st.number_input("Total visitors (B)", min_value=1, value=2000, step=1)


if st.button("Run analysis", type="primary"):

    freq = frequentist_two_proportion_test(conv_a, n_a, conv_b, n_b)

    st.header("Frequentist: Two-proportion Z-Test")
    fcol1, fcol2, fcol3 = st.co;umns(3)
    fcol1.metric("Rate A", f"{freq['rate_a']:.2%}")
    fcol2.metric("Rate B", f"{freq['rate_b']:.2%}")
    fcol3.metric("p-value", f"{freq['p_value']:.4f}")

    if freq["p_value"] < 0.05:
        st.success("Statistically significant difference at α = 0.05.")
    else:
        st.info("No statistically significant difference at α = 0.05.")