"""
Insight Engine for generating actionable insights from data analysis.
"""

import pandas as pd
import numpy as np
from .advanced_analytics import AdvancedAnalytics


class InsightEngine:
    """Generate actionable insights from data and analysis results."""

    def generate(self, data, profile=None, kpis=None):
        """
        Generate comprehensive insights from data and analysis results.

        Parameters
        ----------
        data : pd.DataFrame
            Input data
        profile : dict, optional
            Data profile results
        kpis : dict, optional
            KPI calculation results

        Returns
        -------
        list
            List of insight dictionaries with actionable recommendations
        """
        insights = []

        # Basic insights from profile
        if profile:
            insights.extend(self._quality_insights(profile))
            insights.extend(self._distribution_insights(data))

        # KPI-based insights
        if kpis:
            insights.extend(self._kpi_insights(kpis))

        # Advanced AI-like insights
        try:
            advanced = AdvancedAnalytics(data)
            insights.extend(advanced.generate_insights_and_recommendations())
        except Exception as e:
            pass  # Continue with basic insights if advanced analytics fails

        return insights

    @staticmethod
    def _quality_insights(profile):
        """Generate insights about data quality."""
        insights = []
        quality = profile.get("quality_metrics", {})

        completeness = quality.get("completeness_pct", 100)
        if completeness < 90:
            severity = "critical" if completeness < 70 else "high"
            insights.append({
                "type": "warning",
                "title": "Data Completeness Issue",
                "message": f"Data completeness is {completeness:.1f}%. "
                          "Many missing values detected. This may affect analysis accuracy.",
                "severity": severity,
                "action": "Implement data imputation strategy or remove incomplete records"
            })
        elif completeness < 95:
            insights.append({
                "type": "info",
                "title": "Minor Data Quality Issue",
                "message": f"Data completeness is {completeness:.1f}%. "
                          "Some missing values present but manageable.",
                "severity": "low",
                "action": "Consider imputation for missing values"
            })

        duplicate_count = quality.get("duplicate_rows", 0)
        if duplicate_count > 0:
            duplicate_pct = (duplicate_count / quality.get("total_cells", 1)) * 100
            severity = "high" if duplicate_pct > 5 else "medium"
            insights.append({
                "type": "warning",
                "title": "Duplicate Records Detected",
                "message": f"Found {duplicate_count} duplicate rows ({duplicate_pct:.2f}%). "
                          "Duplicates can skew analysis results.",
                "severity": severity,
                "action": "Remove or merge duplicate records before final analysis"
            })

        return insights

    @staticmethod
    def _distribution_insights(data):
        """Generate insights about data distribution and statistical patterns."""
        insights = []
        numeric_cols = data.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            col_data = data[col].dropna()
            if len(col_data) == 0:
                continue

            skewness = col_data.skew()
            kurtosis = col_data.kurtosis()

            # Skewness analysis
            if abs(skewness) > 1.5:
                insights.append({
                    "type": "observation",
                    "title": f"Significant Skewness in '{col}'",
                    "message": f"Column '{col}' is highly {'right' if skewness > 0 else 'left'}-skewed "
                              f"(skewness: {skewness:.3f}). Data is not symmetrically distributed.",
                    "severity": "info",
                    "column": col,
                    "action": "Consider log transformation or other scaling techniques"
                })

            # Kurtosis analysis
            if kurtosis > 3:
                insights.append({
                    "type": "observation",
                    "title": f"High Concentration in '{col}'",
                    "message": f"Column '{col}' has high kurtosis ({kurtosis:.3f}). "
                              "Data is heavily concentrated with extreme values.",
                    "severity": "info",
                    "column": col,
                    "action": "Investigate extreme values and outliers"
                })

            # Check if data is relatively constant
            if col_data.std() < col_data.mean() * 0.05 and col_data.mean() != 0:
                insights.append({
                    "type": "observation",
                    "title": f"Low Variability in '{col}'",
                    "message": f"Column '{col}' has low variability (CV < 5%). "
                              "Values don't vary much, limiting predictive power.",
                    "severity": "low",
                    "column": col,
                    "action": "This column may not be useful for predictive modeling"
                })

        return insights

    @staticmethod
    def _kpi_insights(kpis):
        """Generate insights about KPI values and patterns."""
        insights = []

        # Analyze calculated KPIs
        numeric_kpis = {k: v for k, v in kpis.items() if isinstance(v, (int, float))}
        
        # Flag negative values in metrics that shouldn't be negative
        for kpi_name, kpi_value in numeric_kpis.items():
            if kpi_value < 0 and not any(x in kpi_name.lower() for x in ['negative', 'loss', 'deficit', 'debt']):
                insights.append({
                    "type": "warning",
                    "title": f"Unexpected Negative Value",
                    "message": f"KPI '{kpi_name}' has a negative value: {kpi_value:.4f}. "
                              "This may indicate a calculation issue or data problem.",
                    "severity": "medium",
                    "kpi": kpi_name,
                    "value": kpi_value,
                    "action": "Verify calculation and data validity"
                })

        # High variation flag
        cv_metrics = {k: v for k, v in kpis.items() if '_cv' in k}  # Coefficient of variation
        for kpi_name, cv_value in cv_metrics.items():
            if cv_value > 100:
                insights.append({
                    "type": "observation",
                    "title": f"High Variability in {kpi_name}",
                    "message": f"Coefficient of variation for {kpi_name} is {cv_value:.2f}%. "
                              "This indicates high inconsistency in the underlying data.",
                    "severity": "info",
                    "action": "Investigate sources of variation and consider stratification"
                })

        return insights

