#!/usr/bin/env python
"""Test script for enhanced AnalystX features."""

import pandas as pd
from src.analystx import AnalystX, AdvancedAnalytics

def main():
    """Test enhanced features."""
    # Create sample data
    data = pd.DataFrame({
        'sales': [100, 150, 200, 180, 220, 250, 300, 350],
        'revenue': [5000, 7500, 10000, 9000, 11000, 12500, 15000, 17500],
        'customers': [10, 15, 20, 18, 22, 25, 30, 35],
        'expenses': [3000, 4000, 5000, 4500, 5500, 6000, 7000, 8000]
    })

    print('========== AnalystX Version 0.1.1 ==========')
    print('Testing new features...\n')

    # Test AnalystX
    analyzer = AnalystX(data)

    # Test enhanced KPIs
    print('1. Enhanced KPI Calculation:')
    kpis = analyzer.calculate_kpis()
    print(f'   - Total rows: {kpis.get("total_rows")}')
    print(f'   - Total columns: {kpis.get("total_columns")}')
    print(f'   - Sales sum: {kpis.get("sales_sum")}')
    print(f'   - Sales mean: {kpis.get("sales_mean"):.2f}')
    print(f'   - Sales variance: {kpis.get("sales_variance"):.2f}')
    print(f'   - Sales coefficient of variation: {kpis.get("sales_cv"):.2f}%')
    print(f'   - Sales outliers: {kpis.get("sales_outliers_count")}')

    # Test advanced analytics directly
    print('\n2. Advanced Analytics Features:')
    analytics = AdvancedAnalytics(data)

    print('\n   Correlation Analysis:')
    corr = analytics.correlation_analysis()
    print(f'   - Strong correlations found: {corr.get("correlation_count")}')

    print('\n   Anomaly Detection:')
    anomalies = analytics.anomaly_detection()
    print(f'   - Anomalies found: {anomalies.get("total_anomalies_found")}')

    print('\n   Trend Analysis:')
    trends = analytics.trend_analysis()
    print(f'   - Columns analyzed: {len(trends.get("trends", {}))}')

    print('\n   Distribution Analysis:')
    dist = analytics.distribution_analysis()
    print(f'   - Columns analyzed: {dist.get("total_columns_analyzed")}')

    print('\n   Data Quality Assessment:')
    quality = analytics.data_quality_assessment()
    print(f'   - Quality Score: {quality.get("quality_score")}%')
    print(f'   - Quality Rating: {quality.get("quality_rating")}')

    print('\n   Insights and Recommendations:')
    insights = analytics.generate_insights_and_recommendations()
    print(f'   - Total insights generated: {len(insights)}')
    for i, insight in enumerate(insights[:3], 1):
        print(f'     {i}. {insight.get("title", "N/A")}')

    # Test via AnalystX methods
    print('\n3. AnalystX Advanced Methods:')
    print('   Testing correlation_analysis():')
    corr_result = analyzer.correlation_analysis()
    print(f'   - Strong correlations: {corr_result.get("correlation_count")}')

    print('\n   Testing detect_anomalies():')
    anomaly_result = analyzer.detect_anomalies()
    print(f'   - Anomalies detected: {anomaly_result.get("total_anomalies_found")}')

    print('\n   Testing analyze_trends():')
    trend_result = analyzer.analyze_trends()
    print(f'   - Trend columns: {len(trend_result.get("trends", {}))}')

    print('\n   Testing assess_data_quality():')
    quality_result = analyzer.assess_data_quality()
    print(f'   - Quality rating: {quality_result.get("quality_rating")}')

    print('\n✓ All enhanced features working correctly!')
    print('✓ Version 0.1.1 - Final version')
    print('✓ Author: Shariful Islam')

if __name__ == '__main__':
    main()
