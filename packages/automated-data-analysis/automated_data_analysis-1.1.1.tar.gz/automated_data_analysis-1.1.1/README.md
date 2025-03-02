# automated_data_analysis

An automated data analysis pipeline package for efficient data processing and cleaning.

## Features

- Automated data loading (CSV/Excel)
- Duplicate removal
- Smart missing value handling
- Data format validation
- Statistical analysis
- Data accuracy checks
- Comprehensive terminal reporting

Check out the [example script](examples/example_usage.py) for more details.

## Usage Parameters
analyze_data() :
- file_path : Path to CSV/Excel file

- fill_strategy (optional) : Dictionary specifying filling strategies for columns

- stats_columns (optional) : List of columns for statistical analysis

- stats (optional)  : List of statistics to calculate (default: ['mean', 'median', 'std', 'min', 'max'])
## Dependency :
- pandas>=1.0.0
- numpy>=1.18.0
- openpyxl>=3.0.0

## Installation

```bash

pip install automated_data_analysis
