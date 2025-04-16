import numpy as np
import pandas as pd
from scipy.stats import norm, t, skewnorm
from tqdm import tqdm

def construct_portfolio(factors: pd.DataFrame, regime: dict):
    """
    Construct a dynamic portfolio from the five-factor returns with tilting based on market regime.
    
    Weight scheme:
      - Expansion: Overweight market factor.
          Weights: [MKT, SMB, HML, RMW, CMA] = [0.40, 0.15, 0.15, 0.15, 0.15]
      - Recession: Reduce market exposure; overweight defensive factors.
          Weights: [0.15, 0.22, 0.22, 0.20, 0.21]
      - Contraction: Overweight value and quality factors.
          Weights: [0.15, 0.15, 0.30, 0.25, 0.15]
      - Recovery: Balance growth and defensive factors.
          Weights: [0.25, 0.25, 0.15, 0.15, 0.20]
    
    Args:
        factors (DataFrame): Must have columns ['MKT', 'SMB', 'HML', 'RMW', 'CMA'].
        regime (dict): Market regime info.
    
    Returns:
        Series: Daily portfolio returns.
    """
    if regime['regime'] == 'Expansion':
        weights = np.array([0.40, 0.15, 0.15, 0.15, 0.15])
    elif regime['regime'] == 'Recession':
        weights = np.array([0.15, 0.22, 0.22, 0.20, 0.21])
    elif regime['regime'] == 'Contraction':
        weights = np.array([0.15, 0.15, 0.30, 0.25, 0.15])
    else:  # Recovery
        weights = np.array([0.25, 0.25, 0.15, 0.15, 0.20])
    
    weights = weights / weights.sum()  # Normalize weights
    portfolio_returns = factors.dot(weights)
    return portfolio_returns

def monte_carlo_var_cvar(returns: pd.Series, confidence_level=0.95, n_simulations=100000, horizon=1, method='norm'):
    """
    Calculate VaR and CVaR using Monte Carlo simulation.
    
    Args:
        returns (Series): Historical daily returns.
        confidence_level (float): Confidence level (e.g., 0.95 for 95%).
        n_simulations (int): Number of Monte Carlo simulations.
        horizon (int): Time horizon in days.
        method (str): Distribution method ('norm', 't', or 'empirical').
    
    Returns:
        tuple: (VaR, CVaR) at the specified confidence level.
    """
    alpha = 1 - confidence_level
    
    # Estimate parameters from historical returns
    mu = returns.mean()
    sigma = returns.std()
    
    # Generate simulated returns
    if method == 'norm':
        # Normal distribution
        simulated_returns = np.random.normal(mu * horizon, sigma * np.sqrt(horizon), n_simulations)
    elif method == 't':
        # Student's t-distribution (better for fat tails)
        df = 5  # degrees of freedom - can be estimated from data
        simulated_returns = t.rvs(df, loc=mu * horizon, scale=sigma * np.sqrt(horizon), size=n_simulations)
    elif method == 'empirical':
        # Empirical bootstrap (resampling from historical returns)
        simulated_returns = np.random.choice(returns, size=n_simulations, replace=True)
    elif method == 'skewed':
        # Skewed normal distribution
        skewness = returns.skew()
        a = skewness  # skewness parameter (simplified)
        simulated_returns = skewnorm.rvs(a, loc=mu * horizon, scale=sigma * np.sqrt(horizon), size=n_simulations)
    else:
        raise ValueError(f"Unsupported method: {method}")
    
    # Calculate VaR and CVaR
    sorted_returns = np.sort(simulated_returns)
    var_index = int(n_simulations * alpha)
    var = -sorted_returns[var_index]
    cvar = -sorted_returns[:var_index].mean()
    
    return var, cvar

def calculate_risk_metrics(returns: pd.Series, risk_free_rate=0.0, mc_method='t'):
    """
    Calculate comprehensive risk metrics for a series of portfolio returns.
    
    Metrics include:
      - Annualized volatility
      - Annualized Sharpe ratio
      - Monte Carlo VaR (95%)
      - Monte Carlo CVaR (95%)
      - Maximum drawdown
      - Skewness and kurtosis
    
    Args:
        returns (Series): Daily portfolio returns.
        risk_free_rate (float): Annual risk-free rate.
        mc_method (str): Monte Carlo simulation method.
    
    Returns:
        dict: Risk metrics.
    """
    volatility = returns.std() * np.sqrt(252)
    excess_return = returns.mean() - (risk_free_rate / 252)
    sharpe_ratio = (excess_return / returns.std()) * np.sqrt(252)
    
    # Monte Carlo VaR and CVaR calculation
    var_95, cvar_95 = monte_carlo_var_cvar(returns, confidence_level=0.95, method=mc_method)
    
    # Historical VaR and CVaR for comparison
    hist_var_95 = -returns.quantile(0.05)
    hist_cvar_95 = -returns[returns <= -hist_var_95].mean()
    
    cumulative = (1 + returns).cumprod()
    max_drawdown = (cumulative / cumulative.cummax() - 1).min()
    
    skewness = returns.skew()
    kurtosis = returns.kurtosis()
    
    return {
        'Annualized Volatility': round(volatility, 4),
        'Sharpe Ratio': round(sharpe_ratio, 4),
        'VaR (95%)': round(var_95, 4),
        'CVaR (95%)': round(cvar_95, 4),
        'Historical VaR (95%)': round(hist_var_95, 4),
        'Historical CVaR (95%)': round(hist_cvar_95, 4),
        'Maximum Drawdown': round(max_drawdown, 4),
        'Skewness': round(skewness, 4),
        'Kurtosis': round(kurtosis, 4)
    }

