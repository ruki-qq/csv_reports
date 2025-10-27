from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Any

from .logger import get_logger
from .shortcuts import convert_to_number, is_numeric

logger = get_logger(__name__)


class BaseReport(ABC):
    """Base report class."""

    @abstractmethod
    def generate(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Generate report from data.

        Args:
            data: list of dictionaries with some data.

        Returns:
            List of dictionaries for further operations.
        """

        raise NotImplementedError


class AverageRatingReport(BaseReport):
    """Reports average ratings by brand."""

    def generate(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Generate report with brands avg rating from products data.

        Args:
            data: List of dictionaries with products data.

        Returns:
            List of dictionaries with brands and their avf ratings,
            sorted by rating(desc).
        """

        logger.info(f"Generating average rating report for {len(data)} products")

        brand_ratings = defaultdict(list)

        for product in data:
            brand = product["brand"]
            rating = product["rating"]

            try:
                is_numeric(rating)
            except ValueError as e:
                logger.error(e)
                raise ValueError(e)

            rating = convert_to_number(product["rating"])
            brand_ratings[brand].append(rating)

        report_data = []
        for brand, ratings in brand_ratings.items():
            avg_rating = sum(ratings) / len(ratings)
            report_data.append({"brand": brand, "rating": round(avg_rating, 2)})

        report_data.sort(key=lambda x: x["rating"], reverse=True)

        logger.info(f"Generated report with {len(report_data)} brands")
        return report_data


class ReportRegistry:
    """Registry of available reports."""

    _reports = {
        "average-rating": AverageRatingReport,
    }

    @classmethod
    def get_report(cls, report_name: str) -> BaseReport:
        """
        Return report class instance by name.

        Args:
            report_name: report name.

        Returns:
            Report class instance.

        Raises:
            ValueError: If report name is not found.
        """

        logger.info(f"Requesting report: {report_name}")

        if report_name not in cls._reports:
            error_msg = (
                f"Report '{report_name}' isn't found."
                f"Available reports: {', '.join(cls._reports)}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)

        logger.info(f"Successfully created report instance for: {report_name}")
        return cls._reports[report_name]()

    @classmethod
    def get_available_reports(cls) -> list[str]:
        """
        Returns available reports.

        Returns:
            List of available report names.
        """

        return list(cls._reports)

    @classmethod
    def register_report(cls, report_name: str, report_class: BaseReport) -> BaseReport:
        """
        Register report class.

        Args:
            report_name: report name.
            report_class: report class.

        Returns:
            Registered report class.
        """

        cls._reports[report_name] = report_class
        return report_class
