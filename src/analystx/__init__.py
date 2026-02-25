"""
AnalystX: Advanced analytics and KPI engine for data-driven insights.

A comprehensive Python library for data profiling, KPI calculation, insight 
generation, and professional report creation.

Example:
    >>> from analystx import AnalystX
    >>> import pandas as pd
    >>> df = pd.read_csv('data.csv')
    >>> analyzer = AnalystX(data=df)
    >>> profile = analyzer.profile()
    >>> kpis = analyzer.calculate_kpis()
    >>> insights = analyzer.generate_insights()
    >>> report = analyzer.create_report()
"""

__version__ = "0.4.0"
__author__ = "MD Shariful Islam"
__email__ = "srnoyon780@gmail.com"
__license__ = "MIT"
__description__ = "Advanced analytics and KPI engine for data-driven insights"

# Import main classes and functions
from .main import AnalystX, analyze, AnalysisResult
from .profiling import DataProfiler
from .kpi_engine import KPIEngine
from .insight_engine import InsightEngine
from .report import ReportGenerator

# Public API
__all__ = [
    "AnalystX",
    "analyze",
    "AnalysisResult",
    "DataProfiler",
    "KPIEngine",
    "InsightEngine",
    "ReportGenerator",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]
