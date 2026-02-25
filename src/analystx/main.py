"""
Main AnalystX module containing the core analyzer class.
"""

import pandas as pd
from .profiling import DataProfiler
from .kpi_engine import KPIEngine
from .insight_engine import InsightEngine
from .report import ReportGenerator


class AnalystX:
    """Main analyzer class for data profiling, KPI calculation, and insight generation."""

    def __init__(self, data=None):
        """
        Initialize AnalystX analyzer.

        Parameters
        ----------
        data : pd.DataFrame, optional
            Input dataframe for analysis
        """
        self.data = data
        self.profiler = DataProfiler()
        self.kpi_engine = KPIEngine()
        self.insight_engine = InsightEngine()
        self.report_generator = ReportGenerator()
        self._profile = None
        self._kpis = None
        self._insights = None

    def load_data(self, data):
        """
        Load or update data for analysis.

        Parameters
        ----------
        data : pd.DataFrame
            Dataframe to analyze
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Data must be a pandas DataFrame")
        self.data = data
        return self

    def profile(self):
        """
        Generate data profile including statistical summaries and quality metrics.

        Returns
        -------
        dict
            Profile results
        """
        if self.data is None:
            raise ValueError("No data loaded. Use load_data() first.")
        self._profile = self.profiler.analyze(self.data)
        return self._profile

    def calculate_kpis(self, config=None):
        """
        Calculate KPIs based on provided configuration.

        Parameters
        ----------
        config : dict, optional
            KPI configuration

        Returns
        -------
        dict
            Calculated KPIs
        """
        if self.data is None:
            raise ValueError("No data loaded. Use load_data() first.")
        self._kpis = self.kpi_engine.calculate(self.data, config)
        return self._kpis

    def generate_insights(self):
        """
        Generate insights from profiling and KPI results.

        Returns
        -------
        list
            List of insights
        """
        if self._profile is None:
            self.profile()
        self._insights = self.insight_engine.generate(self.data, self._profile, self._kpis)
        return self._insights

    def create_report(self, output_format="html"):
        """
        Create a comprehensive report.

        Parameters
        ----------
        output_format : str, optional
            Output format (html, pdf, markdown)

        Returns
        -------
        str
            Report content or file path
        """
        if self._profile is None:
            self.profile()
        if self._insights is None:
            self.generate_insights()

        report = self.report_generator.generate(
            data=self.data,
            profile=self._profile,
            kpis=self._kpis,
            insights=self._insights,
            format=output_format
        )
        return report


def analyze(data, business_context=None, output_format="html"):
    """
    Convenience function for quick data analysis.

    Performs complete analysis workflow: profiling, KPI calculation, 
    insight generation, and report creation in one call.

    Parameters
    ----------
    data : pd.DataFrame
        Input data to analyze
    business_context : str, optional
        Business context or description of the analysis
    output_format : str, optional
        Output format (html, pdf, markdown). Default is 'html'

    Returns
    -------
    dict
        Dictionary containing:
        - 'profile': Data profile results
        - 'kpis': Calculated KPIs
        - 'insights': Generated insights
        - 'report': Generated report

    Example
    -------
    >>> import pandas as pd
    >>> from analystx import analyze
    >>> df = pd.read_csv('sales_data.csv')
    >>> results = analyze(df, business_context="Sales analysis")
    >>> print(results['insights'])
    """
    analyzer = AnalystX(data=data)
    profile = analyzer.profile()
    kpis = analyzer.calculate_kpis()
    insights = analyzer.generate_insights()
    report = analyzer.create_report(output_format=output_format)

    return {
        'profile': profile,
        'kpis': kpis,
        'insights': insights,
        'report': report,
        'business_context': business_context,
        'analyzer': analyzer,
    }
