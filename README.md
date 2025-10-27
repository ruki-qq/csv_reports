# csv_reports

This project is for generating reports from CSV files.
It's currently supports average-rating report, though new reports can be added.

## Usage

```bash
poetry install
python main.py --files <paths_to_csv_files> --report <report_name>
```

## Examples

```bash
python main.py --files csv/products1.csv csv/products2.csv --report average-rating
```

## Testing

```bash
python -m pytest -vvv
```
