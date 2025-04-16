# Dynamic Factor-Tilted Portfolio with Advanced Risk Analytics

This project builds a dynamic factor-tilted portfolio that adjusts its exposures based on the prevailing macroeconomic environment, using advanced risk modeling and interactive visualizations. Rather than simulating or sourcing factor returns via yfinance, we download the historical Fama–French 5 Factor data directly from Kenneth French's website.

## Project Features

### Factor Modeling
Uses the free historical "F-F Research Data 5 Factors 2x3 Daily" dataset from Kenneth French's website. The factors computed are:
- **MKT:** Market risk premium  
- **SMB:** Size premium  
- **HML:** Value premium  
- **RMW:** Profitability premium  
- **CMA:** Investment premium

### Market Regime Analysis
- **Volatility Analysis:** Tracks SPY's rolling 30-day annualized volatility
- **Trend Detection:** Evaluates 50-day vs. 200-day moving averages
- **Momentum Indicator:** Incorporates 14-day RSI (Relative Strength Index)
- **Regime Classification:** Determines whether the market is in Expansion, Recession, Contraction, or Recovery phase

### Dynamic Portfolio Construction
- Adjusts factor exposure weights based on the determined market regime
- Implements strategic factor tilts tailored to different market environments
- Rebalances automatically with updated market regime detection

### Advanced Risk Analysis
- **Monte Carlo Simulations:** Calculates VaR and CVaR using Student's t-distributions for better tail modeling
- **Multiple Distribution Options:** Supports normal, Student's t, empirical bootstrap, and skewed normal distributions
- **Comprehensive Metrics:** Computes volatility, Sharpe ratio, VaR, CVaR, maximum drawdown, skewness, and kurtosis

### Sophisticated Stress Testing
- Models complex scenario impacts across multiple statistical moments:
  - **Mean Adjustments:** Both multiplicative and additive return shocks
  - **Volatility Scaling:** Captures heteroskedasticity during stress periods
  - **Skewness Modifications:** Models asymmetric return distributions typical in crises
  - **Tail Behavior Adjustments:** Enhances modeling of extreme events (kurtosis)
- Includes scenarios such as:
  - Severe Recession
  - Rapid Rate Hike
  - Market Crash
  - Mild Correction
  - Stagflation

### Interactive Visualizations
- **Plotly Integration:** All charts feature interactive elements like hover information and zooming
- **Portfolio Performance:** Cumulative returns with moving averages and range selectors
- **Risk Profile Radar:** Multi-dimensional comparison of risk metrics across scenarios
- **Factor Correlation Heatmap:** Visual representation of factor relationships
- **Metric Comparisons:** Interactive bar charts for all risk metrics

### Automated Documentation
- Generates a comprehensive GitHub Pages site using Sphinx
- Includes both static images and interactive Plotly visualizations
- Detailed methodological explanations and API documentation

### Continuous Integration
- Uses GitHub Actions to schedule weekly (Sunday midnight UTC) runs
- Automatically updates documentation with fresh analysis
- Supports manual triggering via workflow_dispatch

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/abencarrington/Factor-Portfolio-Stress-Testing
   cd Factor-Portfolio-Stress-Testing
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the analysis:**
   ```bash
   python src/main.py
   ```

4. **Build the Documentation:**
   ```bash
   cd docs
   make html
   ```

The generated HTML files will be in `docs/_build/html/`.

## Project Workflow

A GitHub Actions workflow is set up (see `.github/workflows/schedule.yml`) to automatically run the analysis on a weekly schedule and update the GitHub Pages site with the latest results.

## Project Structure

1. **src/**: Contains the source code for:
   - `factors.py`: Factor data acquisition and processing
   - `macro.py`: Market regime classification and stress scenario definitions
   - `portfolio.py`: Portfolio construction and advanced risk analytics
   - `main.py`: Orchestration and visualization generation

2. **docs/**: Contains the Sphinx documentation files:
   - `index.rst`: Main documentation page
   - `conf.py`: Sphinx configuration
   - `_static/`: Generated visualizations and custom CSS

3. **.github/workflows/**: Contains the GitHub Actions workflow file for scheduled runs

4. **requirements.txt**: Lists all the required Python libraries

## Requirements

- Python 3.8+
- Libraries: pandas, numpy, plotly, scipy, statsmodels, sphinx, tqdm, yfinance, beautifulsoup4, requests

## License

This project is licensed under the MIT License.
