import logging

FORMAT = "%(asctime)-15s %(levelname)-8s %(message)s"


def setup_logging(log_level: int) -> None:
    """Setup logging for application."""
    logging.basicConfig(format=FORMAT, level=log_level)