def generate_correlated_scenario_returns(returns: pd.Series, shock_params):
    """
    Generate scenario returns with specified shock parameters that maintain realistic
    correlations and create meaningful variations in higher moments (skewness, kurtosis).
    
    Args:
        returns (Series): Original portfolio returns.
        shock_params (dict): Parameters for the shock including:
            - 'multiplicative': Factor to multiply returns by
            - 'additive': Constant to add to returns
            - 'vol_factor': Factor to adjust volatility
            - 'skew_factor': Factor to adjust skewness
            - 'tail_factor': Factor to enhance tail events (affects kurtosis)
    
    Returns:
        Series: Adjusted returns for the stress scenario.
    """
    # Extract parameters
    multiplicative = shock_params.get('multiplicative', 1.0)
    additive = shock_params.get('additive', 0)
    vol_factor = shock_params.get('vol_factor', 1.0)
    skew_factor = shock_params.get('skew_factor', 0)
    tail_factor = shock_params.get('tail_factor', 1.0)
    
    # Base adjustment
    adjusted_returns = returns * multiplicative + additive
    
    # Adjust volatility
    if vol_factor != 1.0:
        mean_return = adjusted_returns.mean()
        centered_returns = adjusted_returns - mean_return
        adjusted_returns = (centered_returns * vol_factor) + mean_return
    
    # Enhance tail events for kurtosis
    if tail_factor != 1.0:
        # Find returns beyond 2 standard deviations
        threshold = 2 * adjusted_returns.std()
        extreme_mask = adjusted_returns.abs() > threshold
        
        # Apply tail factor only to extreme returns
        tail_adjustment = adjusted_returns.copy()
        tail_adjustment[extreme_mask] *= tail_factor
        adjusted_returns = tail_adjustment
    
    # Apply skewness adjustment
    if skew_factor != 0:
        # Create a skew component proportional to the cube of standardized returns
        mean = adjusted_returns.mean()
        std = adjusted_returns.std()
        z_scores = (adjusted_returns - mean) / std
        skew_component = skew_factor * (z_scores**3) * std / 10
        
        adjusted_returns = adjusted_returns + skew_component
    
    return adjusted_returns

def stress_test_portfolio(returns: pd.Series, scenarios: list, mc_method='t'):
    """
    Apply stress scenarios to portfolio returns and compute risk metrics.
    
    Each scenario now has a more sophisticated shock model that affects not just
    the mean and variance but also higher moments like skewness and kurtosis.
       
    Args:
        returns (Series): Original daily portfolio returns.
        scenarios (list): List of stress scenarios with shock parameters.
        mc_method (str): Monte Carlo simulation method for VaR calculations.
    
    Returns:
        dict: Dictionary with scenario names as keys and risk metrics as values.
    """
    stressed_results = {}
    
    for scenario in tqdm(scenarios, desc="Running stress tests"):
        shock_params = {
            'multiplicative': 1 + scenario.get('shock', 0),
            'additive': scenario.get('additive', 0),
            'vol_factor': scenario.get('vol_factor', 1.0),
            'skew_factor': scenario.get('skew_factor', 0),
            'tail_factor': scenario.get('tail_factor', 1.0)
        }
        
        stressed_returns = generate_correlated_scenario_returns(returns, shock_params)
        metrics = calculate_risk_metrics(stressed_returns, mc_method=mc_method)
        stressed_results[scenario['name']] = metrics
    
    return stressed_results

if __name__ == "__main__":
    from factors import download_fama_french_5_factors
    from macro import analyze_market_regime, define_stress_scenarios
    
    factors = download_fama_french_5_factors()
    regime = analyze_market_regime()
    portfolio = construct_portfolio(factors, regime)
    metrics = calculate_risk_metrics(portfolio)
    stressed = stress_test_portfolio(portfolio, define_stress_scenarios())
    
    print("Market Regime:", regime)
    print("Risk Metrics:", metrics)
    print("Stress Test Metrics:", stressed)