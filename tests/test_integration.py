from utils import AverageRatingReport, CsvReader, ReportRegistry, TableCreator


class TestIntegration:
    """Integration tests for the CSV filter application."""

    def test_end_to_end_csv_processing(self, temp_csv_file, sample_csv_data):
        """Test complete CSV processing pipeline."""

        reader = CsvReader(temp_csv_file)
        is_valid, msg = reader.check_csv_file
        assert is_valid is True

        data = reader.load_csv
        assert len(data) == len(sample_csv_data)

        report = AverageRatingReport()
        report_data = report.generate(data)

        assert len(report_data) > 0
        assert all("brand" in item and "rating" in item for item in report_data)

        table_creator = TableCreator(report_data, "Average Ratings")
        table = table_creator.create_table()

        assert table is not None

    def test_report_registry_integration(self):
        """Test ReportRegistry integration with actual report classes."""

        available_reports = ReportRegistry.get_available_reports()
        assert "average-rating" in available_reports

        report = ReportRegistry.get_report("average-rating")
        assert isinstance(report, AverageRatingReport)

        test_data = [
            {"brand": "apple", "rating": "4.5"},
            {"brand": "apple", "rating": "4.7"},
            {"brand": "samsung", "rating": "4.3"},
        ]

        result = report.generate(test_data)
        assert len(result) == 2

        apple_rating = next(
            item["rating"] for item in result if item["brand"] == "apple"
        )
        samsung_rating = next(
            item["rating"] for item in result if item["brand"] == "samsung"
        )
        assert apple_rating > samsung_rating

    def test_table_creation_with_real_data(self, sample_csv_data):
        """Test table creation with real sample data."""

        report = AverageRatingReport()
        report_data = report.generate(sample_csv_data)

        table_creator = TableCreator(report_data, "Brand Ratings")
        table = table_creator.create_table()

        assert table is not None
        assert len(table.columns) == 2
        assert len(table.rows) == len(report_data)
        assert table.title == "Brand Ratings"

    def test_performance_with_large_dataset(self):
        """Test performance with larger dataset."""

        large_data = []
        brands = ["apple", "samsung", "xiaomi", "huawei", "oneplus"]

        for i in range(1000):
            brand = brands[i % len(brands)]
            rating = 3.0 + (i % 20) * 0.1
            large_data.append({"brand": brand, "rating": str(rating)})

        report = AverageRatingReport()
        report_data = report.generate(large_data)

        assert len(report_data) == 5

        table_creator = TableCreator(report_data, "Large Dataset")
        table = table_creator.create_table()

        assert table is not None
        assert len(table.rows) == 5
