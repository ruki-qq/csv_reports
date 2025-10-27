import pytest

from utils import CsvReader


class TestCsvReader:
    """Test cases for CsvReader class."""

    def test_csv_reader_initialization(self, temp_csv_file):
        """Test CsvReader initialization."""

        reader = CsvReader(temp_csv_file)
        assert reader.file == temp_csv_file

    def test_check_csv_file_valid(self, temp_csv_file):
        """Test checking a valid CSV file."""

        reader = CsvReader(temp_csv_file)
        is_valid, msg = reader.check_csv_file

        assert is_valid is True
        assert "Valid CSV file." in msg

    def test_check_csv_file_nonexistent(self, nonexistent_file):
        """Test checking a non-existent file."""

        reader = CsvReader(nonexistent_file)
        is_valid, msg = reader.check_csv_file

        assert is_valid is False
        assert f"File {nonexistent_file} does not exist!" in msg

    def test_check_csv_file_wrong_extension(self, non_csv_file):
        """Test checking a file with wrong extension."""

        reader = CsvReader(non_csv_file)
        is_valid, msg = reader.check_csv_file

        assert is_valid is False
        assert f"File {non_csv_file} is not a CSV file!" in msg

    def test_check_csv_file_empty(self, empty_csv_file):
        """Test checking an empty CSV file."""

        reader = CsvReader(empty_csv_file)
        is_valid, msg = reader.check_csv_file

        assert is_valid is False
        assert f"CSV file {empty_csv_file} is empty!" in msg

    def test_check_csv_file_invalid_format(self, invalid_csv_file):
        """Test checking an invalid CSV format."""

        reader = CsvReader(invalid_csv_file)
        is_valid, msg = reader.check_csv_file

        assert is_valid is False
        assert "not a valid CSV format" in msg

    def test_load_csv_valid(self, temp_csv_file, sample_csv_data):
        """Test loading a valid CSV file."""

        reader = CsvReader(temp_csv_file)
        data = reader.load_csv

        assert len(data) == len(sample_csv_data)
        assert data[0]["name"] == sample_csv_data[0]["name"]
        assert data[0]["brand"] == sample_csv_data[0]["brand"]
        assert data[0]["price"] == sample_csv_data[0]["price"]
        assert data[0]["rating"] == sample_csv_data[0]["rating"]

    def test_load_csv_file_not_found(self, nonexistent_file):
        """Test loading a non-existent CSV file."""

        reader = CsvReader(nonexistent_file)

        with pytest.raises(FileNotFoundError):
            reader.load_csv
