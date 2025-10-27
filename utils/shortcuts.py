import csv
from pathlib import Path
from typing import Any

from rich import box
from rich.table import Table

from .logger import get_logger

logger = get_logger(__name__)


class CsvReader:
    def __init__(self, file: Path):
        self.file = file

    @property
    def check_csv_file(self) -> (bool, str):
        logger.debug(f"Checking CSV file: {self.file}")

        if not self.file.is_file():
            error_msg = f"File {self.file} does not exist!"
            return False, error_msg

        if not self.file.suffix == ".csv":
            error_msg = f"File {self.file} is not a CSV file!"
            return False, error_msg

        try:
            with open(self.file, "r", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile, delimiter=",")
                header = next(reader)
                header_count = len(header)
                rows = list(reader)

                if len(rows) == 0:
                    error_msg = f"CSV file {self.file} is empty!"
                    return False, error_msg

                for row in rows:
                    if len(row) != header_count:
                        raise csv.Error(f"More columns than headers in row: {row}")

                logger.info(f"CSV file {self.file} is valid with {len(rows)} rows")
                return True, "Valid CSV file."

        except csv.Error as e:
            error_msg = f"File {self.file} is not a valid CSV format! Error: {str(e)}"
            return False, error_msg
        except Exception as e:
            error_msg = f"Error reading file: {str(e)}!"
            logger.error(error_msg)
            return False, error_msg

    @property
    def load_csv(self) -> list[dict[str, str]]:
        """Loads CSV file and returns list of dictionaries."""
        logger.info(f"Loading CSV file: {self.file}")

        with open(self.file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            data = list(reader)

        logger.info(f"Successfully loaded {len(data)} records from {self.file}")
        return data


def is_numeric(value: Any) -> bool:
    """Checks if value is numeric."""

    try:
        float(value)
        return True
    except ValueError:
        return False


def convert_to_number(value: str) -> int | float:
    """Converts string into numeric (int or float)."""
    logger.debug(f"Converting value to number: {value}")

    try:
        if "." in value:
            result = float(value)
            logger.debug(f"Converted to float: {result}")
            return result
        else:
            result = int(value)
            logger.debug(f"Converted to int: {result}")
            return result
    except ValueError as e:
        error_msg = f"Cannot convert value {value} to numeric."
        logger.error(error_msg)
        raise ValueError(error_msg) from e


class TableCreator:
    def __init__(self, table_data: list[dict[str, str]], title: str = "Data"):
        self.table_data = table_data
        self.title = title
        logger.info(f"Created table with {len(table_data)} rows and title: {title}")

    def create_table(self) -> Table | str:
        """Creating table from data using rich."""
        logger.debug(f"Creating table with {len(self.table_data)} rows")

        if not self.table_data:
            logger.warning("No data to show in table")
            return "No data to show."

        table = Table(title=self.title, box=box.ROUNDED)

        headers = list(self.table_data[0].keys())
        for header in headers:
            table.add_column(header, style="cyan", no_wrap=True)

        for row in self.table_data:
            table.add_row(*[str(row[col]) for col in headers])

        logger.info(
            f"Successfully created table with {len(headers)} columns and {len(self.table_data)} rows"
        )
        return table

    def __str__(self) -> str:
        """String representation of the table."""
        table = self.create_table()
        if isinstance(table, str):
            return table
        return str(table)
