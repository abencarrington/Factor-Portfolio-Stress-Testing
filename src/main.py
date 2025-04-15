import os
import matplotlib.pyplot as plt

from factors import download_fama_french_5_factors
from macro import analyze_market_regime, define_stress_scenarios
from portfolio import construct_portfolio, calculate_risk_metrics, stress_test_portfolio

def generate_individual_metric_plots(baseline_metrics, stressed_results):
    """
    Generate an individual plot (bar chart) for each risk metric.
    
    For each risk metric, the plot shows the baseline value alongside the stressed scenario values.
    Each plot is saved as a separate PNG file in the docs/_static directory.
    
    Args:
        baseline_metrics (dict): Risk metrics for the baseline (current regime).
        stressed_results (dict): Dictionary with scenario names as keys and corresponding risk metrics as values.
    """
    output_dir = os.path.join("docs", "_static")
    os.makedirs(output_dir, exist_ok=True)
    
    # List all risk metric names
    metric_names = list(baseline_metrics.keys())
    
    # For each metric, create a bar plot.
    for metric in metric_names:
        # Prepare scenario labels and values.
        scenarios = ["Baseline"] + list(stressed_results.keys())
        values = [baseline_metrics[metric]]
        for scenario in stressed_results:
            values.append(stressed_results[scenario][metric])
        
        plt.figure(figsize=(8, 4))
        plt.bar(scenarios, values, color="steelblue")
        plt.title(metric, fontsize=12)
        plt.xlabel("Scenario", fontsize=10)
        plt.ylabel("Value", fontsize=10)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        filename = f"{metric.replace(' ', '_').lower()}.png"
        output_path = os.path.join(output_dir, filename)
        plt.savefig(output_path)
        plt.close()
        print(f"Saved plot for {metric} at {output_path}")

# Example usage inside main():
def main():
    # Download factor data (from Kenneth French's website)
    factors = download_fama_french_5_factors()
    dates = factors.index

    # Analyze the current market regime using SPY data.
    regime = analyze_market_regime()
    print("Market Regime:", regime)

    # Build the dynamic portfolio based on the regime.
    portfolio_returns = construct_portfolio(factors, regime)

    # Calculate baseline risk metrics.
    baseline_metrics = calculate_risk_metrics(portfolio_returns)
    print("Baseline Risk Metrics:", baseline_metrics)

    # Define stress scenarios and compute risk metrics for each scenario.
    scenarios = define_stress_scenarios()
    stressed_results = stress_test_portfolio(portfolio_returns, scenarios)
    print("Stress Test Results:", stressed_results)

    # Generate cumulative returns plot (unchanged)
    cum_returns = (1 + portfolio_returns).cumprod()
    output_dir = os.path.join("docs", "_static")
    os.makedirs(output_dir, exist_ok=True)
    portfolio_plot_path = os.path.join(output_dir, "portfolio_returns.png")
    plt.figure(figsize=(10, 6))
    plt.plot(dates, cum_returns, label="Portfolio Cumulative Return")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.title("Dynamic Portfolio Cumulative Returns")
    plt.legend()
    plt.tight_layout()
    plt.savefig(portfolio_plot_path)
    plt.close()
    print(f"Portfolio returns plot saved to {portfolio_plot_path}")

    # Generate individual plots for each risk metric.
    generate_individual_metric_plots(baseline_metrics, stressed_results)

    # Write environment info to a text file.
    with open(os.path.join("docs", "environment_info.txt"), "w") as f:
        f.write("Market Regime:\n")
        f.write(str(regime) + "\n\n")
        f.write("Baseline Risk Metrics:\n")
        f.write(str(baseline_metrics) + "\n\n")
        f.write("Stress Test Results:\n")
        f.write(str(stressed_results) + "\n")

if __name__ == "__main__":
    main()