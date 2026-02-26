"""
Advanced Analytics Module - AI-powered data analysis and problem solving.

Provides sophisticated analysis including correlation, anomaly detection,
trend analysis, and intelligent recommendations for data-driven decision making.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any


class AdvancedAnalytics:
    """Advanced analytics engine for comprehensive data insights and problem solving."""

    def __init__(self, data: pd.DataFrame):
        """
        Initialize advanced analytics.

        Parameters
        ----------
        data : pd.DataFrame
            Input data for advanced analysis
        """
        self.data = data
        self.numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = data.select_dtypes(include=['object']).columns.tolist()

    def correlation_analysis(self) -> Dict[str, Any]:
        """
        Perform comprehensive correlation analysis.

        Returns
        -------
        dict
            Dictionary containing correlation matrix and key relationships
        """
        if len(self.numeric_cols) < 2:
            return {"message": "Insufficient numeric columns for correlation analysis"}

        corr_matrix = self.data[self.numeric_cols].corr()
        
        # Find strong correlations (>0.7 or <-0.7)
        strong_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:
                    strong_correlations.append({
                        "variable1": corr_matrix.columns[i],
                        "variable2": corr_matrix.columns[j],
                        "correlation": round(corr_value, 4),
                        "strength": "Strong positive" if corr_value > 0 else "Strong negative"
                    })

        return {
            "correlation_matrix": corr_matrix.to_dict(),
            "strong_correlations": strong_correlations,
            "correlation_count": len(strong_correlations),
            "summary": f"Found {len(strong_correlations)} strong correlations"
        }

    def anomaly_detection(self, method: str = "iqr") -> Dict[str, Any]:
        """
        Detect anomalies and outliers in data.

        Parameters
        ----------
        method : str
            Detection method: 'iqr' (Interquartile Range) or 'zscore'

        Returns
        -------
        dict
            Dictionary containing anomalies and statistics
        """
        anomalies = {}
        
        for col in self.numeric_cols:
            col_data = self.data[col].dropna()
            
            if method == "iqr":
                q1 = col_data.quantile(0.25)
                q3 = col_data.quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                outlier_mask = (col_data < lower_bound) | (col_data > upper_bound)
                
            elif method == "zscore":
                mean = col_data.mean()
                std = col_data.std()
                if std > 0:
                    z_scores = np.abs((col_data - mean) / std)
                    outlier_mask = z_scores > 3
                else:
                    outlier_mask = pd.Series([False] * len(col_data))
            else:
                continue

            if outlier_mask.any():
                outliers = col_data[outlier_mask]
                anomalies[col] = {
                    "count": len(outliers),
                    "percentage": round(len(outliers) / len(col_data) * 100, 2),
                    "values": outliers.tolist()[:10],  # Top 10 anomalies
                    "mean": round(col_data.mean(), 4),
                    "std": round(col_data.std(), 4)
                }

        return {
            "anomalies": anomalies,
            "total_anomalies_found": sum(len(v.get("values", [])) for v in anomalies.values()),
            "affected_columns": list(anomalies.keys()),
            "method": method
        }

    def trend_analysis(self, time_column: str = None) -> Dict[str, Any]:
        """
        Analyze trends over time or sequence.

        Parameters
        ----------
        time_column : str, optional
            Column name for time-based analysis. If None, analyzes by row sequence.

        Returns
        -------
        dict
            Dictionary containing trend analysis results
        """
        trends = {}

        for col in self.numeric_cols:
            col_data = self.data[col].dropna()
            if len(col_data) < 2:
                continue

            # Calculate trend using simple linear regression
            x = np.arange(len(col_data))
            y = col_data.values
            
            # Fit line: y = mx + b
            coefficients = np.polyfit(x, y, 1)
            slope = coefficients[0]
            
            # Determine trend direction
            if slope > 0.001:
                direction = "Increasing"
                strength = "strong" if abs(slope) > 0.1 else "weak"
            elif slope < -0.001:
                direction = "Decreasing"
                strength = "strong" if abs(slope) > 0.1 else "weak"
            else:
                direction = "Stable"
                strength = "no"

            trends[col] = {
                "direction": direction,
                "strength": strength,
                "slope": round(float(slope), 6),
                "first_value": float(y[0]),
                "last_value": float(y[-1]),
                "change_pct": round((y[-1] - y[0]) / y[0] * 100, 2) if y[0] != 0 else 0,
                "volatility": round(col_data.std() / col_data.mean() * 100, 2) if col_data.mean() != 0 else 0
            }

        return {
            "trends": trends,
            "analysis_type": "Time series" if time_column else "Sequential",
            "columns_analyzed": list(trends.keys())
        }

    def distribution_analysis(self) -> Dict[str, Any]:
        """
        Analyze data distribution patterns.

        Returns
        -------
        dict
            Dictionary containing distribution insights
        """
        distributions = {}

        for col in self.numeric_cols:
            col_data = self.data[col].dropna()
            if len(col_data) == 0:
                continue

            skewness = col_data.skew()
            kurtosis = col_data.kurtosis()

            # Classify distribution
            if abs(skewness) < 0.5:
                distribution_type = "Approximately symmetric"
            elif skewness > 0:
                distribution_type = "Right-skewed (positive skew)"
            else:
                distribution_type = "Left-skewed (negative skew)"

            distributions[col] = {
                "type": distribution_type,
                "skewness": round(float(skewness), 4),
                "kurtosis": round(float(kurtosis), 4),
                "normality": "Non-normal" if abs(skewness) > 0.5 or abs(kurtosis) > 3 else "Approximately normal",
                "mean": round(float(col_data.mean()), 4),
                "median": round(float(col_data.median()), 4),
                "mode": col_data.mode()[0] if not col_data.mode().empty else None
            }

        return {
            "distributions": distributions,
            "total_columns_analyzed": len(distributions),
            "columns_analyzed": list(distributions.keys())
        }

    def data_quality_assessment(self) -> Dict[str, Any]:
        """
        Comprehensive data quality assessment.

        Returns
        -------
        dict
            Dictionary containing data quality metrics and issues
        """
        total_cells = self.data.shape[0] * self.data.shape[1]
        missing_cells = self.data.isnull().sum().sum()
        duplicate_rows = self.data.duplicated().sum()
        
        quality_score = 100
        issues = []

        # Check missing values
        missing_pct = (missing_cells / total_cells * 100) if total_cells > 0 else 0
        if missing_pct > 20:
            quality_score -= 20
            issues.append(f"High missing data: {missing_pct:.2f}%")
        elif missing_pct > 5:
            quality_score -= 10
            issues.append(f"Moderate missing data: {missing_pct:.2f}%")

        # Check duplicates
        duplicate_pct = (duplicate_rows / len(self.data) * 100) if len(self.data) > 0 else 0
        if duplicate_pct > 10:
            quality_score -= 15
            issues.append(f"High duplicate rows: {duplicate_pct:.2f}%")
        elif duplicate_pct > 1:
            quality_score -= 5
            issues.append(f"Some duplicate rows: {duplicate_pct:.2f}%")

        # Check for columns with all same values
        for col in self.data.columns:
            if self.data[col].nunique() == 1:
                quality_score -= 5
                issues.append(f"Column '{col}' has constant values")

        # Check outliers
        for col in self.numeric_cols:
            col_data = self.data[col].dropna()
            if len(col_data) > 0:
                q1 = col_data.quantile(0.25)
                q3 = col_data.quantile(0.75)
                iqr = q3 - q1
                if iqr > 0:
                    outliers = ((col_data < (q1 - 1.5 * iqr)) | (col_data > (q3 + 1.5 * iqr))).sum()
                    outlier_pct = (outliers / len(col_data) * 100) if len(col_data) > 0 else 0
                    if outlier_pct > 5:
                        quality_score -= 2
                        issues.append(f"Column '{col}' has {outlier_pct:.1f}% outliers")

        quality_score = max(0, quality_score)  # Ensure non-negative

        return {
            "quality_score": quality_score,
            "total_cells": total_cells,
            "missing_cells": missing_cells,
            "missing_pct": round(missing_pct, 2),
            "duplicate_rows": duplicate_rows,
            "duplicate_pct": round(duplicate_pct, 2),
            "issues_found": len(issues),
            "issues": issues,
            "quality_rating": self._get_quality_rating(quality_score),
            "recommendations": self._get_quality_recommendations(issues)
        }

    def generate_insights_and_recommendations(self) -> List[Dict[str, str]]:
        """
        Generate actionable insights and recommendations based on comprehensive analysis.

        Returns
        -------
        list
            List of insight dictionaries with recommendations
        """
        insights = []

        # Correlation insights
        corr_analysis = self.correlation_analysis()
        if corr_analysis.get("strong_correlations"):
            for corr in corr_analysis["strong_correlations"][:3]:  # Top 3
                insights.append({
                    "type": "correlation",
                    "title": f"Strong relationship found: {corr['variable1']} & {corr['variable2']}",
                    "message": f"{corr['strength']} correlation ({corr['correlation']}) detected. "
                              f"These variables move together and could be useful for prediction models.",
                    "severity": "info",
                    "action": "Consider using one as a feature for machine learning models"
                })

        # Anomaly insights
        anomalies = self.anomaly_detection()
        if anomalies.get("affected_columns"):
            insights.append({
                "type": "anomaly",
                "title": "Anomalies detected",
                "message": f"Found {anomalies['total_anomalies_found']} anomalies across "
                          f"{len(anomalies['affected_columns'])} columns. "
                          f"These outliers may indicate data entry errors or genuine unusual events.",
                "severity": "warning",
                "action": "Review anomalies and determine if they should be removed or kept for analysis"
            })

        # Trend insights
        trends = self.trend_analysis()
        increasing_trends = [k for k, v in trends.get("trends", {}).items() if v["direction"] == "Increasing"]
        decreasing_trends = [k for k, v in trends.get("trends", {}).items() if v["direction"] == "Decreasing"]
        
        if increasing_trends:
            insights.append({
                "type": "trend",
                "title": f"Upward trend(s) identified",
                "message": f"{', '.join(increasing_trends)} showing increasing trends. "
                          f"This indicates positive growth or escalation over time.",
                "severity": "info",
                "action": "Monitor these trends for business opportunities or capacity planning"
            })

        if decreasing_trends:
            insights.append({
                "type": "trend",
                "title": f"Downward trend(s) identified",
                "message": f"{', '.join(decreasing_trends)} showing decreasing trends. "
                          f"This may indicate declining performance or reduced activity.",
                "severity": "warning",
                "action": "Investigate root causes and implement corrective measures if needed"
            })

        # Distribution insights
        distributions = self.distribution_analysis()
        non_normal = [col for col, dist in distributions.get("distributions", {}).items() 
                     if dist.get("normality") == "Non-normal"]
        if non_normal:
            insights.append({
                "type": "distribution",
                "title": "Non-normal distributions found",
                "message": f"{', '.join(non_normal)} have non-normal distributions. "
                          f"Consider transformations for statistical tests or use non-parametric methods.",
                "severity": "info",
                "action": "Apply log or other transformations for normalized analysis"
            })

        # Quality insights
        quality = self.data_quality_assessment()
        if quality["issues"]:
            insights.append({
                "type": "quality",
                "title": f"Data quality score: {quality['quality_score']}%",
                "message": f"Data quality assessment identified {len(quality['issues'])} issues. "
                          f"Quality rating: {quality['quality_rating']}",
                "severity": "warning" if quality["quality_score"] < 70 else "info",
                "action": "Address identified issues to improve data reliability"
            })

        # Statistical insights
        high_variance_cols = [col for col in self.numeric_cols 
                            if self.data[col].std() / self.data[col].mean() > 1 
                            if self.data[col].mean() != 0]
        if high_variance_cols:
            insights.append({
                "type": "statistical",
                "title": "High variability detected",
                "message": f"{', '.join(high_variance_cols[:3])} show high variability (CV > 100%). "
                          f"This indicates inconsistent or diverse data patterns.",
                "severity": "info",
                "action": "Investigate sources of variation and consider stratified analysis"
            })

        return insights

    @staticmethod
    def _get_quality_rating(score: float) -> str:
        """Get quality rating based on score."""
        if score >= 90:
            return "Excellent"
        elif score >= 80:
            return "Good"
        elif score >= 70:
            return "Fair"
        elif score >= 50:
            return "Poor"
        else:
            return "Critical"

    @staticmethod
    def _get_quality_recommendations(issues: List[str]) -> List[str]:
        """Generate recommendations based on quality issues."""
        recommendations = []
        
        if any("missing" in issue.lower() for issue in issues):
            recommendations.append("Impute or remove rows/columns with missing values")
        
        if any("duplicate" in issue.lower() for issue in issues):
            recommendations.append("Remove duplicate rows to ensure data uniqueness")
        
        if any("constant" in issue.lower() for issue in issues):
            recommendations.append("Remove columns with constant values as they add no information")
        
        if any("outlier" in issue.lower() for issue in issues):
            recommendations.append("Investigate and handle outliers appropriately")
        
        if not recommendations:
            recommendations.append("Data quality is good - proceed with analysis")
        
        return recommendations

    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive analysis report.

        Returns
        -------
        dict
            Complete analysis report with all metrics
        """
        return {
            "data_overview": {
                "rows": len(self.data),
                "columns": len(self.data.columns),
                "numeric_columns": len(self.numeric_cols),
                "categorical_columns": len(self.categorical_cols)
            },
            "correlation_analysis": self.correlation_analysis(),
            "anomaly_detection": self.anomaly_detection(),
            "trend_analysis": self.trend_analysis(),
            "distribution_analysis": self.distribution_analysis(),
            "data_quality": self.data_quality_assessment(),
            "insights_and_recommendations": self.generate_insights_and_recommendations(),
            "analysis_timestamp": pd.Timestamp.now().isoformat()
        }
