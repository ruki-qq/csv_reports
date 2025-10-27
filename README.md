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

## Screenshots

### Basic usage
![alt](https://files.catbox.moe/1lij66.png)

### Some error handling
![alt](https://files.catbox.moe/ari1tq.png)

![alt](https://files.catbox.moe/usmkkt.png)

### Multi-file usage
![alt](https://files.catbox.moe/ez7q54.png)

![alt](https://files.catbox.moe/sst2vr.png)
