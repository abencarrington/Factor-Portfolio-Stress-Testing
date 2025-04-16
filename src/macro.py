import yfinance as yf
import pandas as pd
import numpy as np

def analyze_market_regime(start_date='2020-01-01', end_date=None):
    """
    Analyze the current market regime using SPY historical data.
    
    Uses:
      - 30-day rolling annualized volatility of SPY returns.
      - 50-day and 200-day moving averages to assess trend.
      - 14-day RSI to assess momentum
      
    Classification rules:
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
            - 'rsi': Relative Strength Index value.
    """
    if end_date is None:
        end_date = pd.Timestamp.today().strftime('%Y-%m-%d')
    
    spy = yf.download("SPY", start=start_date, end=end_date)
    spy_returns = spy['Close'].pct_change().dropna()
    
    # Compute volatility
    rolling_vol = spy_returns.rolling(window=30).std() * np.sqrt(252)
    latest_vol = rolling_vol.iloc[-1].item()
    
    # Compute moving averages
    ma50 = spy['Close'].rolling(window=50).mean().iloc[-1].item()
    ma200 = spy['Close'].rolling(window=200).mean().iloc[-1].item()
    
    # Compute RSI
    delta = spy['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs.iloc[-1]))
    
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
        'trend': trend,
        'rsi': rsi
    }

def define_stress_scenarios():
    """
    Define a set of hypothetical macroeconomic stress scenarios with enhanced parameters
    to create more realistic variations in risk metrics.
    
    Each scenario includes:
      - 'shock': Multiplicative factor (e.g., -0.30 means returns become 70% of original)
      - 'additive': Additional additive shock to simulate a downward shift
      - 'vol_factor': Volatility scaling factor
      - 'skew_factor': Skewness adjustment factor
      - 'tail_factor': Factor to enhance tail events (affecting kurtosis)
      
    Returns:
        list: A list of scenarios with comprehensive parameters.
    """
    scenarios = [
        {
            'name': 'Severe Recession', 
            'shock': -0.30,                 # Significant reduction in returns
            'additive': -0.001,             # Additional negative shift
            'vol_factor': 1.75,             # Increased volatility
            'skew_factor': -0.7,            # Negative skew (more extreme negative returns)
            'tail_factor': 1.5,             # Fatter tails (higher kurtosis)
            'description': 'A severe economic downturn with increased volatility, negative skew, and extreme tail events.'
        },
        {
            'name': 'Rapid Rate Hike', 
            'shock': -0.15,                 # Moderate reduction in returns
            'additive': -0.0005,            # Small negative shift
            'vol_factor': 1.35,             # Moderately increased volatility
            'skew_factor': -0.4,            # Slight negative skew
            'tail_factor': 1.3,             # Moderately fatter tails
            'description': 'A scenario where central banks rapidly increase interest rates, causing market turbulence.'
        },
        {
            'name': 'Market Crash',  
            'shock': -0.40,                 # Major reduction in returns
            'additive': -0.002,             # Larger negative shift
            'vol_factor': 2.2,              # Dramatically increased volatility
            'skew_factor': -1.2,            # Strong negative skew
            'tail_factor': 2.0,             # Much fatter tails
            'description': 'A sudden market crash with extreme volatility and strongly negative skewed returns.'
        },
        {
            'name': 'Mild Correction', 
            'shock': -0.05,                 # Minor reduction in returns
            'additive': -0.0002,            # Very small negative shift
            'vol_factor': 1.15,             # Slightly increased volatility
            'skew_factor': -0.2,            # Minimal negative skew
            'tail_factor': 1.1,             # Slightly fatter tails
            'description': 'A modest market correction with slightly elevated volatility.'
        },
        {
            'name': 'Stagflation', 
            'shock': -0.12,                 # Moderate reduction in returns
            'additive': -0.0008,            # Moderate negative shift
            'vol_factor': 1.5,              # Increased volatility
            'skew_factor': -0.3,            # Moderate negative skew
            'tail_factor': 1.25,            # Moderately fatter tails
            'description': 'A period of high inflation combined with slow economic growth and elevated market uncertainty.'
        }
    ]
    return scenarios

if __name__ == "__main__":
    regime_info = analyze_market_regime()
    print("Current Market Regime:", regime_info)
    print("Stress Scenarios:", define_stress_scenarios())