"""
📌 NumericalAnalysisMixin: Analyzes numerical columns.

🔹 **Purpose**:
    - Computes summary statistics (mean, median, std, min, max, outliers).
    - Generates **histograms** and **boxplots** for visualization.
    - Supports **log scale** and **outlier visibility toggling**.
"""

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from redcap_eda.logger import logger
from redcap_eda.analysis.lib import AnalysisResult


class NumericalAnalysisMixin:
    """Mixin for numerical analysis."""

    __slots__ = ()

    @staticmethod
    def numerical_summary(series: pd.Series, output_dir: str) -> AnalysisResult:
        """Analyze numerical columns (int/float) & generate plots.

        Args:
            series (pd.Series): The numerical series to analyze.
            output_dir (str): The directory to save output files.

        Returns:
            AnalysisResult: Named tuple containing summary statistics and plots.
            #AnalysisResult = namedtuple("AnalysisResult", ["summary", "plots"])
        """
        if series.empty:
            logger.warning(f"⚠️ Skipping empty numerical column: {series.name}")
            return AnalysisResult(
                summary=("Numerical Analysis", {"error": "Column is empty"}),
                plot_paths=[],
            )

        # Compute summary statistics
        stats = {
            "mean": series.mean(),
            "median": series.median(),
            "std_dev": series.std(),
            "min": series.min(),
            "max": series.max(),
            "outliers": NumericalAnalysisMixin.detect_outliers(series),
        }

        summary = (f"Numerical Analysis of {series.name}", stats)

        # Generate plots (store file paths)
        plot_paths = [
            NumericalAnalysisMixin.plot_distribution(series, output_dir),
            NumericalAnalysisMixin.plot_boxplot(series, output_dir),
        ]

        return AnalysisResult(summary, plot_paths)

    @staticmethod
    def detect_outliers(series):
        """Detect outliers using the IQR method."""
        q1, q3 = series.quantile([0.25, 0.75])
        iqr = q3 - q1
        lower_bound, upper_bound = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        return series[(series < lower_bound) | (series > upper_bound)].tolist()

    @staticmethod
    def plot_distribution(series: pd.Series, output_dir: str) -> str:
        """Plots a histogram & KDE for numerical data and saves the file.

        Args:
            series (pd.Series): The numerical series to plot.

        Returns:
            str: The file path of the saved plot.
            output_dir (str): The directory to save the plot.
        """
        if series.empty:
            logger.warning(f"⚠️ No data available for histogram: {series.name}")
            return ""

        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(series, bins=20, kde=True, ax=ax)
        ax.set_title(f"Distribution of {series.name}")

        filename = f"{series.name}_distribution.png"
        plot_path = os.path.join(output_dir, filename)
        fig.savefig(plot_path)
        plt.close(fig)

        if os.path.exists(plot_path):
            logger.info(f"✅ Numerical Distribution Figure saved as {plot_path}")
            return plot_path
        else:
            logger.warning(
                f"❌ Failed to save Numerical Distribution Figure at: {plot_path}",
            )
            return ""

    @staticmethod
    def plot_boxplot(series: pd.Series, output_dir: str) -> str:
        """Plots a boxplot for numerical data and saves the file.

        Args:
            series (pd.Series): The numerical series to plot.

        Returns:
            str: The file path of the saved plot.
        """
        if series.empty:
            logger.warning(f"⚠️ No data available for boxplot: {series.name}")
            return ""

        fig, ax = plt.subplots(figsize=(4, 6))
        sns.boxplot(y=series, ax=ax)
        ax.set_title(f"Boxplot of {series.name}")

        filename = f"{series.name}_boxplot.png"
        plot_path = os.path.join(output_dir, filename)
        fig.savefig(plot_path)
        plt.close(fig)

        if os.path.exists(plot_path):
            logger.info(f"✅ Numerical boxplot saved as {plot_path}")
            return plot_path
        else:
            logger.warning(f"❌ Failed to save Numerical boxplot at: {plot_path}")
            return ""
