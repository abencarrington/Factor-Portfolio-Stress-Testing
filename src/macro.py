import yfinance as yf
import pandas as pd
import numpy as np

def analyze_market_regime(start_date='2020-01-01', end_date=None):
    """
    Analyze the current market regime using SPY historical data.
    
    Uses:
      - 30-day rolling annualized volatility of SPY returns.
      - 50-day and 200-day moving averages to assess trend.
      
    Classification rules (example):
      - If volatility > 0.25: 'Recession'
      - Else if volatility < 0.15 and 50-day MA > 200-day MA: 'Expansion'
      - Else if 50-day MA < 200-day MA: 'Contraction'
      - Otherwise: 'Recovery'
    
    Args:
        start_date (str): Start date for SPY data.
        end_date (str): End date (defaults to today if None).
    
    Returns:
        dict: Contains:
            - 'regime': The classified market regime.
            - 'description': A short description.
            - 'volatility': Latest computed annualized volatility.
            - 'trend': 'Bullish' or 'Bearish'.
    """
    if end_date is None:
        end_date = pd.Timestamp.today().strftime('%Y-%m-%d')
    
    spy = yf.download("SPY", start=start_date, end=end_date)['Close']
    spy_returns = spy.pct_change().dropna()
    
    rolling_vol = spy_returns.rolling(window=30).std() * (252 ** 0.5)
    latest_vol = rolling_vol.iloc[-1].item()
    
    # Compute moving averages and convert them to scalars
    ma50 = spy.rolling(window=50).mean().iloc[-1].item()
    ma200 = spy.rolling(window=200).mean().iloc[-1].item()
    
    trend = "Bullish" if ma50 > ma200 else "Bearish"
    
    if latest_vol > 0.25:
        regime = "Recession"
        description = "High volatility environment indicating potential recession."
    elif latest_vol < 0.15 and trend == "Bullish":
        regime = "Expansion"
        description = "Low volatility with bullish trend, indicating economic expansion."
    elif trend == "Bearish":
        regime = "Contraction"
        description = "Bearish trend indicating economic contraction."
    else:
        regime = "Recovery"
        description = "Transitioning environment, potentially recovering."
    
    return {
        'regime': regime,
        'description': description,
        'volatility': latest_vol,
        'trend': trend
    }

def define_stress_scenarios():
    """
    Define a set of hypothetical macroeconomic stress scenarios.
    
    Each scenario now includes:
      - 'shock': the multiplicative factor (e.g., -0.30 means returns become 70% of original)
      - 'additive': an additional additive shock to simulate a downward shift
      
    Returns:
        list: A list of scenarios with keys 'name', 'shock', 'additive', and 'description'.
    """
    scenarios = [
        {'name': 'Severe Recession', 'shock': -0.30, 'additive': -0.001, 
         'description': 'A sharp downturn with an additional negative shift.'},
        {'name': 'Rapid Rate Hike',  'shock': -0.15, 'additive': -0.0005, 
         'description': 'A moderate drop with a small negative shift.'},
        {'name': 'Market Crash',      'shock': -0.40, 'additive': -0.002, 
         'description': 'A significant drop with a larger negative shift.'},
        {'name': 'Mild Correction',   'shock': -0.05, 'additive': -0.0002, 
         'description': 'A minor drop with a slight negative shift.'}
    ]
    return scenarios

if __name__ == "__main__":
    regime_info = analyze_market_regime()
    print("Current Market Regime:", regime_info)
    print("Stress Scenarios:", define_stress_scenarios())