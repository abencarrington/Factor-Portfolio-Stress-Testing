# Dynamic Factor-Tilted Portfolio with Macro Stress Testing

This project builds a dynamic factor-tilted portfolio that adjusts its exposures based on the prevailing macroeconomic environment. Rather than simulating or sourcing factor returns via yfinance, we download the historical Fama–French 5 Factor data directly from Kenneth French’s website.

## Project Features

- **Factor Modeling:**  
  Uses the free historical “F-F Research Data 5 Factors 2x3 Daily” dataset from Kenneth French’s website. The factors computed are:
  - **MKT:** Market risk premium  
  - **SMB:** Size premium  
  - **HML:** Value premium  
  - **RMW:** Profitability premium  
  - **CMA:** Investment premium

- **Market Regime Analysis:**  
  Analyzes SPY’s rolling volatility and moving averages (50-day vs. 200-day) to determine whether the market is in Expansion, Recession, Contraction, or Recovery.

- **Dynamic Portfolio Construction:**  
  Adjusts portfolio weights based on the determined regime.

- **Comprehensive Risk Analysis:**  
  Computes advanced metrics including volatility, Sharpe ratio, Value at Risk (VaR), Conditional VaR (CVaR), maximum drawdown, skewness, and kurtosis.

- **Stress Testing:**  
  Evaluates portfolio performance under various hypothetical macroeconomic stress scenarios.

- **Automated Documentation:**  
  Generates a GitHub Pages site (using Sphinx) with all necessary plots and explanation.

- **Automation:**  
  Uses GitHub Actions to schedule weekly (Sunday midnight UTC) runs and update the documentation.

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/abencarrington/Factor-Portfolio-Stress-Testing
   cd Factor-Portfolio-Stress-Testing

2.	**Install dependencies:**
    ```bash
    pip install -r requirements.txt

3. **Run the analysis:**
    ```bash
    python src/main.py

4. **Build the Documentation:**
    ```bash
    cd docs
    make html

The generated HTML files will be in docs/_build/html/.

## Project Workflow

A GitHub Actions workflow is set up (see .github/workflows/schedule.yml) to automatically run the analysis on a weekly schedule and update the GitHub Pages site with the latest results.

## Project Structure

1.	src/: Contains the source code for factor computation, macro environment classification, portfolio construction, and risk analysis.
2.	docs/: Contains the Sphinx documentation files that form the GitHub Pages site.
3.	.github/workflows/: Contains the GitHub Actions workflow file for scheduled runs.
4.	requirements.txt: Lists all the required Python libraries.

## License

This project is licensed under the MIT License.
