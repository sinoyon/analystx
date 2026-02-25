"""
Main AnalystX module containing the core analyzer class.
"""

import pandas as pd
from .profiling import DataProfiler
from .kpi_engine import KPIEngine
from .insight_engine import InsightEngine
from .report import ReportGenerator
from .insights_generator import InsightsAnalyzer, format_report_as_html


class AnalysisResult:
    """
    Wrapper class for analysis results with export capabilities.
    
    Provides convenient access to analysis outputs and export methods.
    """
    
    def __init__(self, profile=None, kpis=None, insights=None, report=None, 
                 business_context=None, analyzer=None):
        """Initialize analysis results."""
        self.profile = profile
        self.kpis = kpis
        self.insights = insights
        self.report = report
        self.business_context = business_context
        self.analyzer = analyzer
    
    def to_html(self, filepath=None):
        """
        Export report as HTML.
        
        Parameters
        ----------
        filepath : str, optional
            Path to save the HTML file. If None, returns HTML string.
            
        Returns
        -------
        str or None
            HTML string if filepath is None, else None (saves to file)
        """
        if isinstance(self.report, str):
            html_content = self.report
        elif isinstance(self.report, pd.DataFrame):
            html_content = self.report.to_html()
        else:
            html_content = str(self.report)
        
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return filepath
        return html_content
    
    def to_pdf(self, filepath):
        """
        Export report as PDF (requires pdfkit or similar).
        
        Parameters
        ----------
        filepath : str
            Path to save the PDF file
        """
        try:
            import pdfkit
            html = self.to_html()
            pdfkit.from_string(html, filepath)
            return filepath
        except ImportError:
            raise ImportError("pdfkit required for PDF export. Install with: pip install pdfkit")
    
    def to_dataframe(self):
        """Get report as pandas DataFrame if applicable."""
        if isinstance(self.report, pd.DataFrame):
            return self.report
        return None
    
    def __repr__(self):
        """String representation."""
        return (f"AnalysisResult(profile_keys={list(self.profile.keys()) if isinstance(self.profile, dict) else 'N/A'}, "
                f"kpis_count={len(self.kpis) if self.kpis else 0}, "
                f"insights_count={len(self.insights) if self.insights else 0})")
    
    def __str__(self):
        """Detailed string representation."""
        lines = ["AnalystX Analysis Results", "=" * 40]
        if self.business_context:
            lines.append(f"Context: {self.business_context}")
        lines.append(f"Profile: {type(self.profile).__name__}")
        lines.append(f"KPIs: {type(self.kpis).__name__}")
        lines.append(f"Insights: {type(self.insights).__name__}")
        lines.append(f"Report: {type(self.report).__name__}")
        return "\n".join(lines)


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
    AnalysisResult
        Result object containing:
        - result.profile : Data profile results
        - result.kpis : Calculated KPIs
        - result.insights : Generated insights
        - result.report : Generated report
        - result.business_context : Analysis context
        - result.analyzer : AnalystX instance
        
        Methods:
        - result.to_html(filepath=None) : Export as HTML
        - result.to_pdf(filepath) : Export as PDF
        - result.to_dataframe() : Get as DataFrame

    Example
    -------
    >>> import pandas as pd
    >>> from analystx import analyze
    >>> df = pd.read_csv('sales_data.csv')
    >>> results = analyze(df, business_context="Sales analysis")
    >>> results.to_html("report.html")  # Export to HTML
    >>> print(results.insights)  # Access insights
    >>> print(results.kpis)  # Access KPIs
    """
    analyzer = AnalystX(data=data)
    profile = analyzer.profile()
    kpis = analyzer.calculate_kpis()
    insights = analyzer.generate_insights()
    
    # Generate enhanced business-focused analysis
    enhanced_insights = InsightsAnalyzer(data)
    analysis_summary = enhanced_insights.generate_summary()
    
    # Create comprehensive report
    report = analyzer.create_report(output_format=output_format)
    
    # Format as HTML with enhanced insights
    html_report = format_report_as_html({
        'title': 'Data Analysis Report',
        'context': business_context or 'General Data Analysis',
        'generated_at': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
        'data_shape': {'rows': len(data), 'columns': len(data.columns)},
        'summary': analysis_summary,
    })

    return AnalysisResult(
        profile=profile,
        kpis=kpis,
        insights=analysis_summary,
        report=html_report,
        business_context=business_context,
        analyzer=analyzer,
    )
