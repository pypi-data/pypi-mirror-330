"""
📌 eda.py: Orchestrates Exploratory Data Analysis (EDA) for REDCap datasets.

🔹 **Purpose**:
    - Distributes analysis across multiple column types.
    - Uses **parallel execution** with `multiprocessing` for efficiency.
    - Tracks progress with `tqdm` for user feedback.
    - **Saves visualizations dynamically based on column data type**.

🔹 **Why Use Parallel Processing?**
    - REDCap datasets often have **hundreds of columns**.
    - **Single-threaded execution is slow**, especially for large datasets.
    - `multiprocessing.Pool` allows **CPU-bound tasks to run in parallel**.

🔹 **Example Usage**:
    ```python
    from redcap_eda.analysis.eda import ExploratoryDataAnalysis
    df, report = ExploratoryDataAnalysis(df, unireport).explore()
    ```
"""

import pandas as pd
import multiprocessing as mp
from tqdm import tqdm
from redcap_eda.logger import logger
from redcap_eda.unified_report import UnifiedReport
from redcap_eda.analysis.numerical.mixins import NumericalAnalysisMixin
from redcap_eda.analysis.categorical.mixins import CategoricalAnalysisMixin
from redcap_eda.analysis.text.mixins import TextAnalysisMixin
from redcap_eda.analysis.datetime.mixins import DatetimeAnalysisMixin
from redcap_eda.analysis.missing.mixins import MissingDataAnalysisMixin
from redcap_eda.analysis.lib import AnalysisResult
from redcap_eda.analysis.json_report_handler import JSONReportHandler


class ExploratoryDataAnalysis(
    NumericalAnalysisMixin,
    CategoricalAnalysisMixin,
    TextAnalysisMixin,
    DatetimeAnalysisMixin,
    MissingDataAnalysisMixin,
):
    """Performs Exploratory Data Analysis (EDA) on a DataFrame."""

    def __init__(self, df: pd.DataFrame, output: str, unified_report: UnifiedReport):
        self.df = df
        self.output = output
        self.unified_report = unified_report

    def analyze_column(self, col: str) -> tuple[AnalysisResult, dict[str, dict | str]]:
        """Analyze a single column and save visualizations.

        Args:
            col (str): Column name.

        Returns:
            dict[str, dict | str]: Column analysis result.
        """

        dtype = str(self.df[col].dtype)
        # Initialize a default AnalysisResult to avoid UnboundLocalError
        analysis_result: AnalysisResult = AnalysisResult(
            summary=(f"Analysis of {col}", {"error": "No analysis performed"}),
            plot_paths=[],
        )
        try:
            logger.debug(f"🔍 Column '{col}' detected as type '{dtype}'")

            match dtype:
                case "int64" | "float64":
                    analysis_result = super().numerical_summary(
                        self.df[col],
                        self.output,
                    )

                case "category":
                    analysis_result = super().categorize(self.df[col], self.output)

                case _ if "string" in dtype:  # handles string[python]
                    analysis_result = super().analyze_text(self.df[col], self.output)

                case _ if "datetime" in dtype:  # handles datetime64[ns]
                    analysis_result = super().analyze_datetime(
                        self.df[col],
                        self.output,
                    )

                case _:
                    return analysis_result, {
                        col: {"message": f"Skipped analysis for {dtype} columns"},
                    }

            analysis_result_json = {col: analysis_result.summary}

            return analysis_result, analysis_result_json

        except Exception as e:
            logger.error(f"❌ Error analyzing column {col}: {e}")
            return analysis_result, {col: {"error": str(e)}}  # Wrap errors in a dict

    def explore(self) -> dict[str, dict]:
        """Runs parallel EDA with optimized multiprocessing."""
        logger.info("🚀 Starting Exploratory Data Analysis...")

        # Analyze Missing Data
        if self.unified_report:
            missing_data_result = super().analyze_missing_data(self.df, self.output)
            self.unified_report.load_missing_values_page_content(missing_data_result)

        # Proceed with standard column analysis
        column_list = list(self.df.columns)
        num_workers = min(mp.cpu_count(), len(column_list))
        chunksize = max(1, len(column_list) // (num_workers * 2))

        # Initialize containers for unified report and json report
        json_data = {}

        with mp.Pool(num_workers) as pool:
            results = list(
                tqdm(
                    pool.imap(self.analyze_column, column_list, chunksize),
                    total=len(column_list),
                    desc="🔍 Analyzing Columns",
                    unit="col",
                ),
            )

        for analysis_result, analysis_result_json in results:
            # Load the UnifiedReport instance with AnalysisResult object
            if self.unified_report:
                self.unified_report.load_analysis_page_content(analysis_result)
            else:
                logger.warning(
                    "❌ Skipped loading AnalysisResult as UnifiedReport is not initialized.",
                )

            # Aggregate JSON data for JSONReportHandler
            json_data.update(analysis_result_json)

        # Use JSONReportHandler to handle JSON export
        json_report_handler = JSONReportHandler(self.output)
        json_report_handler.collect_results([json_data])
        json_report_handler.save_report(display=True)

        logger.info("✅ EDA Complete! Report saved.")
        return json_data
