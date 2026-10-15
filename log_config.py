"""Shared colored terminal logging configuration."""

import logging

import colorlog


class _ProjectLogFilter(logging.Filter):
    """Keep third-party records out of the project's formatted handler."""

    PREFIXES = (
        "data-preprocessing",
        "federated-",
        "model-",
    )

    def filter(self, record: logging.LogRecord) -> bool:
        return record.name.startswith(self.PREFIXES)


def configure_logging(level: int = logging.INFO) -> None:
    """Configure one colored handler shared by the entire project."""
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()
    handler = colorlog.StreamHandler()
    handler.setLevel(level)
    handler.addFilter(_ProjectLogFilter())
    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s | %(levelname)-8s | %(name)s | "
            "%(filename)s:%(lineno)d | %(message)s",
            datefmt="%H:%M:%S",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red,bg_white",
            },
            reset=True,
        )
    )
    root_logger.addHandler(handler)
    # Flower has its own console handler. Keep only warnings from it so project
    # round summaries are not duplicated by Flower INFO/DEBUG records.
    logging.getLogger("flwr").setLevel(logging.WARNING)


def base_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Return a named logger using the shared project configuration."""
    if not logging.getLogger().handlers:
        configure_logging()
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger
