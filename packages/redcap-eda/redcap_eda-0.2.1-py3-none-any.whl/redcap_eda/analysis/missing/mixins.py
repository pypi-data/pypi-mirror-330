"""
📌 MissingDataAnalysisMixin: Analyzes and visualizes missing data in datasets.

🔹 **Purpose**:
    - Computes summary of missing values per column.
    - Generates a **heatmap** to visualize missing data distribution.
    - Supports integration with **UnifiedReport** for EDA reporting.

🔹 **Example Usage**:
    ```python
    from redcap_eda.analysis.missing.mixins import MissingDataAnalysisMixin
    class MyClass(MissingDataAnalysisMixin):
        pass
    obj = MyClass()
    missing_summary, heatmap_fig, heatmap_filename = obj.analyze_missing_data(df)
    ```
"""

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from redcap_eda.logger import logger
from redcap_eda.analysis.lib import AnalysisResult


class MissingDataAnalysisMixin:
    """Mixin for analyzing and visualizing missing data in datasets."""

    __slots__ = ()

    @staticmethod
    def analyze_missing_data(df: pd.DataFrame, output_dir: str) -> AnalysisResult:
        """Analyze missing data in a DataFrame & generate a heatmap.

        Args:
            df (pd.DataFrame): The dataset to analyze.
            output_dir (str): The directory to save output files.

        Returns:
            AnalysisResult: Named tuple containing summary statistics and plots.
        """
        if df.empty:
            logger.warning("⚠️ Skipping missing data analysis on empty DataFrame.")
            return AnalysisResult(
                summary={"error": "DataFrame is empty"},
                plot_paths=[],
            )

        # Compute missing values summary
        missing_summary = df.isnull().sum().to_dict()
        summary = ("Missing Values Summary", missing_summary)

        # Generate heatmap for missing data visualization
        plot_paths = [
            MissingDataAnalysisMixin.plot_missing_values_heatmap(df, output_dir),
        ]

        # Return AnalysisResult with the summary and heatmap plot
        return AnalysisResult(summary, plot_paths)

    @staticmethod
    def plot_missing_values_heatmap(df: pd.DataFrame, output_dir: str) -> str:
        """Generates a heatmap showing missing values and saves it.

        Args:
            df (pd.DataFrame): The dataset to visualize.
            output_dir (str): The directory to save the heatmap.

        Returns:
            str: The path to the generated plot
        """
        if df.empty:
            logger.warning("⚠️ No data available for missing values heatmap.")
            return ""

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(df.isnull(), cmap="coolwarm", cbar=False, ax=ax)
        ax.set_title("Missing Values Heatmap")

        filename = "missing_values_heatmap.png"
        plot_path = os.path.join(output_dir, filename)
        fig.savefig(plot_path)
        plt.close(fig)

        if os.path.exists(plot_path):
            logger.info(f"✅ Missing values heatmap saved as {plot_path}")
            return plot_path
        else:
            logger.warning(f"❌ Failed to save heatmap at: {plot_path}")
            return ""
