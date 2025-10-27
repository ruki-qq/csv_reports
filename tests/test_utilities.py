import pytest

from utils import convert_to_number, is_numeric


class TestUtilityFunctions:
    """Test cases for utility functions."""

    def test_is_numeric_valid_integers(self):
        assert is_numeric("123") is True
        assert is_numeric("0") is True
        assert is_numeric("-456") is True

    def test_is_numeric_valid_floats(self):
        assert is_numeric("123.45") is True
        assert is_numeric("0.0") is True
        assert is_numeric("-456.789") is True
        assert is_numeric(".5") is True
        assert is_numeric("5.") is True

    def test_is_numeric_invalid_strings(self):
        assert is_numeric("abc") is False
        assert is_numeric("12abc") is False
        assert is_numeric("") is False
        assert is_numeric(" ") is False
        assert is_numeric("12.34.56") is False

    def test_is_numeric_edge_cases(self):
        assert is_numeric("inf") is True
        assert is_numeric("-inf") is True
        assert is_numeric("nan") is True

    def test_convert_to_number_integers(self):
        assert convert_to_number("123") == 123
        assert convert_to_number("0") == 0
        assert convert_to_number("-456") == -456

    def test_convert_to_number_floats(self):
        assert convert_to_number("123.45") == 123.45
        assert convert_to_number("0.0") == 0.0
        assert convert_to_number("-456.789") == -456.789
        assert convert_to_number(".5") == 0.5
        assert convert_to_number("5.") == 5.0

    def test_convert_to_number_invalid_strings(self):
        with pytest.raises(ValueError, match="Cannot convert value abc to numeric"):
            convert_to_number("abc")

        with pytest.raises(ValueError, match="Cannot convert value 12abc to numeric"):
            convert_to_number("12abc")

        with pytest.raises(ValueError, match="Cannot convert value  to numeric"):
            convert_to_number("")

    def test_convert_to_number_type_consistency(self):
        """Test that convert_to_number returns consistent types."""

        assert isinstance(convert_to_number("123"), int)
        assert isinstance(convert_to_number("0"), int)
        assert isinstance(convert_to_number("-456"), int)

        assert isinstance(convert_to_number("123.45"), float)
        assert isinstance(convert_to_number("0.0"), float)
        assert isinstance(convert_to_number(".5"), float)
