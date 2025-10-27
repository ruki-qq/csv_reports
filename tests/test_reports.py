import pytest

from utils import AverageRatingReport, BaseReport, ReportRegistry


class TestAverageRatingReport:
    """Test cases for AverageRatingReport class."""

    def test_generate_empty_data(self):
        report = AverageRatingReport()
        result = report.generate([])

        assert result == []

    def test_generate_single_product(self):
        report = AverageRatingReport()
        data = [{"brand": "apple", "rating": "4.5"}]
        result = report.generate(data)

        assert len(result) == 1
        assert result[0]["brand"] == "apple"
        assert result[0]["rating"] == 4.5

    def test_generate_multiple_products_same_brand(self):
        """Test generating report with multiple products from same brand."""

        report = AverageRatingReport()
        data = [
            {"brand": "apple", "rating": "4.5"},
            {"brand": "apple", "rating": "4.7"},
            {"brand": "apple", "rating": "4.3"},
        ]
        result = report.generate(data)

        assert len(result) == 1
        assert result[0]["brand"] == "apple"
        assert result[0]["rating"] == 4.5

    def test_generate_multiple_brands(self, sample_csv_data):
        report = AverageRatingReport()
        result = report.generate(sample_csv_data)

        assert len(result) == 3

        ratings = [item["rating"] for item in result]
        assert ratings == sorted(ratings, reverse=True)

        brands = {item["brand"] for item in result}
        assert brands == {"apple", "samsung", "xiaomi"}

    def test_generate_rating_precision(self):
        """Test that ratings are properly rounded to 2 decimal places."""

        report = AverageRatingReport()
        data = [
            {"brand": "apple", "rating": "4.333333"},
            {"brand": "apple", "rating": "4.666666"},
        ]
        result = report.generate(data)

        assert result[0]["rating"] == 4.5

    def test_generate_invalid_rating(self):
        report = AverageRatingReport()
        data = [{"brand": "apple", "rating": "invalid"}]

        with pytest.raises(ValueError, match="Cannot convert value invalid to numeric"):
            report.generate(data)

    def test_generate_missing_brand_key(self):
        report = AverageRatingReport()
        data = [{"rating": "4.5"}]

        with pytest.raises(KeyError):
            report.generate(data)

    def test_generate_missing_rating_key(self):
        report = AverageRatingReport()
        data = [{"brand": "apple"}]

        with pytest.raises(KeyError):
            report.generate(data)

    def test_generate_non_numeric_rating_key(self):
        report = AverageRatingReport()
        data = [{"brand": "apple", "rating": "four"}]

        with pytest.raises(ValueError, match="Cannot convert value four to numeric."):
            report.generate(data)


class TestReportRegistry:
    """Test cases for ReportRegistry class."""

    def test_get_report_valid(self):
        report = ReportRegistry.get_report("average-rating")

        assert isinstance(report, AverageRatingReport)

    def test_get_report_invalid(self):
        with pytest.raises(ValueError, match="Report 'invalid-report' isn't found"):
            ReportRegistry.get_report("invalid-report")

    def test_get_available_reports(self):
        reports = ReportRegistry.get_available_reports()

        assert isinstance(reports, list)
        assert "average-rating" in reports

    def test_register_report(self):
        """Test registering a new report."""

        class TestReport(BaseReport):
            def generate(self, data):
                return data

        ReportRegistry.register_report("test-report", TestReport)

        assert "test-report" in ReportRegistry.get_available_reports()

        report = ReportRegistry.get_report("test-report")
        assert isinstance(report, TestReport)

        del ReportRegistry._reports["test-report"]
