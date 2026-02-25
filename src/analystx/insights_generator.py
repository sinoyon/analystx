"""
Enhanced insights generator for business-focused analysis.
Generates actionable insights and problem-solving recommendations.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any


class InsightsAnalyzer:
    """Generate business-focused, problem-solving insights from data."""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize the insights analyzer."""
        self.df = df
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        self.date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate comprehensive analysis summary."""
        return {
            'data_quality': self._analyze_data_quality(),
            'key_metrics': self._extract_key_metrics(),
            'patterns': self._identify_patterns(),
            'issues': self._identify_issues(),
            'recommendations': self._generate_recommendations(),
        }
    
    def _analyze_data_quality(self) -> Dict[str, Any]:
        """Analyze data quality issues."""
        total_rows = len(self.df)
        total_cols = len(self.df.columns)
        
        return {
            'total_records': total_rows,
            'total_fields': total_cols,
            'missing_data': self._check_missing_values(),
            'data_types': self.df.dtypes.astype(str).to_dict(),
            'completeness': round((1 - self.df.isnull().sum().sum() / (total_rows * total_cols)) * 100, 2),
        }
    
    def _check_missing_values(self) -> Dict[str, int]:
        """Check for missing values."""
        missing = {}
        for col in self.df.columns:
            missing_count = self.df[col].isnull().sum()
            if missing_count > 0:
                missing[col] = int(missing_count)
        return missing if missing else {'status': 'No missing values'}
    
    def _extract_key_metrics(self) -> Dict[str, Any]:
        """Extract key metrics from the data."""
        metrics = {
            'numeric_summary': {},
            'categorical_summary': {},
        }
        
        # Numeric metrics
        for col in self.numeric_cols:
            metrics['numeric_summary'][col] = {
                'count': int(self.df[col].count()),
                'mean': round(self.df[col].mean(), 2),
                'median': round(self.df[col].median(), 2),
                'std': round(self.df[col].std(), 2),
                'min': round(self.df[col].min(), 2),
                'max': round(self.df[col].max(), 2),
            }
        
        # Categorical metrics
        for col in self.categorical_cols:
            metrics['categorical_summary'][col] = {
                'unique_values': int(self.df[col].nunique()),
                'most_common': self.df[col].value_counts().head(3).to_dict(),
                'distribution': self.df[col].value_counts().to_dict(),
            }
        
        return metrics
    
    def _identify_patterns(self) -> List[str]:
        """Identify important patterns in the data."""
        patterns = []
        
        # User/Status patterns
        for col in self.categorical_cols:
            if self.df[col].nunique() < 10:
                value_counts = self.df[col].value_counts()
                for val, count in value_counts.head(2).items():
                    percentage = round((count / len(self.df)) * 100, 1)
                    patterns.append(f"{percentage}% of records have {col}='{val}'")
        
        # Numeric patterns
        for col in self.numeric_cols:
            if col in self.numeric_cols:
                outliers = len(self.df[
                    (self.df[col] < self.df[col].quantile(0.25) - 1.5 * (self.df[col].quantile(0.75) - self.df[col].quantile(0.25))) |
                    (self.df[col] > self.df[col].quantile(0.75) + 1.5 * (self.df[col].quantile(0.75) - self.df[col].quantile(0.25)))
                ])
                if outliers > 0:
                    outlier_pct = round((outliers / len(self.df)) * 100, 1)
                    patterns.append(f"{outlier_pct}% outliers detected in {col}")
        
        return patterns if patterns else ["No significant patterns detected"]
    
    def _identify_issues(self) -> List[str]:
        """Identify data quality and business issues."""
        issues = []
        
        # Data quality issues
        missing_data = self._check_missing_values()
        if missing_data.get('status') != 'No missing values':
            for col, count in missing_data.items():
                pct = round((count / len(self.df)) * 100, 1)
                if pct > 5:
                    issues.append(f"⚠️ High missing values in {col}: {pct}%")
        
        # Imbalanced categorical distributions
        for col in self.categorical_cols:
            value_counts = self.df[col].value_counts()
            if len(value_counts) > 1:
                max_pct = (value_counts.iloc[0] / len(self.df)) * 100
                if max_pct > 80:
                    issues.append(f"⚠️ Imbalanced distribution in {col}: {round(max_pct, 1)}% dominated by '{value_counts.index[0]}'")
        
        return issues if issues else ["✓ No critical issues detected"]
    
    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        # Based on data quality
        if self._check_missing_values().get('status') != 'No missing values':
            recommendations.append("🔧 Impute or remove missing values to improve data completeness")
        
        # Based on patterns
        for col in self.categorical_cols:
            if col.lower() in ['status', 'subscription_status', 'state', 'category']:
                value_counts = self.df[col].value_counts()
                if 'inactive' in value_counts.index or 'canceled' in value_counts.index:
                    recommendations.append(f"📊 Analyze {col} distribution - consider retention strategies")
        
        # Based on numeric data
        if len(self.numeric_cols) > 0:
            recommendations.append("📈 Monitor numeric metrics for trends and anomalies")
        
        recommendations.append("✅ Enable automated monitoring and alerts for data drift")
        
        return recommendations


def create_analysis_report(df: pd.DataFrame, business_context: str = None) -> Dict[str, Any]:
    """
    Create a comprehensive business analysis report.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input data to analyze
    business_context : str, optional
        Business context for the analysis
        
    Returns
    -------
    dict
        Comprehensive analysis report with insights
    """
    analyzer = InsightsAnalyzer(df)
    
    report = {
        'title': f'Data Analysis Report',
        'context': business_context or 'General Data Analysis',
        'generated_at': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
        'data_shape': {'rows': len(df), 'columns': len(df.columns)},
        'summary': analyzer.generate_summary(),
    }
    
    return report


def format_report_as_html(report: Dict[str, Any]) -> str:
    """Format analysis report as HTML."""
    html_parts = [
        '<html>',
        '<head>',
        '<style>',
        '''
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .header { background-color: #2c3e50; color: white; padding: 20px; border-radius: 5px; }
        .section { background-color: white; margin: 20px 0; padding: 15px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .section h2 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        .metric { display: inline-block; background-color: #ecf0f1; padding: 15px; margin: 10px; border-radius: 5px; min-width: 150px; }
        .metric-value { font-size: 24px; font-weight: bold; color: #3498db; }
        .metric-label { font-size: 12px; color: #7f8c8d; }
        .issue { background-color: #ffebee; padding: 10px; margin: 5px 0; border-left: 4px solid #e74c3c; border-radius: 3px; }
        .recommendation { background-color: #e8f5e9; padding: 10px; margin: 5px 0; border-left: 4px solid #27ae60; border-radius: 3px; }
        .pattern { background-color: #e3f2fd; padding: 10px; margin: 5px 0; border-left: 4px solid #2196f3; border-radius: 3px; }
        table { width: 100%; border-collapse: collapse; margin: 10px 0; }
        table th { background-color: #34495e; color: white; padding: 10px; text-align: left; }
        table td { padding: 8px; border-bottom: 1px solid #ddd; }
        table tr:hover { background-color: #f5f5f5; }
        ''',
        '</style>',
        '</head>',
        '<body>',
        '<div class="header">',
        f'<h1>📊 {report["title"]}</h1>',
        f'<p><strong>Context:</strong> {report["context"]}</p>',
        f'<p><strong>Generated:</strong> {report["generated_at"]}</p>',
        '</div>',
    ]
    
    # Data Overview
    html_parts.extend([
        '<div class="section">',
        '<h2>📋 Data Overview</h2>',
        f'<div class="metric"><div class="metric-value">{report["data_shape"]["rows"]}</div><div class="metric-label">Total Records</div></div>',
        f'<div class="metric"><div class="metric-value">{report["data_shape"]["columns"]}</div><div class="metric-label">Fields</div></div>',
        f'<div class="metric"><div class="metric-value">{report["summary"]["data_quality"]["completeness"]}%</div><div class="metric-label">Data Completeness</div></div>',
        '</div>',
    ])
    
    # Key Metrics
    summary = report['summary']
    
    html_parts.append('<div class="section">')
    html_parts.append('<h2>📈 Key Metrics</h2>')
    
    if summary['key_metrics']['numeric_summary']:
        html_parts.append('<h3>Numeric Metrics</h3>')
        html_parts.append('<table>')
        html_parts.append('<tr><th>Field</th><th>Mean</th><th>Median</th><th>Min</th><th>Max</th></tr>')
        for col, metrics in summary['key_metrics']['numeric_summary'].items():
            html_parts.append(f'<tr><td>{col}</td><td>{metrics["mean"]}</td><td>{metrics["median"]}</td><td>{metrics["min"]}</td><td>{metrics["max"]}</td></tr>')
        html_parts.append('</table>')
    
    html_parts.append('</div>')
    
    # Patterns
    html_parts.extend([
        '<div class="section">',
        '<h2>🔍 Identified Patterns</h2>',
    ])
    for pattern in summary['patterns']:
        html_parts.append(f'<div class="pattern">{pattern}</div>')
    html_parts.append('</div>')
    
    # Issues
    html_parts.extend([
        '<div class="section">',
        '<h2>⚠️ Issues & Concerns</h2>',
    ])
    for issue in summary['issues']:
        html_parts.append(f'<div class="issue">{issue}</div>')
    html_parts.append('</div>')
    
    # Recommendations
    html_parts.extend([
        '<div class="section">',
        '<h2>💡 Recommendations</h2>',
    ])
    for rec in summary['recommendations']:
        html_parts.append(f'<div class="recommendation">{rec}</div>')
    html_parts.append('</div>')
    
    html_parts.extend([
        '</body>',
        '</html>',
    ])
    
    return '\n'.join(html_parts)
