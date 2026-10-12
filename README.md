
# Data Quality Detective

A lightweight Python tool for profiling datasets, detecting data quality issues, and generating reproducible reports.

## Overview

Data Quality Detective helps analysts identify potential data quality problems before using a dataset for analysis or reporting.

The project uses Python and pandas to calculate quality metrics, apply validation rules, and export structured reports for further inspection.

## Features

- **Data profiling:** data types, missing values, missing-value percentages, and unique values by column.
- **Dataset summary:** row count, column count, missing cells, and exact duplicate rows.
- **Rule-based validation:** detects non-numeric ages, ages outside a configurable example range, and negative monthly spending.
- **Issue reporting:** records the affected row, customer ID, column, rule, severity, and observed value.
- **Report generation:** exports summary metrics, column profiles, validation issues, and issue counts to CSV.
- **Basic validation tests:** checks expected results on a synthetic dataset.

## Tech Stack

- Python
- pandas
- Jupyter Notebook / Google Colab

## Project Structure

```text
data-quality-detective/
├── data/
│   └── sample_customers.csv
├── reports/
│   ├── quality_summary.csv
│   ├── quality_profile.csv
│   ├── quality_issues.csv
│   └── quality_issue_summary.csv
├── data_quality.py
├── data-quality-detective.ipynb
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Load the sample dataset

```python
import pandas as pd
import data_quality as dq

df = pd.read_csv("data/sample_customers.csv")
```

### 3. Generate the reports

```python
results = dq.generate_reports(df)

print(results["summary"])
display(results["issues"])
display(results["issue_summary"])
```

The generated CSV reports are saved in the `reports/` directory by default.

## Example Validation Rules

| Rule | Description | Severity |
|---|---|---|
| `AGE_NOT_NUMERIC` | Age is present but cannot be interpreted as a number | High |
| `AGE_OUT_OF_RANGE` | Age falls outside the example range of 0–100 | High |
| `NEGATIVE_SPENDING` | Monthly spending is negative | Medium |

These rules are examples designed for the included synthetic customer dataset. They should be adapted to the business context and data dictionary of each real dataset.

## Output Reports

- `quality_summary.csv`: overall dataset metrics.
- `quality_profile.csv`: data quality metrics for each column.
- `quality_issues.csv`: individual validation issues and affected records.
- `quality_issue_summary.csv`: issue counts by rule and severity.

## Limitations

- The current validation rules are specific to the sample customer dataset.
- Missing values are profiled separately and are not yet included in the validation issue list.
- Duplicate rows are reported as a dataset-level metric rather than individual validation issues.
- The tool flags potential problems; it does not automatically modify or clean the source data.
- The current version accepts an existing pandas DataFrame. Direct CSV ingestion and real-world data sources will be expanded in future iterations.

## Future Improvements

- Support configurable validation rules.
- Add CSV ingestion and schema checks.
- Integrate public data sources and HTML table extraction.
- Improve test coverage and reporting.
- Add visual summaries of data quality metrics.

## Author

Created as a portfolio project to demonstrate practical Python, pandas, data profiling, validation, and reporting skills.
