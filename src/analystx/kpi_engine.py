"""
KPI Engine for calculating key performance indicators from data.
"""

import pandas as pd
import numpy as np


class KPIEngine:
    """Calculate and manage key performance indicators."""

    def __init__(self):
        """Initialize KPI engine with default metrics."""
        self.custom_kpis = {}

    def calculate(self, data, config=None):
        """
        Calculate KPIs from data with comprehensive statistical metrics.

        Parameters
        ----------
        data : pd.DataFrame
            Data to calculate KPIs from
        config : dict, optional
            Configuration for KPI calculation

        Returns
        -------
        dict
            Dictionary of calculated KPIs including basic stats and advanced metrics
        """
        kpis = {}

        # Basic and advanced numeric KPIs
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            col_data = data[col].dropna()
            if len(col_data) == 0:
                continue
                
            # Basic statistics
            kpis[f"{col}_count"] = len(col_data)
            kpis[f"{col}_sum"] = col_data.sum()
            kpis[f"{col}_mean"] = col_data.mean()
            kpis[f"{col}_median"] = col_data.median()
            kpis[f"{col}_mode"] = col_data.mode()[0] if not col_data.mode().empty else None
            kpis[f"{col}_std"] = col_data.std()
            kpis[f"{col}_variance"] = col_data.var()
            
            # Range and spread metrics
            kpis[f"{col}_min"] = col_data.min()
            kpis[f"{col}_max"] = col_data.max()
            kpis[f"{col}_range"] = col_data.max() - col_data.min()
            kpis[f"{col}_q1"] = col_data.quantile(0.25)
            kpis[f"{col}_q3"] = col_data.quantile(0.75)
            kpis[f"{col}_iqr"] = kpis[f"{col}_q3"] - kpis[f"{col}_q1"]
            
            # Advanced metrics
            kpis[f"{col}_cv"] = (col_data.std() / col_data.mean() * 100) if col_data.mean() != 0 else 0  # Coefficient of variation
            kpis[f"{col}_skewness"] = col_data.skew()
            kpis[f"{col}_kurtosis"] = col_data.kurtosis()
            
            # Outlier detection (outliers beyond 1.5*IQR from quartiles)
            q1 = kpis[f"{col}_q1"]
            q3 = kpis[f"{col}_q3"]
            iqr = kpis[f"{col}_iqr"]
            outliers = col_data[(col_data < (q1 - 1.5 * iqr)) | (col_data > (q3 + 1.5 * iqr))]
            kpis[f"{col}_outliers_count"] = len(outliers)
            kpis[f"{col}_outliers_pct"] = (len(outliers) / len(col_data) * 100) if len(col_data) > 0 else 0

        # Overall dataset metrics
        kpis["total_rows"] = len(data)
        kpis["total_columns"] = len(data.columns)
        kpis["missing_values"] = data.isnull().sum().sum()
        kpis["missing_pct"] = (data.isnull().sum().sum() / (len(data) * len(data.columns)) * 100) if len(data) > 0 else 0
        kpis["duplicate_rows"] = data.duplicated().sum()
        kpis["duplicate_pct"] = (data.duplicated().sum() / len(data) * 100) if len(data) > 0 else 0

        # Add custom KPIs if provided
        if config:
            kpis.update(self._calculate_custom_kpis(data, config))

        return kpis

    def register_kpi(self, name, func):
        """
        Register a custom KPI calculation function.

        Parameters
        ----------
        name : str
            Name of the KPI
        func : callable
            Function that calculates the KPI
        """
        self.custom_kpis[name] = func

    def _calculate_custom_kpis(self, data, config):
        """Calculate custom KPIs based on configuration."""
        custom_results = {}
        for kpi_name, kpi_config in config.items():
            if kpi_name in self.custom_kpis:
                try:
                    custom_results[kpi_name] = self.custom_kpis[kpi_name](data, kpi_config)
                except Exception as e:
                    custom_results[kpi_name] = f"Error: {str(e)}"
        return custom_results
