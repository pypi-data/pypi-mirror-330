"""
📌 unified_report.py: Aggregates and compiles the Unified EDA Report in PDF format.

🔹 **Purpose**:
    - Centralized reporting structure for **Exploratory Data Analysis (EDA)**.
    - Aggregates dataset metadata, schema enforcement, missing values, and analysis results.
    - Uses `matplotlib.backends.backend_pdf.PdfPages` for structured multi-page reports.

🔹 **Example Usage**:
    ```python
    report = UnifiedReport(output_dir="eda_reports", dataset_name="sample.csv")
    report.add_title_page()
    report.add_schema_enforcement_page(schema_report)
    report.add_missing_values_page(missing_values_summary, missing_values_heatmap)
    report.add_column_summary("Age", column_summary)
    report.add_column_visual("Age", "eda_reports/histogram_age.png")
    report.export_to_pdf()
    ```
"""

import os
from typing import Any
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
from redcap_eda.logger import logger
from redcap_eda.analysis.lib import AnalysisResult


class UnifiedReport:
    """Handles compilation and export of the Exploratory Data Analysis (EDA) PDF report."""

    def __init__(self, output: str, dataset_name: str):
        """
        Initializes the UnifiedReport.

        Args:
            output (str): Directory to save the final PDF report.
            dataset_name (str): Name of the dataset being analyzed.
        """
        self.output = output
        self.dataset_name = os.path.basename(
            dataset_name,
        )  # TODO is this redundant due to cli.py title_page_content
        self.title_page: dict[str, Any] = {}
        self.schema_page: dict[str, Any] = {}
        self.missing_values_pages: AnalysisResult = AnalysisResult(
            summary=("Missing Values Summary", {}),
            plot_paths=[],
        )
        self.analysis_pages: list[AnalysisResult] = []
        self.pdf_path = os.path.join(
            output,
            f"eda_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        )
        self.pdf_pages = PdfPages(self.pdf_path)

    def load_title_page_content(self, content: dict):
        """
        Load the instance with title content page content

        Args:
            dataset_info (dict): General dataset information, e.g., row count, column count.
        """
        required_keys = {"source", "rows", "columns", "schema", "timestamp"}

        if not all(key in content for key in required_keys):
            raise ValueError(
                f"❌ Missing required title page keys: {required_keys - content.keys()}",
            )

        self.title_page = content

    def load_schema_enforcement_page_content(self, schema_report: pd.DataFrame):
        """
        Load the instance with the schema page content

        Args:
            schema_report (pd.DataFrame): DataFrame containing before-and-after data types.
        """
        if not isinstance(schema_report, pd.DataFrame):
            raise TypeError("❌ Expected schema_report to be a DataFrame.")

        self.schema_page = schema_report

    def load_missing_values_page_content(self, analysis_result: AnalysisResult):
        """
        Load the instance with missing values page content
        """

        if not isinstance(analysis_result, AnalysisResult):
            raise TypeError("❌ Expected analysis_result to be an AnalysisResult.")

        result_title, _ = analysis_result.summary
        logger.debug(f"loading UnifiedReport with AnalysisResult: {result_title}")

        self.missing_values_analysis_pages = analysis_result

    def load_analysis_page_content(self, analysis_result: AnalysisResult):
        """
        Load the instance with an AnalysisResult object
        """
        if not isinstance(analysis_result, AnalysisResult):
            raise TypeError("❌ Expected analysis_result to be an AnalysisResult.")

        result_title, _ = analysis_result.summary
        logger.debug(f"loading UnifiedReport with AnalysisResult: {result_title}")

        self.analysis_pages.append(analysis_result)
        logger.debug(f"Total Analysis Pages Loaded: {len(self.analysis_pages)}")

    def finalize_section(self):
        """Finalizes the aggregation of report sections before PDF export."""
        logger.info("✅ Finalizing report sections.")

    def export_to_pdf(self):
        """Exports all collected report sections into a structured PDF."""
        logger.info(f"📄 Exporting report to {self.pdf_path}")

        # Create page 1: title page
        self._create_title_page()

        # Create page 2:  Schema Enforcement Page
        self._create_schema_page()

        # Create page 3: Missing Values Page
        self._create_missing_values_page()

        # Create remaining pages: One Page per Column
        self._create_analysis_pages()

        self.pdf_pages.close()
        logger.info(f"✅ Unified EDA Report saved: {self.pdf_path}")

    def _create_title_page(self):
        """Generates the title page for the PDF report."""
        content: dict[str, Any] = self.title_page

        fig, ax = plt.subplots(figsize=(8.5, 11))

        ax.text(
            0.5,
            0.8,
            "Exploratory Data Analysis Report",
            fontsize=20,
            ha="center",
            fontweight="bold",
        )
        ax.text(
            0.5,
            0.7,
            f"Generated on: {content['timestamp']}",
            fontsize=12,
            ha="center",
        )
        ax.text(0.5, 0.6, "Generated by: REDCap-EDA", fontsize=12, ha="center")
        ax.text(0.5, 0.5, f"Data Source: {content['source']}", fontsize=14, ha="center")
        ax.text(
            0.5,
            0.4,
            f"Datatype Schema: {content['schema']}",
            fontsize=12,
            ha="center",
        )

        ax.text(
            0.5,
            0.35,
            f"Number of Rows: {content['rows']}",
            fontsize=12,
            ha="center",
        )
        ax.text(
            0.5,
            0.3,
            f"Number of Columns: {content['columns']}",
            fontsize=12,
            ha="center",
        )

        ax.axis("off")
        self.pdf_pages.savefig(fig)
        plt.close(fig)

    def _create_schema_page(self):
        """Generates the schema enforcement results page in a tabular format."""
        results: pd.DataFrame = self.schema_page

        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis("tight")
        ax.axis("off")

        # Create a table
        table = ax.table(
            cellText=results.values,
            colLabels=results.columns,
            rowLabels=results.index,
            cellLoc="center",
            loc="center",
        )

        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.auto_set_column_width([0, 1])  # Adjust column width

        # 🔹 Increase row height to reduce table crowding
        # for key, cell in table.get_celld().items():
        # cell.set_height(0.1)  # Adjust row height

        ax.set_title("Data Type Conversion Summary", fontsize=16, fontweight="bold")
        self.pdf_pages.savefig(fig)
        plt.close(fig)

    def _create_missing_values_page(self):
        """Generates the missing values analysis page."""
        logger.debug("🚦 Generating Missing Values Page in the PDF")

        # Retrieve the stored content
        results = self.missing_values_pages
        summary, plot_paths = results.summary, results.plot_paths

        # Unpack summary data
        title, stats = summary
        logger.debug(f"📝 Creating Missing Values Summary Page: {title}")

        # 📝 Create the summary page as a table
        # fig, ax = plt.subplots(figsize=(8.5, 11))
        # ax.axis('tight')
        # ax.axis('off')

        # Convert report to a tabular format
        # sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
        # table_data = [[col, f'{missing_count} missing'] for col, missing_count in sorted_stats]
        # col_labels = ['Column', 'Missing Values']

        # table = ax.table(
        #    cellText=table_data,
        #    colLabels=col_labels,
        #    cellLoc='center',
        #    loc='center',
        # )

        # table.auto_set_font_size(False)
        # table.set_fontsize(12)
        # table.auto_set_column_width([0, 1])  # Adjust column width

        # ax.set_title('Missing Values Summary', fontsize=16, fontweight='bold')
        # self.pdf_pages.savefig(fig)
        # plt.close(fig)

        if not plot_paths:
            logger.warning(f"❌ No plots available for {title}.")
            return

        # 🖼️ Create a page for each saved plot image
        for plot_path in plot_paths:
            if os.path.exists(plot_path):
                fig, ax = plt.subplots(figsize=(8.5, 11))
                try:
                    img = plt.imread(plot_path)
                    ax.imshow(img, aspect="auto")
                    ax.axis("off")
                    ax.set_position(
                        (0.1, 0.1, 0.8, 0.8),
                    )  # Center the image with margins
                    self.pdf_pages.savefig(fig)
                    plt.close(fig)
                    logger.debug(f"🖼️ Plot added to PDF: {plot_path}")
                except Exception as e:
                    logger.error(
                        f"❌ Failed to load figure at: {plot_path}. Error: {e}",
                    )
            else:
                logger.warning(f"❌ Expected figure not found at: {plot_path}")

    def _create_analysis_pages(self):
        """Generates individual column analysis pages."""
        logger.debug("🚦 Generating Analysis Pages in the PDF")

        for result in self.analysis_pages:
            # unpack the AnalysisResult:
            summary, plot_paths = result.summary, result.plot_paths

            # unpack the summary:
            title, stats = summary
            logger.debug(f"📝 Creating Analysis Page for: {title}")

            # create the summary page
            fig, ax = plt.subplots(figsize=(8.5, 11))
            ax.axis("off")

            ax.text(
                0.5,
                0.9,
                f"Column Analysis: {title}",
                fontsize=16,
                ha="center",
                fontweight="bold",
            )

            y_pos = 0.8
            for key, value in stats.items():
                ax.text(0.1, y_pos, f"{key}: {value}", fontsize=12, va="top")
                y_pos -= 0.03

            self.pdf_pages.savefig(fig)
            plt.close(fig)

            if not plot_paths:
                logger.warning(f"❌ No plots available for {title}.")
                continue

            # 🖼️ Create a page for each saved plot image
            for plot_path in plot_paths:
                if os.path.exists(plot_path):
                    fig, ax = plt.subplots(figsize=(8.5, 11))
                    try:
                        img = plt.imread(plot_path)
                        ax.imshow(img, aspect="auto")
                        ax.axis("off")
                        self.pdf_pages.savefig(fig)
                        plt.close(fig)
                        logger.debug(f"🖼️ Plot added to PDF: {plot_path}")
                    except Exception:
                        logger.error(f"❌ Expected figure not found at: {plot_path}")
