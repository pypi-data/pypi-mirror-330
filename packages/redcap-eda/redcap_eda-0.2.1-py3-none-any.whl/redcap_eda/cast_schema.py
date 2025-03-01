import os
import json
import yaml
import datetime
import pandas as pd
from redcap_eda.logger import logger

"""
📌 SchemaHandler: Manages schema enforcement and interactive schema creation for REDCap-EDA.

🔹 **Capabilities**:
    - Loads schema from JSON or YAML.
    - Interactively creates a schema if none is provided.
    - Enforces schema on a DataFrame to ensure correct data types.

🔹 **Example Usage**:
    ```python
    schema_handler = SchemaHandler()
    schema_handler.load_or_create_schema(df)
    df, report = schema_handler.enforce_schema(df)
    ```
"""


class SchemaHandler:
    """Handles schema enforcement and interactive schema creation."""

    DTYPE_OPTIONS = {
        "int64": "Whole numbers (e.g., 1, 2, 3). No decimals.",
        "float64": "Decimal numbers (e.g., 3.14, 42.0, -0.99).",
        "bool": "True/False or Yes/No values.",
        "string": "Text data (e.g., names, emails, IDs).",
        "category": "Limited set of unique labels (e.g., Male/Female, Small/Medium/Large).",
        "datetime64[ns]": "Timestamps or dates (e.g., 2024-02-17, 12:30 PM).",
        "timedelta64[ns]": "Time differences (e.g., 5 days, 3 hours).",
        "object": "Mixed data types, unstructured text, or complex objects.",
    }

    SAMPLE_SCHEMA = {
        "record_id": "int64",
        "unvalidated_text": "string",
        "date_dmy": "datetime64[ns]",
        "date_mdy": "datetime64[ns]",
        "date_ymd": "datetime64[ns]",
        "datetime_dmyhm": "datetime64[ns]",
        "datetime_mdyhm": "datetime64[ns]",
        "datetime_ymdhm": "datetime64[ns]",
        "datetime_dmyhms": "datetime64[ns]",
        "datetime_mdyhms": "datetime64[ns]",
        "datetime_ymdhms": "datetime64[ns]",
        "email": "string",
        "integer": "int64",
        "number": "float64",
        "phone": "string",
        "time": "datetime64[ns]",
        "zip": "int64",
        "notes": "string",
        "calculated": "float64",
        "dropdown_numeric": "int64",
        "dropdown_character": "category",
        "dropdown_mixed": "category",
        "radio_buttons": "int64",
        "checkbox___1": "category",
        "checkbox___2": "category",
        "checkbox___3": "category",
        "yes_no": "bool",
        "true_false": "bool",
        "signature_draw": "object",
        "file_upload": "object",
        "slider": "int64",
    }

    def __init__(self, schema_path: str | None = None):
        """
        Initializes SchemaHandler.

        Args:
            schema_path (str, optional): Path to an existing schema file (JSON/YAML).
        """
        self.schema_path = schema_path
        self.schema: dict[str, str] = {}

    def load_schema(self) -> dict:
        """
        Loads a schema from a JSON or YAML file.

        Returns:
            dict: The loaded schema.

        Raises:
            ValueError: If the file format is unsupported or fails to load.
        """
        if not self.schema_path:
            logger.warning("⚠️ No schema provided. Proceeding without type enforcement.")
            return {}

        try:
            if self.schema_path.endswith(".json"):
                with open(self.schema_path) as f:
                    self.schema = json.load(f)
            elif self.schema_path.endswith((".yaml", ".yml")):
                with open(self.schema_path) as f:
                    self.schema = yaml.safe_load(f)
            else:
                raise ValueError(f"Unsupported schema format: {self.schema_path}")

            logger.info(f"📥 Loaded schema from {self.schema_path}")
            return self.schema

        except (FileNotFoundError, json.JSONDecodeError, yaml.YAMLError) as e:
            logger.error(f"❌ Failed to load schema from {self.schema_path}: {e}")
            raise ValueError(f"Invalid schema file: {e}")

    def enforce_schema(self, df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
        """
        Applies a schema to a DataFrame for data type enforcement.

        Args:
            df (pd.DataFrame): The dataset to process.

        Returns:
            tuple[pd.DataFrame, dict]: The updated DataFrame and a report of conversions.

        Raises:
            ValueError: If the schema is invalid.
        """
        if not self.schema:
            logger.warning(
                "⚠️ No schema available. Proceeding without data type enforcement.",
            )
            return df, {}

        before_types = df.dtypes.copy()  # Capture data types before conversion
        conversion_report = {}

        for column, dtype in self.schema.items():
            if column in df.columns:
                try:
                    df[column] = df[column].astype(dtype)
                    conversion_report[column] = (
                        before_types[column],
                        dtype,
                    )  # Store changes
                except ValueError as e:
                    logger.warning(f"⚠️ Failed to convert {column} to {dtype}: {e}")
                    conversion_report[column] = (
                        before_types[column],
                        "Conversion Failed",
                    )

        # Convert the report to a structured DataFrame
        schema_report = pd.DataFrame.from_dict(
            conversion_report,
            orient="index",
            columns=["Before", "After"],
        )

        return df, schema_report

    def create_interactive_schema(
        self,
        df: pd.DataFrame,
        csv_path: str | None = None,
        output_dir: str = "schemas",
    ) -> str:
        """
        Interactive prompt to define and save a schema.

        Args:
            df (pd.DataFrame): The dataset to analyze.
            csv_path (str, optional): Path to the CSV file (used for naming the schema).
            output_dir (str, optional): Directory to save the schema.

        Returns:
            str: The path to the saved schema file.
        """
        logger.info(
            "📝 Interactive Schema Creation: Define data types for each column.",
        )

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Determine recommended filename based on CSV name
        if csv_path:
            base_name = os.path.splitext(os.path.basename(csv_path))[
                0
            ]  # Extract "mydata" from "mydata.csv"
            suggested_filename = f"{output_dir}/{base_name}.json"
        else:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            suggested_filename = f"{output_dir}/schema_{timestamp}.json"

        # Ask user to confirm or modify the filename
        print(f"\n💾 Recommended schema filename: {suggested_filename}")
        custom_filename = input(
            "Press Enter to accept or provide a new filename: ",
        ).strip()
        schema_filename = custom_filename if custom_filename else suggested_filename

        # Collect column type choices
        self.schema = {}
        for column in df.columns:
            print(f"\n📌 Column: {column}")
            print(f"   🔍 Detected Type: {df[column].dtype}")
            print("   🔽 Choose a data type:")

            for i, (dtype, hint) in enumerate(self.DTYPE_OPTIONS.items(), 1):
                print(f"   {i}. {dtype} → {hint}")

            while True:
                choice = input(
                    "   ➤ Enter number (press Enter to keep detected type): ",
                ).strip()
                if choice.isdigit() and 1 <= int(choice) <= len(self.DTYPE_OPTIONS):
                    self.schema[column] = list(self.DTYPE_OPTIONS.keys())[
                        int(choice) - 1
                    ]
                    break
                elif choice == "":
                    self.schema[column] = str(df[column].dtype)
                    break
                else:
                    print("   ❌ Invalid choice. Please enter a valid number.")

        # Save the schema
        with open(schema_filename, "w") as f:
            json.dump(self.schema, f, indent=4)

        logger.info(f"✅ Schema saved as {schema_filename}")
        return schema_filename

    def load_or_create_schema(
        self,
        df: pd.DataFrame,
        csv_path: str | None = None,
    ) -> str:
        """
        Loads an existing schema or prompts for interactive creation.

        Args:
            df (pd.DataFrame): The dataset to analyze.
            csv_path (str, optional): Path to the CSV file (used for schema naming).

        Returns:
            str: The schema file path.
        """
        if self.schema_path == "sample":
            logger.info("📥 Using built-in SAMPLE_SCHEMA")
            self.schema = self.SAMPLE_SCHEMA
            return self.schema_path
        if self.schema_path and os.path.exists(self.schema_path):
            logger.info(f"📥 Loading schema from {self.schema_path}")
            self.load_schema()
            return self.schema_path
        else:
            logger.warning(
                "⚠️ No existing schema found. Launching interactive schema creation.",
            )
            return self.create_interactive_schema(df, csv_path)


# Example Usage:
# schema_handler = SchemaHandler("path/to/schema.json")  # Provide schema path if available
# schema_handler.load_or_create_schema(df)
# df, report = schema_handler.enforce_schema(df)
