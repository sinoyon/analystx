"""
Basic tests for AnalystX functionality.
"""

import pytest
import pandas as pd
import numpy as np
from analystx import AnalystX


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return pd.DataFrame({
        "id": [1, 2, 3, 4, 5],
        "value": [10.5, 20.3, 15.8, 30.1, 25.6],
        "category": ["A", "B", "A", "B", "A"],
        "flag": [True, False, True, False, True]
    })


class TestAnalystXBasic:
    """Basic tests for AnalystX core functionality."""

    def test_initialization(self):
        """Test initialization without data."""
        analyzer = AnalystX()
        assert analyzer.data is None

    def test_load_data(self, sample_data):
        """Test loading data."""
        analyzer = AnalystX()
        analyzer.load_data(sample_data)
        assert analyzer.data is not None
        assert len(analyzer.data) == 5

    def test_initialization_with_data(self, sample_data):
        """Test initialization with data."""
        analyzer = AnalystX(data=sample_data)
        assert analyzer.data is not None

    def test_profiling(self, sample_data):
        """Test data profiling."""
        analyzer = AnalystX(data=sample_data)
        profile = analyzer.profile()

        assert profile is not None
        assert "shape" in profile
        assert "columns" in profile
        assert "dtypes" in profile
        assert "missing_values" in profile

    def test_kpi_calculation(self, sample_data):
        """Test KPI calculation."""
        analyzer = AnalystX(data=sample_data)
        kpis = analyzer.calculate_kpis()

        assert kpis is not None
        assert isinstance(kpis, dict)
        assert "value_mean" in kpis

    def test_insight_generation(self, sample_data):
        """Test insight generation."""
        analyzer = AnalystX(data=sample_data)
        insights = analyzer.generate_insights()

        assert insights is not None
        assert isinstance(insights, list)

    def test_report_generation(self, sample_data):
        """Test report generation."""
        analyzer = AnalystX(data=sample_data)
        report = analyzer.create_report(output_format="html")

        assert report is not None
        assert isinstance(report, str)
        assert "AnalystX Report" in report

    def test_report_markdown(self, sample_data):
        """Test markdown report generation."""
        analyzer = AnalystX(data=sample_data)
        report = analyzer.create_report(output_format="markdown")

        assert report is not None
        assert isinstance(report, str)
        assert "# AnalystX Report" in report

    def test_error_on_missing_data(self):
        """Test error when no data is loaded."""
        analyzer = AnalystX()
        with pytest.raises(ValueError):
            analyzer.profile()

    def test_invalid_data_type(self):
        """Test error with invalid data type."""
        analyzer = AnalystX()
        with pytest.raises(TypeError):
            analyzer.load_data([1, 2, 3])


class TestDataProfiler:
    """Tests for data profiling functionality."""

    def test_profile_columns(self, sample_data):
        """Test column detection in profile."""
        analyzer = AnalystX(data=sample_data)
        profile = analyzer.profile()

        assert len(profile["columns"]) == 4
        assert "id" in profile["columns"]
        assert "value" in profile["columns"]

    def test_profile_dtypes(self, sample_data):
        """Test dtype detection in profile."""
        analyzer = AnalystX(data=sample_data)
        profile = analyzer.profile()

        assert "id" in profile["dtypes"]


class TestKPIEngine:
    """Tests for KPI engine functionality."""

    def test_kpi_mean(self, sample_data):
        """Test mean KPI calculation."""
        analyzer = AnalystX(data=sample_data)
        kpis = analyzer.calculate_kpis()

        expected_mean = sample_data["value"].mean()
        assert abs(kpis["value_mean"] - expected_mean) < 0.01

    def test_kpi_median(self, sample_data):
        """Test median KPI calculation."""
        analyzer = AnalystX(data=sample_data)
        kpis = analyzer.calculate_kpis()

        expected_median = sample_data["value"].median()
        assert abs(kpis["value_median"] - expected_median) < 0.01


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
