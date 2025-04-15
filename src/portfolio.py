import numpy as np
import pandas as pd
from scipy.stats import norm

def construct_portfolio(factors: pd.DataFrame, regime: dict):
    """
    Construct a dynamic portfolio from the five-factor returns with tilting based on market regime.
    
    Weight scheme example:
      - Expansion: Overweight market factor.
          Weights: [MKT, SMB, HML, RMW, CMA] = [0.40, 0.15, 0.15, 0.15, 0.15]
      - Recession: Reduce market exposure; overweight defensive factors.
          Weights: [0.15, 0.22, 0.22, 0.20, 0.21]
      - Otherwise (Contraction, Recovery): Equal weights.
          Weights: [0.20, 0.20, 0.20, 0.20, 0.20]
    
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
    else:
        weights = np.full(5, 0.20)
    
    weights = weights / weights.sum()  # Normalize weights
    portfolio_returns = factors.dot(weights)
    return portfolio_returns

def calculate_risk_metrics(returns: pd.Series, risk_free_rate=0.0):
    """
    Calculate comprehensive risk metrics for a series of portfolio returns.
    
    Metrics include:
      - Annualized volatility
      - Annualized Sharpe ratio
      - Historical VaR (95%)
      - Historical CVaR (95%)
      - Maximum drawdown
      - Skewness and kurtosis
    
    Args:
        returns (Series): Daily portfolio returns.
        risk_free_rate (float): Default 0.
    
    Returns:
        dict: Risk metrics.
    """
    volatility = returns.std() * (252 ** 0.5)
    sharpe_ratio = (returns.mean() / returns.std()) * (252 ** 0.5)
    var_95 = -returns.quantile(0.05)
    cvar_95 = -returns[returns <= returns.quantile(0.05)].mean()
    
    cumulative = (1 + returns).cumprod()
    max_drawdown = (cumulative / cumulative.cummax() - 1).min()
    
    skewness = returns.skew()
    kurtosis = returns.kurtosis()
    
    return {
        'Annualized Volatility': round(volatility, 4),
        'Sharpe Ratio': round(sharpe_ratio, 4),
        'VaR 95': round(var_95, 4),
        'CVaR 95': round(cvar_95, 4),
        'Maximum Drawdown': round(max_drawdown, 4),
        'Skewness': round(skewness, 4),
        'Kurtosis': round(kurtosis, 4)
    }

def stress_test_portfolio(returns: pd.Series, scenarios: list):
    """
    Apply stress scenarios to portfolio returns and compute risk metrics.
    
    Each scenario adjusts returns using both a multiplicative and additive shock.
    That is, for a given scenario,
    stressed_returns = returns * (1 + scenario['shock']) + scenario['additive']
       
    This method will alter both the scale and distribution shape, so that metrics like Sharpe ratio,
    skewness, and kurtosis (which are scale- and shift-sensitive, respectively) will change.
    
    Args:
        returns (Series): Original daily portfolio returns.
        scenarios (list): List of stress scenarios.
    
    Returns:
        dict: Dictionary with scenario names as keys and risk metrics as values.
    """
    stressed_results = {}
    for scenario in scenarios:
        stressed_returns = returns * (1 + scenario['shock']) + scenario['additive']
        metrics = calculate_risk_metrics(stressed_returns)
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