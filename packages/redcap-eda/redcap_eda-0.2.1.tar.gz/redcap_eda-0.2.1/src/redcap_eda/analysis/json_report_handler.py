"""
📌 JSONReportHandler: Manages JSON export and display of EDA analysis results.

🔹 **Purpose**:
    - Aggregates analysis results into a structured JSON format.
    - Saves the report to a specified output directory.
    - Provides an option to display the report in a human-readable format.

🔹 **Why Use This?**
    - Simplifies `ExploratoryDataAnalysis` by delegating JSON-related tasks.
    - Ensures a consistent approach to storing and displaying analysis results.

🔹 **Example Usage**:
    ```python
    from redcap_eda.analysis.json_report_handler import JSONReportHandler
    report_handler = JSONReportHandler(output_dir="eda_reports")
    report_handler.collect_results(results)
    report_handler.save_report(display=True)
    ```
"""

import os
import json
import numpy as np
from typing import Any
from redcap_eda.logger import logger


class JSONReportHandler:
    """Handles JSON export and display of EDA analysis results."""

    def __init__(self, output_dir: str) -> None:
        """
        Initializes the JSONReportHandler.

        Args:
            output_dir (str): Directory to save the JSON report.
        """
        self.output_dir = output_dir
        self.report_data: dict[str, dict[str, Any]] = {}

    def collect_results(self, results: list[dict[str, dict[str, Any] | str]]) -> None:
        """
        Collects and aggregates analysis results.

        Args:
            results (list[dict[str, dict[str, Any] | str]]): List of analysis results
                where each item is a dictionary containing column analysis data.
        """
        logger.debug("📥 Collecting analysis results for JSON report...")

        for result in results:
            for col, analysis in result.items():
                if isinstance(analysis, dict):
                    self.report_data[col] = analysis
                else:
                    self.report_data[col] = {"message": str(analysis)}

        logger.debug(f"📑 Collected {len(self.report_data)} columns for the report.")

    def save_report(self, display: bool = False) -> None:
        """
        Saves the collected report as a JSON file and optionally displays it.

        Args:
            display (bool, optional): If True, displays the report after saving.
        """
        json_path = os.path.join(self.output_dir, "eda_report.json")

        try:
            # Convert and serialize while handling NumPy types
            json_data = json.dumps(
                self.report_data,
                indent=4,
                default=lambda x: x.item() if isinstance(x, np.generic) else str(x),
            )

            # Write to file
            with open(json_path, "w") as f:
                f.write(json_data)

            logger.info(f"📂 Saved EDA report to {json_path}")

            if display:
                self.display_report(json_path)

        except Exception as e:
            logger.error(f"❌ Error saving report: {e}")

    @staticmethod
    def display_report(json_path: str) -> None:
        """
        Loads and displays the EDA report from a JSON file in a human-readable format.

        Args:
            json_path (str): The path to the saved JSON report.
        """
        if not os.path.exists(json_path):
            logger.error(f"❌ Report file not found: {json_path}")
            return

        try:
            with open(json_path) as f:
                report = json.load(f)

            logger.info(f"📂 Loaded EDA report from {json_path}\n")

            # Format and print the report in a human-readable format
            for col, stats in report.items():
                print(f"📌 Column: {col}")
                if isinstance(stats, dict):
                    for key, value in stats.items():
                        print(f"   - {key}: {value}")
                else:
                    print(f"   - {stats}")  # Handles error messages or skipped analysis
                print("-" * 40)

        except json.JSONDecodeError as e:
            logger.error(f"❌ Failed to parse JSON: {e}")
        except Exception as e:
            logger.error(f"❌ Error loading report: {e}")
