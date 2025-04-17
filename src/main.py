import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from factors import download_fama_french_5_factors
from macro import analyze_market_regime, define_stress_scenarios
from portfolio import construct_portfolio, calculate_risk_metrics, stress_test_portfolio

def generate_plotly_metric_plots(baseline_metrics, stressed_results, output_dir):
    """
    Generate interactive Plotly visualizations for each risk metric.
    
    Args:
        baseline_metrics (dict): Risk metrics for the baseline portfolio.
        stressed_results (dict): Dictionary with scenario metrics.
        output_dir (str): Directory to save the HTML files.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all metrics (excluding historical VaR/CVaR to avoid redundancy)
    metric_names = [key for key in baseline_metrics.keys() 
                   if not key.startswith('Historical')]
    
    # Color scheme
    colors = px.colors.qualitative.Plotly
    
    # Create a plot for each metric
    for i, metric in enumerate(metric_names):
        scenarios = ["Baseline"] + list(stressed_results.keys())
        values = [baseline_metrics[metric]]
        
        for scenario in stressed_results:
            values.append(stressed_results[scenario][metric])
        
        # Create a bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=scenarios,
            y=values,
            text=[f"{x:.4f}" for x in values],
            textposition='auto',
            marker_color=[colors[0]] + [colors[i % len(colors) + 1] for i in range(len(scenarios)-1)],
            hovertemplate='%{x}: %{y:.4f}<extra></extra>'
        ))
        
        # Customize layout
        fig.update_layout(
            title=f"{metric}",
            xaxis_title="Scenario",
            yaxis_title="Value",
            template="plotly_white",
            height=500,
            width=800,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        # Add horizontal grid lines
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
        
        # Save as interactive HTML
        filename = f"{metric.replace(' ', '_').lower()}.html"
        output_path = os.path.join(output_dir, filename)
        fig.write_html(output_path)
        
        # Save as static PNG for documentation
        png_path = os.path.join(output_dir, f"{metric.replace(' ', '_').lower()}.png")
        fig.write_image(png_path)
        
        print(f"Saved plots for {metric} at {output_path} and {png_path}")

def generate_portfolio_performance_plot(portfolio_returns, output_dir):
    """
    Generate an interactive Plotly plot of portfolio cumulative returns with moving averages.
    
    Args:
        portfolio_returns (Series): Portfolio returns series.
        output_dir (str): Directory to save the plot.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Calculate cumulative returns and moving averages
    cum_returns = (1 + portfolio_returns).cumprod()
    ma50 = cum_returns.rolling(window=50).mean()
    ma200 = cum_returns.rolling(window=200).mean()
    
    # Create Plotly figure
    fig = go.Figure()
    
    # Add traces
    fig.add_trace(go.Scatter(
        x=portfolio_returns.index,
        y=cum_returns,
        mode='lines',
        name='Portfolio Cumulative Return',
        line=dict(color='rgb(49,130,189)', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=portfolio_returns.index,
        y=ma50,
        mode='lines',
        name='50-Day MA',
        line=dict(color='rgba(255,0,0,0.7)', width=1.5, dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=portfolio_returns.index,
        y=ma200,
        mode='lines',
        name='200-Day MA',
        line=dict(color='rgba(0,128,0,0.7)', width=1.5, dash='dash')
    ))
    
    # Customize layout
    fig.update_layout(
        title='Dynamic Factor-Tilted Portfolio Cumulative Returns',
        xaxis_title='Date',
        yaxis_title='Cumulative Return',
        template='plotly_white',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=600,
        width=1000
    )
    
    # Add range slider
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    
    # Save as interactive HTML
    output_path = os.path.join(output_dir, "portfolio_returns.html")
    fig.write_html(output_path)
    
    # Save as static PNG for documentation
    png_path = os.path.join(output_dir, "portfolio_returns.png")
    fig.write_image(png_path)
    
    print(f"Portfolio returns plot saved to {output_path} and {png_path}")

def generate_correlation_heatmap(factors, output_dir):
    """
    Generate a correlation heatmap of the five factors.
    
    Args:
        factors (DataFrame): The factor returns dataframe.
        output_dir (str): Directory to save the plot.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Calculate correlation matrix
    corr_matrix = factors.corr()
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu_r',
        zmid=0,
        text=np.around(corr_matrix.values, decimals=3),
        texttemplate='%{text:.3f}',
        hovertemplate='%{y} vs %{x}: %{z:.3f}<extra></extra>'
    ))
    
    # Update layout
    fig.update_layout(
        title='Factor Correlation Matrix',
        width=700,
        height=600,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    # Save as interactive HTML
    output_path = os.path.join(output_dir, "factor_correlation.html")
    fig.write_html(output_path)
    
    # Save as static PNG for documentation
    png_path = os.path.join(output_dir, "factor_correlation.png")
    fig.write_image(png_path)
    
    print(f"Factor correlation heatmap saved to {output_path} and {png_path}")

def generate_risk_comparison_radar(baseline_metrics, stressed_results, output_dir):
    """
    Generate a radar chart comparing risk metrics across scenarios.
    
    Args:
        baseline_metrics (dict): Risk metrics for the baseline portfolio.
        stressed_results (dict): Dictionary with scenario metrics.
        output_dir (str): Directory to save the plot.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Select metrics to include in radar (normalized) with shorter display names
    radar_metrics_display = {
        'Annualized Volatility': 'Volatility', 
        'VaR (95%)': 'VaR', 
        'CVaR (95%)': 'CVaR', 
        'Maximum Drawdown': 'Max DD',
        'Skewness': 'Skew',
        'Kurtosis': 'Kurtosis'
    }
    
    radar_metrics = list(radar_metrics_display.keys())
    radar_display_names = list(radar_metrics_display.values())
    
    # Prepare data for radar chart
    scenarios = ["Baseline"] + list(stressed_results.keys())
    
    # Create a dictionary to store min and max values for each metric
    min_max = {}
    for metric in radar_metrics:
        values = [baseline_metrics[metric]]
        for scenario in stressed_results:
            values.append(stressed_results[scenario][metric])
        
        # Special handling for skewness which can be negative
        if metric == 'Skewness':
            abs_max = max(abs(min(values)), abs(max(values)))
            min_max[metric] = (-abs_max, abs_max)
        else:
            min_max[metric] = (min(values), max(values))
    
    # Normalize values to 0-1 range for radar chart
    normalized_data = []
    for scenario in scenarios:
        if scenario == "Baseline":
            scenario_data = baseline_metrics
        else:
            scenario_data = stressed_results[scenario]
        
        normalized_values = []
        for metric in radar_metrics:
            min_val, max_val = min_max[metric]
            if max_val == min_val:  # Avoid division by zero
                normalized_values.append(0.5)
            else:
                normalized_val = (scenario_data[metric] - min_val) / (max_val - min_val)
                normalized_values.append(normalized_val)
        
        normalized_data.append(normalized_values)
    
    # Create radar chart
    fig = go.Figure()
    
    for i, scenario in enumerate(scenarios):
        fig.add_trace(go.Scatterpolar(
            r=normalized_data[i],
            theta=radar_display_names,  # Use shorter display names
            fill='toself',
            name=scenario,
            hovertemplate='%{theta}: %{r:.4f}<extra>' + scenario + '</extra>'
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            ),
            angularaxis=dict(
                tickfont=dict(size=14)  # Increase font size for better readability
            )
        ),
        title="Risk Profile Comparison",
        showlegend=True,
        width=800,
        height=800,
        margin=dict(t=100, b=100, l=80, r=80)  # Increased margins to prevent cutoff
    )
    
    # Save as interactive HTML
    output_path = os.path.join(output_dir, "risk_radar.html")
    fig.write_html(output_path)
    
    # Save as static PNG for documentation
    png_path = os.path.join(output_dir, "risk_radar.png")
    fig.write_image(png_path)
    
    print(f"Risk radar chart saved to {output_path} and {png_path}")

def main():
    """Main analysis workflow."""
    print("Starting analysis...")
    
    # Download factor data (from Kenneth French's website)
    print("Downloading Fama-French 5 factor data...")
    factors = download_fama_french_5_factors(start_date='2010-01-01')
    
    # Analyze the current market regime using SPY data
    print("Analyzing market regime...")
    regime = analyze_market_regime()
    print("Market Regime:", regime)
    
    # Build the dynamic portfolio based on the regime
    print("Constructing portfolio...")
    portfolio_returns = construct_portfolio(factors, regime)
    
    # Calculate baseline risk metrics using Monte Carlo VaR/CVaR
    print("Calculating baseline risk metrics with Monte Carlo simulations...")
    baseline_metrics = calculate_risk_metrics(portfolio_returns, risk_free_rate=0.015, mc_method='t')
    print("Baseline Risk Metrics:", baseline_metrics)
    
    # Define stress scenarios and compute risk metrics for each
    print("Running stress tests with enhanced scenario modeling...")
    scenarios = define_stress_scenarios()
    stressed_results = stress_test_portfolio(portfolio_returns, scenarios, mc_method='t')
    print("Stress Test Results:", stressed_results)
    
    # Create output directory
    output_dir = os.path.join("docs", "_static")
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate all the interactive Plotly visualizations
    print("Generating interactive visualizations...")
    generate_portfolio_performance_plot(portfolio_returns, output_dir)
    generate_plotly_metric_plots(baseline_metrics, stressed_results, output_dir)
    generate_correlation_heatmap(factors, output_dir)
    generate_risk_comparison_radar(baseline_metrics, stressed_results, output_dir)
    
    # Write environment info to a text file with pretty formatting
    with open(os.path.join("docs", "environment_info.txt"), "w") as f:
        f.write("Market Regime:\n")
        f.write(f"  Regime: {regime['regime']}\n")
        f.write(f"  Description: {regime['description']}\n")
        f.write(f"  Volatility: {regime['volatility']:.4f}\n")
        f.write(f"  Trend: {regime['trend']}\n\n")
        
        f.write("Baseline Risk Metrics:\n")
        for metric, value in baseline_metrics.items():
            f.write(f"  {metric}: {value:.4f}\n")
        f.write("\n")
        
        f.write("Stress Test Results:\n")
        for scenario, metrics in stressed_results.items():
            f.write(f"  {scenario}:\n")
            for metric, value in metrics.items():
                f.write(f"    {metric}: {value:.4f}\n")
            f.write("\n")
    
    print("Analysis completed successfully!")

if __name__ == "__main__":
    main()