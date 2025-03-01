import os
from datetime import datetime
import click
from redcap_eda.load_case_data import load_data
from redcap_eda.logger import logger, set_log_level
from redcap_eda.cast_schema import SchemaHandler
from redcap_eda.analysis.eda import ExploratoryDataAnalysis
from redcap_eda.unified_report import UnifiedReport


@click.group()
@click.option("--debug", is_flag=True, help="Enable verbose debug logging")
def cli(debug: bool) -> None:
    """Command-line interface for REDCap-EDA.

    This CLI tool loads REDCap datasets, applies schema casting,
    and performs exploratory data analysis.

    Args:
        debug (bool): Enables verbose logging if set.
    """
    set_log_level(debug)


@click.command()
@click.option(
    "--sample",
    is_flag=True,
    help="Use the default REDCap sample dataset (Case 01).",
)
@click.option(
    "--sample-schema",
    is_flag=True,
    help="Use the sample schema for the REDCap sample dataset (Case 01).",
)
@click.option(
    "--csv",
    type=click.Path(exists=True),
    help="Path to a user-provided CSV file.",
)
@click.option(
    "--schema",
    type=click.Path(exists=True),
    help="Path to a schema file (JSON/YAML).",
)
@click.option(
    "--output",
    default="eda_reports",
    help="Specify the directory to save reports.",
)
def analyze(
    sample: bool,
    sample_schema: bool,
    csv: str | None,
    schema: str | None,
    output: str,
) -> None:
    """Performs EDA on the specified dataset.

    Args:
        sample (bool): Use the predefined REDCap sample dataset.
        sample_schema (bool): Use the predefined sample schema.
        csv (str | None): Path to a user-provided dataset.
        schema (str | None): Path to a schema file.
        output (str): Directory to store analysis reports.
    """
    if csv and sample:
        logger.error("❌ Cannot specify both `--sample` and `--csv`. Choose one.")
        return

    if csv and sample_schema:
        logger.error(
            "❌ Cannot use `--sample-schema` and `--csv`. Pass a valid path to `--schema` or omit `--schema` to interactive create one.",
        )
        return

    if not csv and not sample:
        logger.error("❌ No dataset specified. Choose `--csv` or `--sample`")
        return

    # Ensure top-level directory exists
    os.makedirs(output, exist_ok=True)

    # Create a timestamped subdirectory for each run
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(output, f"eda_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)

    logger.info(f"📂 Using output directory: {output_dir}")

    dataset_source = "Sample Dataset" if sample else csv
    logger.info(f"📂 Dataset source: {dataset_source}")

    # Initialize UnifiedReport for capturing dataset metadata & results
    unified_report = UnifiedReport(
        output=output_dir,
        dataset_name=csv or "sample_dataset",
    )

    try:
        # Load the dataset
        df = load_data(sample=sample, csv_path=csv)

        # Check for sample-schema:
        if sample_schema:
            schema = "sample"

        # Capture dataset metadata for the title page
        title_page_content = {
            "source": dataset_source,
            "rows": df.shape[0],
            "columns": df.shape[1],
            "schema": f"Provided by: {schema}" if schema else "Created Interactively",
            "timestamp": datetime.utcnow().isoformat(),
        }

        # Feed the title page content to the UnifiedReport instance
        unified_report.load_title_page_content(title_page_content)

        # Initialize SchemaHandler
        schema_handler = SchemaHandler(schema)

        # Handle schema enforcement
        schema_handler.load_or_create_schema(df, csv_path=csv or "")

        # Capture df with applied schema datatypes and schema report
        df, schema_report = schema_handler.enforce_schema(df)

        # Feed the schema report to the UnifiedReport instance
        unified_report.load_schema_enforcement_page_content(schema_report)

        # Create an instance of ExploratoryDataAnalysis
        eda = ExploratoryDataAnalysis(
            df,
            output=output_dir,
            unified_report=unified_report,
        )

        # Trigger AnalysisReport objects to be fed to the UnifiedReport instance
        eda.explore()

        # Finalize Unified Report
        unified_report.finalize_section()

        # Trigger the UnifiedReport to create the PDF
        unified_report.export_to_pdf()

    except FileNotFoundError as e:
        logger.critical(f"❌ Dataset file not found: {e}")
    except ValueError as e:
        logger.warning(f"⚠️ Data integrity issue detected: {e}")
    except Exception as e:
        logger.exception(f"🚨 Unexpected error occurred: {e}")


@click.command()
def list_cases() -> None:
    """Lists available REDCap test cases."""
    logger.info("📂 Available test cases: ['01',]")


# Register CLI commands
cli.add_command(analyze)
cli.add_command(list_cases)

if __name__ == "__main__":
    cli()
