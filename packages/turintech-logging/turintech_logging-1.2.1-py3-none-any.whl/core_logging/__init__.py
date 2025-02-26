# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

from core_logging.logger_utils import get_logger

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

logger = get_logger()

__all__ = ["logger", "get_logger"]
