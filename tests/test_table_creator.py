from rich.table import Table

from utils import TableCreator


class TestTableCreator:
    """Test cases for TableCreator class."""

    def test_table_creator_initialization(self, sample_csv_data):
        """Test TableCreator initialization."""

        table_creator = TableCreator(sample_csv_data, "Test Table")

        assert table_creator.table_data == sample_csv_data
        assert table_creator.title == "Test Table"

    def test_table_creator_default_title(self, sample_csv_data):
        """Test TableCreator with default title."""

        table_creator = TableCreator(sample_csv_data)

        assert table_creator.title == "Data"

    def test_create_table_empty_data(self):
        """Test creating table with empty data."""

        table_creator = TableCreator([])
        result = table_creator.create_table()

        assert result == "No data to show."

    def test_create_table_valid_data(self, sample_csv_data):
        """Test creating table with valid data."""

        table_creator = TableCreator(sample_csv_data, "Products")
        result = table_creator.create_table()

        assert isinstance(result, Table)
        assert result.title == "Products"

        columns = [col.header for col in result.columns]
        expected_columns = ["name", "brand", "price", "rating"]
        assert all(col in columns for col in expected_columns)

    def test_create_table_single_row(self):
        """Test creating table with single row."""

        data = [{"name": "iphone", "brand": "apple", "price": "999", "rating": "4.5"}]
        table_creator = TableCreator(data, "Single Product")
        result = table_creator.create_table()

        assert isinstance(result, Table)
        assert len(result.rows) == 1
        assert result.title == "Single Product"

    def test_create_table_mixed_data_types(self):
        """Test creating table with mixed data types."""

        data = [
            {"name": "iphone", "brand": "apple", "price": 999, "rating": 4.5},
            {"name": "galaxy", "brand": "samsung", "price": "1199", "rating": "4.8"},
        ]
        table_creator = TableCreator(data, "Mixed Types")
        result = table_creator.create_table()

        assert isinstance(result, Table)
        assert len(result.rows) == 2
        assert result.title == "Mixed Types"

    def test_create_table_different_column_order(self):
        """Test creating table with different column order."""

        data = [
            {"rating": "4.5", "name": "iphone", "price": "999", "brand": "apple"},
            {"rating": "4.8", "name": "galaxy", "price": "1199", "brand": "samsung"},
        ]
        table_creator = TableCreator(data, "Different Order")
        result = table_creator.create_table()

        assert isinstance(result, Table)

        columns = [col.header for col in result.columns]
        expected_order = ["rating", "name", "price", "brand"]
        assert columns == expected_order

    def test_create_table_none_values(self):
        """Test creating table with None values."""
        data = [
            {"name": "iphone", "brand": "apple", "price": None, "rating": "4.5"},
            {"name": "galaxy", "brand": "samsung", "price": "1199", "rating": None},
        ]
        table_creator = TableCreator(data, "None Values")
        result = table_creator.create_table()

        assert isinstance(result, Table)
        assert len(result.rows) == 2
        assert result.title == "None Values"
