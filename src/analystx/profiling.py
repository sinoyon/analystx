"""
Data profiling module for comprehensive data analysis and quality assessment.
"""

import pandas as pd
import numpy as np


class DataProfiler:
    """Generate detailed data profiles including statistics and quality metrics."""

    def analyze(self, data):
        """
        Analyze dataset and generate comprehensive profile.

        Parameters
        ----------
        data : pd.DataFrame
            Data to profile

        Returns
        -------
        dict
            Profile results including shape, dtypes, statistics, and quality metrics
        """
        profile = {
            "shape": data.shape,
            "columns": list(data.columns),
            "dtypes": data.dtypes.to_dict(),
            "summary_stats": self._get_summary_stats(data),
            "missing_values": self._get_missing_values(data),
            "unique_counts": self._get_unique_counts(data),
            "quality_metrics": self._get_quality_metrics(data),
        }
        return profile

    @staticmethod
    def _get_summary_stats(data):
        """Generate summary statistics for numeric columns."""
        numeric_data = data.select_dtypes(include=[np.number])
        if numeric_data.empty:
            return {}
        return numeric_data.describe().to_dict()

    @staticmethod
    def _get_missing_values(data):
        """Calculate missing value statistics."""
        missing = data.isnull().sum()
        missing_pct = (missing / len(data) * 100).round(2)
        return {
            "count": missing.to_dict(),
            "percentage": missing_pct.to_dict(),
        }

    @staticmethod
    def _get_unique_counts(data):
        """Get unique value counts for all columns."""
        return data.nunique().to_dict()

    @staticmethod
    def _get_quality_metrics(data):
        """Calculate data quality metrics."""
        total_cells = data.shape[0] * data.shape[1]
        missing_cells = data.isnull().sum().sum()
        completeness = ((total_cells - missing_cells) / total_cells * 100)

        return {
            "completeness_pct": round(completeness, 2),
            "total_cells": total_cells,
            "missing_cells": missing_cells,
            "duplicate_rows": data.duplicated().sum(),
        }
