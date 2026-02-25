"""
Dictionary module for managing business logic and metadata.
"""


class DataDictionary:
    """Manage data dictionary, metadata, and business logic definitions."""

    def __init__(self):
        """Initialize data dictionary."""
        self.definitions = {}
        self.metrics = {}
        self.transformations = {}

    def add_definition(self, name, definition):
        """
        Add a column or metric definition.

        Parameters
        ----------
        name : str
            Name of the item
        definition : dict
            Definition details (type, description, format, etc.)
        """
        self.definitions[name] = definition

    def add_metric(self, name, formula, description=""):
        """
        Add a business metric definition.

        Parameters
        ----------
        name : str
            Metric name
        formula : str
            Metric calculation formula or expression
        description : str, optional
            Metric description
        """
        self.metrics[name] = {
            "formula": formula,
            "description": description
        }

    def add_transformation(self, name, func, description=""):
        """
        Register a data transformation.

        Parameters
        ----------
        name : str
            Transformation name
        func : callable
            Transformation function
        description : str, optional
            Description of the transformation
        """
        self.transformations[name] = {
            "function": func,
            "description": description
        }

    def get_definition(self, name):
        """Get a definition."""
        return self.definitions.get(name)

    def get_metric(self, name):
        """Get a metric definition."""
        return self.metrics.get(name)

    def list_all(self):
        """List all definitions and metrics."""
        return {
            "definitions": self.definitions,
            "metrics": self.metrics,
            "transformations": list(self.transformations.keys())
        }
