import logging


def setup_logging(level: int = logging.INFO) -> None:
    """
    Configure logging for the application.

    Args:
        level: Logging level (default: INFO)
    """

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for the given module name.

    Args:
        name: Module name (usually __name__)

    Returns:
        Logger instance
    """

    return logging.getLogger(name)
