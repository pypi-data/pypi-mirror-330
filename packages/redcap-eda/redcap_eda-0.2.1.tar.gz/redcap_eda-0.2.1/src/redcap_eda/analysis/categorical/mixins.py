"""
📌 CategoricalAnalysisMixin: Analyzes categorical columns.

🔹 **Purpose**:
    - Computes **category counts** and **proportions**.
    - Identifies **most/least frequent categories**.
    - Generates **bar plots** for category distribution.
"""

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from redcap_eda.logger import logger
from redcap_eda.analysis.lib import AnalysisResult


class CategoricalAnalysisMixin:
    """Mixin for categorical column analysis."""

    __slots__ = ()

    @staticmethod
    def categorize(series: pd.Series, output_dir: str) -> AnalysisResult:
        """Analyzes categorical columns.

        Args:
            series (pd.Series): The categorical series to analyze.
            output_dir (str): The directory to save output files.

        Returns:
            AnalysisResult: Named tuple containing summary statistics and plot_paths.
            #AnalysisResult = namedtuple("AnalysisResult", ["summary", "plot_paths"])
        """
        if series.empty:
            logger.warning(f"⚠️ Skipping empty categorical column: {series.name}")
            return AnalysisResult(
                summary=("Categorical Analysis", {"error": "Column is empty"}),
                plot_paths=[],
            )

        category_counts = series.value_counts()

        stats = {
            "unique_values": series.nunique(),
            "missing_values": series.isnull().sum(),
            "mode": category_counts.idxmax() if not category_counts.empty else None,
            "most_frequent": category_counts.idxmax()
            if not category_counts.empty
            else None,
            "least_frequent": category_counts.idxmin()
            if not category_counts.empty
            else None,
            "category_counts": category_counts.to_dict(),
            "category_proportions": (category_counts / len(series)).to_dict(),
        }

        summary = (f"Categorical Analysis of {series.name}", stats)

        plot_paths = [
            CategoricalAnalysisMixin.plot_category_distribution(series, output_dir),
        ]

        return AnalysisResult(summary, plot_paths)

    @staticmethod
    def plot_category_distribution(series: pd.Series, output_dir) -> str:
        """Creates a bar plot for categorical data.

        Args:
            series (pd.Series): The categorical series to plot.
            output_dir (str): The directory to save the plot.

        Returns:
            str: The path to the saved figure.
        """
        if series.empty:
            logger.warning(
                f"⚠️ No data available for category distribution: {series.name}",
            )
            return ""

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.countplot(y=series, order=series.value_counts().index, ax=ax)
        ax.set_title(f"Category Distribution of {series.name}")

        filename = f"{series.name}_category_distribution.png"
        plot_path = os.path.join(output_dir, filename)
        fig.savefig(plot_path)
        plt.close(fig)

        if os.path.exists(plot_path):
            logger.info(f"✅ Category Distribution saved as {plot_path}")
            return plot_path
        else:
            logger.warning(f"❌ Failed to save Category Distribution at: {plot_path}")
            return ""
