import csv
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def sample_csv_data():
    """Sample CSV data for testing."""

    return [
        {"name": "iphone 15 pro", "brand": "apple", "price": "999", "rating": "4.9"},
        {
            "name": "galaxy s23 ultra",
            "brand": "samsung",
            "price": "1199",
            "rating": "4.8",
        },
        {"name": "redmi note 12", "brand": "xiaomi", "price": "199", "rating": "4.6"},
        {"name": "iphone 14", "brand": "apple", "price": "799", "rating": "4.7"},
        {"name": "galaxy a54", "brand": "samsung", "price": "349", "rating": "4.2"},
    ]


@pytest.fixture
def temp_csv_file(sample_csv_data):
    """Create a temporary CSV file for testing."""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        writer = csv.DictWriter(f, fieldnames=["name", "brand", "price", "rating"])
        writer.writeheader()
        writer.writerows(sample_csv_data)
        temp_path = Path(f.name)

    yield temp_path

    temp_path.unlink()


@pytest.fixture
def invalid_csv_file():
    """Create a temporary invalid CSV file for testing."""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("invalid,csv,content\nwith no proper structure")
        temp_path = Path(f.name)

    yield temp_path

    # Cleanup
    temp_path.unlink()


@pytest.fixture
def empty_csv_file():
    """Create a temporary empty CSV file for testing."""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("empty,csv,file")
        temp_path = Path(f.name)

    yield temp_path

    # Cleanup
    temp_path.unlink()


@pytest.fixture
def non_csv_file():
    """Create a temporary non-CSV file for testing."""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("This is not a CSV file")
        temp_path = Path(f.name)

    yield temp_path

    # Cleanup
    temp_path.unlink()


@pytest.fixture
def nonexistent_file():
    """Path to a non-existent file."""
    return Path("nonexistent_file.csv")
