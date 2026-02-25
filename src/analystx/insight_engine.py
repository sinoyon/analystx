"""
Insight Engine for generating actionable insights from data analysis.
"""

import pandas as pd
import numpy as np


class InsightEngine:
    """Generate actionable insights from data and analysis results."""

    def generate(self, data, profile=None, kpis=None):
        """
        Generate insights from data and analysis results.

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
            List of insight dictionaries
        """
        insights = []

        if profile:
            insights.extend(self._quality_insights(profile))
            insights.extend(self._distribution_insights(data))

        if kpis:
            insights.extend(self._kpi_insights(kpis))

        return insights

    @staticmethod
    def _quality_insights(profile):
        """Generate insights about data quality."""
        insights = []
        quality = profile.get("quality_metrics", {})

        if quality.get("completeness_pct", 100) < 90:
            insights.append({
                "type": "warning",
                "message": f"Data completeness is {quality.get('completeness_pct', 0)}%. "
                          "Consider addressing missing values.",
                "severity": "high"
            })

        if quality.get("duplicate_rows", 0) > 0:
            insights.append({
                "type": "warning",
                "message": f"Found {quality.get('duplicate_rows', 0)} duplicate rows.",
                "severity": "medium"
            })

        return insights

    @staticmethod
    def _distribution_insights(data):
        """Generate insights about data distribution."""
        insights = []
        numeric_cols = data.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            skewness = data[col].skew()
            if abs(skewness) > 1:
                insights.append({
                    "type": "observation",
                    "message": f"Column '{col}' has significant skewness ({skewness:.2f}).",
                    "column": col
                })

        return insights

    @staticmethod
    def _kpi_insights(kpis):
        """Generate insights about KPI values."""
        insights = []

        # Example: Flag anomalies or trends
        for kpi_name, kpi_value in kpis.items():
            if isinstance(kpi_value, (int, float)):
                if kpi_value < 0:
                    insights.append({
                        "type": "observation",
                        "message": f"KPI '{kpi_name}' has a negative value: {kpi_value}",
                        "kpi": kpi_name,
                        "value": kpi_value
                    })

        return insights
