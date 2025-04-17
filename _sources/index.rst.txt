.. Dynamic Factor-Tilted Portfolio with Macro Stress Testing documentation master file

Dynamic Factor-Tilted Portfolio with Macro Stress Testing
===========================================================

Overview
--------

This project dynamically constructs a factor-tilted portfolio using the Fama–French 5 Factor model.  
The historical factor data is sourced directly from Kenneth French's website via web scraping.  
The portfolio adjusts its weights based on the current market regime (determined via SPY's volatility and moving averages) and undergoes stress testing based on various market scenarios.

Features:

- **Factor Modeling:** Uses the Fama-French 5 Factor model, which includes:
   - **MKT (Market):** The excess return of the market over the risk-free rate, representing systematic market risk
   - **SMB (Small Minus Big):** The return spread between small and large market capitalization stocks, capturing the size premium
   - **HML (High Minus Low):** The return spread between high and low book-to-market stocks, measuring the value premium
   - **RMW (Robust Minus Weak):** The return spread between stocks with robust vs. weak profitability
   - **CMA (Conservative Minus Aggressive):** The return spread between companies with conservative vs. aggressive investment strategies

- **Market Regime Analysis:** Uses SPY's rolling volatility, moving averages, and RSI to determine the current market environment.

- **Dynamic Factor Tilting:** Adjusts portfolio weights based on the identified market regime.

- **Advanced Risk Analysis:** Calculates risk metrics including:
   - **Monte Carlo VaR/CVaR:** Estimates risk using Student's t-distribution simulations to better capture fat-tailed market behavior. Value-at-Risk (VaR) represents the potential loss at a given confidence level (e.g., 95%), while Conditional VaR (CVaR) estimates the expected loss when exceeding VaR threshold, providing a more complete view of tail risk.
   - **Traditional metrics:** Volatility, Sharpe ratio, and maximum drawdown
   - **Higher-moment statistics:** Skewness (distribution asymmetry) and kurtosis (tail thickness)

- **Sophisticated Stress Testing:** Evaluates performance under various adverse scenarios with detailed modeling of:
   - Return impacts (multiplicative and additive effects)
   - Volatility scaling
   - Skewness adjustments
   - Tail behavior (kurtosis) modifications

- **Interactive Visualizations:** Provides Plotly-based interactive charts for deeper analysis.

- **Automated Documentation:** Builds a comprehensive site with Sphinx, including interactive elements.

- **GitHub Pages Deployment:** Automatically updates the site on a weekly schedule.


Portfolio Performance
---------------------
.. raw:: html
   :file: _static/portfolio_returns.html

Factor Correlations
------------------
Understanding factor correlations is crucial for diversification and factor tilting:

.. raw:: html
   :file: _static/factor_correlation.html

Risk Profile Comparison
----------------------
The radar chart below compares risk metrics across different stress scenarios:

.. raw:: html
   :file: _static/risk_radar.html

Risk Metrics
------------
The following interactive charts display the risk metrics computed for both the baseline portfolio and under different stress scenarios.

Annualized Volatility
~~~~~~~~~~~~~~~~~~~~~
.. raw:: html
   :file: _static/annualized_volatility.html

Sharpe Ratio
~~~~~~~~~~~
.. raw:: html
   :file: _static/sharpe_ratio.html

Value-at-Risk (95%)
~~~~~~~~~~~~~~~~
.. raw:: html
   :file: _static/var_(95%).html

Conditional Value-at-Risk (95%)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. raw:: html
   :file: _static/cvar_(95%).html

Maximum Drawdown
~~~~~~~~~~~~~~
.. raw:: html
   :file: _static/maximum_drawdown.html

Skewness
~~~~~~~~
.. raw:: html
   :file: _static/skewness.html

Kurtosis
~~~~~~~~
.. raw:: html
   :file: _static/kurtosis.html

How It Works
------------

1. **Data and Factor Computation:**  
   The project scrapes Kenneth French's [data library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html)  
   to download the "F-F Research Data 5 Factors 2x3 Daily" dataset.  
   Data is parsed and converted from percentages to decimals.

2. **Market Regime Analysis:**  
   SPY's historical data is used to compute:
   - A 30-day rolling annualized volatility
   - 50-day and 200-day moving averages
   - 14-day Relative Strength Index (RSI)
   
   These metrics are then used to classify the market into regimes such as Expansion, Recession, Contraction, or Recovery.

3. **Dynamic Portfolio Construction:**  
   Based on the identified regime, the portfolio dynamically tilts its exposure among five factors:
   - MKT (Market premium)
   - SMB (Size premium)
   - HML (Value premium)
   - RMW (Profitability premium)
   - CMA (Investment premium)

4. **Monte Carlo Risk Analysis:**  
   VaR and CVaR are computed using Monte Carlo simulations with Student's t-distributions (better for fat tails)
   to more accurately capture market risks compared to simple historical quantiles.

5. **Comprehensive Stress Testing:**  
   The portfolio undergoes sophisticated stress testing that models not just return impacts, but also:
   - Volatility scaling (accounts for heteroskedasticity during stress periods)
   - Skewness adjustments (captures asymmetric return distributions during crises)
   - Tail behavior modifications (models extreme events better than normal distributions)

Multiple stress scenarios model different market environments like severe recessions, rate hikes, market crashes, and corrections.

.. toctree::
   :maxdepth: 2
   :caption: API Documentation

   modules

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`