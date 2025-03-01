# REDCap-EDA

![CI Status](https://github.com/robertp/REDCap-EDA/actions/workflows/ci.yaml/badge.svg)

## 📌 Overview
REDCap-EDA is a command-line tool for performing **Exploratory Data Analysis (EDA)** on **REDCap datasets**. It automates data inspection, schema enforcement, statistical analysis, visualization, and report generation.

## 🚀 Features
- ✅ **Automatic Data Type Enforcement** (casts columns based on a predefined or user-defined schema)
- 📊 **Summary Statistics** (mean, median, std dev, outliers, categorical distributions)
- 📉 **Visualizations** (histograms, box plots, categorical distributions, time trends, word clouds)
- 📂 **Comprehensive PDF Report Generation** with **UnifiedReport**
- 🔄 **Multiprocessing for Faster Execution**
- 🔍 **Progress Bars with `tqdm`**
- 📂 **Exports Reports** (JSON, PDF, and saved visualizations)
- 📝 **Interactive Schema Creation** for custom datasets

## 📦 Installation
```bash
pip install redcap-eda
```

## 🛠️ Usage

### 🔹 Example Using the Sample Dataset and Interactive Schema Creation
```bash
redcap-eda analyze --sample
```

### 🔹 Example Using the Sample Dataset with a Predefined Schema
```bash
redcap-eda analyze --sample --sample-schema
```

### 🔹 Running EDA on a Custom Dataset with Interactive Schema Creation
```bash
redcap-eda analyze --csv path/to/your_data.csv
```

### 🔹 Running EDA on a Custom Dataset with a Predefined Schema
```bash
redcap-eda analyze --csv path/to/your_data.csv --schema path/to/schema.json
```

### 🔹 Running in Debug Mode
```bash
redcap-eda --debug analyze --sample
```

### 🔹 Listing Available Test Cases
```bash
redcap-eda list-cases
```

## 📂 Project Structure
```bash
.
├── Makefile                # Helper commands
├── README.md               # Project documentation
├── dist                    # Distribution files for PyPI
├── mypy.ini                # Type checking configuration
├── poetry.lock             # Poetry dependency lock file
├── pyproject.toml          # Poetry project configuration
├── schemas                 # Saved schema files
│   └── schema_sample_dataset.json
├── src
│   ├── logs
│   │   └── redcap_eda.log  # Log files
│   └── redcap_eda
│       ├── analysis        # EDA analysis modules
│       │   ├── categorical
│       │   │   └── mixins.py # Categorical data analysis
│       │   ├── datetime
│       │   │   └── mixins.py # Datetime data analysis
│       │   ├── eda.py      # Main EDA module
│       │   ├── json_report_handler.py # JSON export utility
│       │   ├── lib.py       # Shared data structures (e.g., AnalysisResult)
│       │   ├── missing
│       │   │   └── mixins.py # Missing data analysis
│       │   ├── numerical
│       │   │   └── mixins.py # Numerical data analysis
│       │   └── text
│       │       └── mixins.py # Text data analysis
│       ├── cast_schema.py  # Schema enforcement
│       ├── cli.py          # Command-line interface
│       ├── load_case_data.py # Dataset loader
│       ├── logger.py       # Logging utilities
│       └── unified_report.py # PDF report generation
└── tests                   # Unit tests
    ├── __init__.py
    └── fixtures
        └── toy_data.csv    # Sample test data
```

## 📝 Contributing
1. **Fork the repository** and create a feature branch.
2. **Run tests** to ensure code integrity:
   ```bash
   poetry run pytest tests/
   ```
3. **Submit a pull request** with a detailed description.

## 📜 License
This project is licensed under the **MIT License**.

## 🤝 Acknowledgments
- [REDCap](https://projectredcap.org/) for enabling structured data collection.
- The **Open Source Community** for inspiration & contributions!
