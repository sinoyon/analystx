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
        Calculate KPIs from data.

        Parameters
        ----------
        data : pd.DataFrame
            Data to calculate KPIs from
        config : dict, optional
            Configuration for KPI calculation

        Returns
        -------
        dict
            Dictionary of calculated KPIs
        """
        kpis = {}

        # Basic numeric KPIs
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            kpis[f"{col}_mean"] = data[col].mean()
            kpis[f"{col}_median"] = data[col].median()
            kpis[f"{col}_std"] = data[col].std()
            kpis[f"{col}_min"] = data[col].min()
            kpis[f"{col}_max"] = data[col].max()

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
