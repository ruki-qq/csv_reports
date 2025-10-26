from pathlib import Path
from rich.console import Console

from utils import (
    ArgParser,
    CsvReader,
    ReportRegistry,
    TableCreator,
    setup_logging,
    get_logger,
)

# Setup logging
setup_logging()
logger = get_logger(__name__)


def main(args: list[str] = None) -> int:
    """
    Script entry point.

    Args:
        args: List of arguments

    Returns:
        Exit code (0 - success, 1 - error)
    """
    parser = ArgParser()
    parsed_args = parser.parse_args(args)

    console = Console()
    products: list[dict[str, str]] = []

    for file in parsed_args.files:
        is_valid, msg = CsvReader(Path(file)).check_csv_file
        if not is_valid:
            logger.warning(msg)
            continue
        products.extend(CsvReader(Path(file)).load_csv)

    if not products:
        logger.error("No products found.")
        return 1

    report_generator = ReportRegistry.get_report(parsed_args.report)

    try:
        report_data = report_generator.generate(products)
    except Exception as e:
        logger.error(e)
        return 1

    table = TableCreator(report_data, parsed_args.report)
    console.print(table.create_table())
    return 0


if __name__ == "__main__":
    main()
