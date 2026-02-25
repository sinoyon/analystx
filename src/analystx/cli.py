"""
Command-line interface for AnalystX.
"""

import argparse
import sys
import pandas as pd
from .main import AnalystX


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AnalystX: Advanced analytics and KPI engine"
    )

    parser.add_argument(
        "command",
        choices=["profile", "kpi", "insight", "report"],
        help="Command to execute"
    )

    parser.add_argument(
        "--data",
        type=str,
        help="Path to input data file (CSV, Excel, etc.)"
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Path to output file"
    )

    parser.add_argument(
        "--format",
        choices=["html", "markdown", "pdf"],
        default="html",
        help="Output format for reports"
    )

    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file (JSON)"
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    args = parser.parse_args()

    try:
        if not args.data:
            parser.print_help()
            print("\nError: --data argument is required")
            sys.exit(1)

        # Load data
        if args.data.endswith(".csv"):
            data = pd.read_csv(args.data)
        elif args.data.endswith((".xlsx", ".xls")):
            data = pd.read_excel(args.data)
        else:
            print(f"Unsupported file format: {args.data}")
            sys.exit(1)

        # Initialize analyzer
        analyzer = AnalystX(data=data)

        # Execute command
        if args.command == "profile":
            result = analyzer.profile()
            print("Data Profile:")
            print(result)

        elif args.command == "kpi":
            result = analyzer.calculate_kpis()
            print("KPIs:")
            for kpi, value in result.items():
                print(f"  {kpi}: {value}")

        elif args.command == "insight":
            result = analyzer.generate_insights()
            print("Insights:")
            for insight in result:
                print(f"  - {insight.get('message', 'N/A')}")

        elif args.command == "report":
            result = analyzer.create_report(output_format=args.format)
            if args.output:
                if args.format == "html":
                    with open(args.output, "w") as f:
                        f.write(result)
                else:
                    with open(args.output, "w") as f:
                        f.write(result)
                print(f"Report saved to {args.output}")
            else:
                print(result)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
