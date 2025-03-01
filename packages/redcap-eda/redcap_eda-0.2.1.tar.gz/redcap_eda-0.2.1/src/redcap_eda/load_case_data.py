import pandas as pd
import requests
from redcap_eda.logger import logger

"""
Handles loading datasets for REDCap-EDA.

Supports:
- Fetching the predefined sample dataset (`records_api` from Case 01).
- Loading user-provided CSV files via CLI.
"""


def load_data(sample: bool = True, csv_path: str | None = None) -> pd.DataFrame:
    """
    Load a dataset either from a user-provided CSV or the REDCap test dataset.

    Args:
        sample (bool): Whether to load the default REDCap sample dataset.
        user_input (str | None): Path to a user-specified CSV file.

    Returns:
        pd.DataFrame: The loaded dataset.

    Raises:
        ValueError: If no valid data source is provided.
        RuntimeError: If the dataset fails to load.
    """
    if csv_path:
        logger.info(f"📂 Loading user-provided dataset: {csv_path}")
        try:
            df = pd.read_csv(csv_path)
            if df.empty:
                raise ValueError(f"❌ Provided dataset '{csv_path}' is empty.")
            logger.info(f"✅ Successfully loaded user dataset from {csv_path}")
            return df
        except FileNotFoundError:
            logger.error(f"❌ File '{csv_path}' not found.")
            raise ValueError(f"File '{csv_path}' does not exist.")
        except pd.errors.ParserError as e:
            logger.error(f"❌ Failed to parse CSV '{csv_path}': {e}")
            raise RuntimeError(f"Failed to parse '{csv_path}': {e}")

    if sample:
        # Base URL for predefined test dataset
        SAMPLE_DATA_URL = "https://raw.githubusercontent.com/redcap-tools/redcap-test-datasets/master/case-01/test-case-01-records-api.csv"
        logger.info(f"🔄 Fetching default sample dataset: {SAMPLE_DATA_URL}")

        try:
            df = pd.read_csv(SAMPLE_DATA_URL)
            if df.empty:
                raise ValueError("❌ Sample dataset is empty.")
            logger.info("✅ Successfully loaded REDCap sample dataset.")
            return df
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to fetch sample dataset: {e}")
            raise RuntimeError(f"Failed to fetch sample dataset: {e}")
        except pd.errors.ParserError as e:
            logger.error(f"❌ Failed to parse sample dataset: {e}")
            raise RuntimeError(f"Failed to parse sample dataset: {e}")

    # If neither user input nor sample dataset is available, raise an error
    raise ValueError(
        "❌ No data source specified. Use either `sample=True` or provide `csv_path`.",
    )
