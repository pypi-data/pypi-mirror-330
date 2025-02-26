# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from typing_extensions import TypeAlias

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["LoggerType", "get_logger"]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                              Serialize logger utilities                                              #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


def logger_type():
    from loguru._logger import Logger  # pylint: disable=import-outside-toplevel

    return Logger


LoggerType: TypeAlias = logger_type()  # type: ignore


def get_logger(**bind_args) -> LoggerType:
    """Retrieve the loguru logger.

    Workaround for the following issue with loguru:
        https://github.com/ray-project/ray/issues/14717

    Returns:
        logger (from loguru import Logger)

    """
    from loguru import logger  # pylint: disable=import-outside-toplevel

    return logger.bind(**bind_args)
