# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
import sys
from typing import Any, Dict, Optional

# Core Source imports
from core_logging import logger
from core_logging.logger_conf import (
    EnableLoggerConf,
    FileLoggerConf,
    LoggerConf,
    enable_logger_conf_factory,
    file_logger_conf_factory,
    logger_conf_factory,
)

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["LoggerService"]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                Service implementation                                                #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class LoggerService:
    """
    Logging configuration service.
    """

    _prefix: Optional[str] = "LOGGER"
    _env_file: Optional[str]

    _enable_logger_conf: Optional[EnableLoggerConf] = None
    defaults_enable_logger_conf: Dict[str, Any]

    _file_logger_conf: Optional[FileLoggerConf] = None
    defaults_file_logger_conf: Dict[str, Any]

    _logger_conf: Optional[Dict[str, LoggerConf]] = None
    mandatory_logger_conf: Dict[str, Dict[str, Any]]

    extra: Optional[Dict[str, str]] = None

    def __init__(
        self,
        prefix: Optional[str] = _prefix,
        env_file: Optional[str] = None,
        defaults_enable_logger_conf: Optional[Dict[str, Any]] = None,
        defaults_file_logger_conf: Optional[Dict[str, Any]] = None,
        extra: Optional[Dict[str, str]] = None,
    ):
        """

        Args:
            prefix (Optional[str]): Prefix that the class attributes must have in the environment variables.
            env_file (Optional[str]): Configuration file of the environment variables from where to load the values.
            defaults_file_logger_conf (Optional[Dict[str, Any]]): Default configuration of enable and disable
                the different types of logging. It is used if it is not specify as environment variables
            defaults_file_logger_conf (Optional[Dict[str, Any]]): Default configuration attributes of the application
                file logs. It is used if it is not specify as environment variables
            extra (Optional[Dict[str, str]]): A dict containing additional parameters bound to the core logger,
                useful to share common properties if you call |bind| in several of your files modules. If not ``None``,
                this will remove previously configured ``extra`` dict.
        """
        self._prefix = prefix
        self._env_file = env_file
        self.defaults_enable_logger_conf = defaults_enable_logger_conf or {}
        self.defaults_file_logger_conf = defaults_file_logger_conf or {}
        self.mandatory_logger_conf = {"stdout": {"sink": sys.stdout}, "stderr": {"sink": sys.stderr, "level": "ERROR"}}
        self.extra = extra

    # ---------------------------------------------------------------------------------------------------

    def get_configuration(self, complete: bool = False) -> Dict[str, Any]:
        """
        Return the current configuration as a dictionary.
        """
        configuration = {
            "prefix": self._prefix,
            "env_file": self._env_file,
            "defaults_enable_logger_conf": self.defaults_enable_logger_conf,
            "defaults_file_logger_conf": self.defaults_file_logger_conf,
            "mandatory_logger_conf": self.mandatory_logger_conf,
            "extra": self.extra,
            "enable_logger_conf": self._enable_logger_conf.dict() if self._enable_logger_conf else None,
            "file_logger_conf": self._file_logger_conf.dict() if self._file_logger_conf else None,
            "logger_conf": {key: logger_conf.dict() for key, logger_conf in (self._logger_conf or {}).items()},
        }
        if complete:
            configuration.update(
                {
                    "enable_logger_conf": self.enable_logger_conf.dict(),
                    "file_logger_conf": self.file_logger_conf.dict(),
                    "logger_conf": {key: logger_conf.dict() for key, logger_conf in self.logger_conf.items()},
                }
            )
        return configuration

    # ------------------------------------- enable_logger_conf -------------------------------------- #

    @property
    def enable_logger_conf(self) -> EnableLoggerConf:
        """
        Enable or disable logging configuration.
        """
        return self._create_enable_logger_conf() if self._enable_logger_conf is None else self._enable_logger_conf

    def _create_enable_logger_conf(self) -> EnableLoggerConf:
        """
        Create an EnableLoggerConf configuration by loading the environment variables from the indicated file and taking
        into account the default values.
        """
        self._enable_logger_conf = enable_logger_conf_factory(
            _env_file=self._env_file, prefix=self._prefix, defaults=self.defaults_enable_logger_conf
        )
        return self._enable_logger_conf

    # --------------------------------------- file_logger_conf --------------------------------------- #

    @property
    def file_logger_conf(self) -> FileLoggerConf:
        """
        Logging configuration of the logs directed to file path outputs.
        """
        return self._create_file_logger_conf() if self._file_logger_conf is None else self._file_logger_conf

    def _create_file_logger_conf(self) -> FileLoggerConf:
        """
        Create an FileLoggerConf configuration by loading the environment variables from the indicated file and taking
        into account the default values.
        """
        self._file_logger_conf = file_logger_conf_factory(
            _env_file=self._env_file, prefix=self._prefix, defaults=self.defaults_file_logger_conf
        )
        return self._file_logger_conf

    # ----------------------------------------- logger_conf ----------------------------------------- #

    @property
    def logger_conf(self) -> Dict[str, LoggerConf]:
        """
        Logging configuration of the logs directed to system outputs.
        """
        return self._create_logger_conf() if self._logger_conf is None else self._logger_conf

    def _create_logger_conf(self) -> Dict[str, LoggerConf]:
        """
        Create an LoggerConf configuration by loading the environment variables from the indicated file and taking into
        account the default values.
        """
        self._logger_conf = {
            key: logger_conf_factory(
                _env_file=self._env_file, prefix=self._prefix, defaults=self.defaults_file_logger_conf, **mandatory
            )
            for key, mandatory in self.mandatory_logger_conf.items()
        }
        return self._logger_conf

    # -------------------------------------- init_logging_conf --------------------------------------- #

    def init_logging_conf(self) -> None:
        """
        Initialize logging with the service configuration.
        """
        enable_logger_conf = self.enable_logger_conf
        if enable_logger_conf.enable:
            logger.configure(extra=self.extra)
            logger.remove()
            for key, configuration in self.logger_conf.items():
                if key == "stdout" or (enable_logger_conf.enable_stderr and key == "stderr"):
                    logger.add(**configuration.dict())
            if enable_logger_conf.enable_file:
                logger.add(**self.file_logger_conf.dict())
            logger.debug(f"Logger configured: {self.get_configuration(complete=True)}")
