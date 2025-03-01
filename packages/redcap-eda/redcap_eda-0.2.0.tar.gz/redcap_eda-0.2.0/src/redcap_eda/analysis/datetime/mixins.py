"""
📌 DatetimeAnalysisMixin: Analyzes datetime columns.

🔹 **Purpose**:
    - Computes time-based statistics.
    - Extracts meaningful datetime features (year, month, weekday, hour).
    - Generates visualizations for time-based trends.

🔹 **Example Usage**:
    ```python
    from redcap_eda.analysis.datetime.mixins import DatetimeAnalysisMixin
    class MyClass(DatetimeAnalysisMixin):
        pass
    obj = MyClass()
    obj.analyze_datetime(df["timestamp_column"])
    ```
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from redcap_eda.logger import logger
from redcap_eda.analysis.lib import AnalysisResult


class DatetimeAnalysisMixin:
    """Mixin for datetime analysis."""

    __slots__ = ()

    @staticmethod
    def analyze_datetime(series: pd.Series, output_dir: str) -> AnalysisResult:
        """Analyzes datetime columns & generates time-based visualizations.

        Args:
            series (pd.Series): The datetime series to analyze.
            output_dir (str): The directory to save the plot.

        Returns:
            AnalysisResult: Named tuple containing summary statistics and plot_paths.
        """
        logger.debug(f"🕒 Analyzing datetime column: {series.name}")

        if series.empty:
            logger.warning(f"⚠️ Skipping empty datetime column: {series.name}")
            return AnalysisResult(
                summary={"error": "Column is empty"},
                plot_paths=[],
            )

        if not pd.api.types.is_datetime64_any_dtype(series):
            logger.warning(f"⚠️ Column {series.name} is not a datetime type.")
            return AnalysisResult(
                summary={"error": "Not a valid datetime column"},
                plot_paths=[],
            )

        # Compute summary statistics
        stats = {
            "earliest": series.min(),
            "latest": series.max(),
            "time_span": str(series.max() - series.min()),
            "missing_values": series.isnull().sum(),
            "year_counts": series.dt.year.value_counts().to_dict(),
            "month_counts": series.dt.month.value_counts().to_dict(),
            "weekday_counts": series.dt.day_name().value_counts().to_dict(),
            "hour_counts": series.dt.hour.value_counts().to_dict(),
        }

        summary = (f"Datetime Analysis of {series.name}", stats)

        # Generate plots
        plot_paths = [
            DatetimeAnalysisMixin.plot_datetime_distribution(series, output_dir),
            DatetimeAnalysisMixin.plot_time_trend(series, output_dir),
        ]

        return AnalysisResult(summary, plot_paths)

    @staticmethod
    def plot_datetime_distribution(series: pd.Series, output_dir: str) -> str:
        """Plots a histogram of datetime values.

        Args:
            series (pd.Series): The datetime series to plot.
            output_dir (str): The directory to save the plot.

        Returns:
            str: the file path to the saved figure
        """
        if series.empty:
            logger.warning(
                f"⚠️ No data available for datetime distribution: {series.name}",
            )
            return ""

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(series, bins=30, kde=True, ax=ax, color="blue")
        ax.set_title(f"Datetime Distribution of {series.name}")
        ax.set_xlabel("Timestamp")
        ax.set_ylabel("Frequency")

        filename = f"{series.name}_datetime_distribution.png"
        plot_path = os.path.join(output_dir, filename)
        fig.savefig(plot_path)
        plt.close(fig)

        if os.path.exists(plot_path):
            logger.info(f"✅ Datetime Distribution saved as {plot_path}")
            return plot_path
        else:
            logger.warning(f"❌ Failed to save Datetime Distribution at: {plot_path}")
            return ""

    @staticmethod
    def plot_time_trend(series: pd.Series, output_dir: str) -> str:
        """Plots a line chart showing time-based trends.

        Args:
            series (pd.Series): The datetime series to plot.
            output_dir (str): The directory to save the plot.

        Returns:
            str: the file path to the saved figure
        """
        if series.empty:
            logger.warning(f"⚠️ No data available for time trend: {series.name}")
            return ""

        df = pd.DataFrame({series.name: series})
        df = df.set_index(series.name)
        df["count"] = 1
        df = df.resample("D").sum()
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df.index, df["count"], marker="o", linestyle="-", color="blue")
        ax.set_title(f"Time Trend of {series.name}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Count of Records")
        ax.grid()

        filename = f"{series.name}_time_trend.png"
        plot_path = os.path.join(output_dir, filename)
        fig.savefig(plot_path)
        plt.close(fig)

        if os.path.exists(plot_path):
            logger.info(f"✅ Time trend saved as {plot_path}")
            return plot_path
        else:
            logger.warning(f"❌ Failed to save Time trend at: {plot_path}")
            return ""
