"""
This module defines the common attributes necessary for the treatment of application logs.
"""
# pylint: disable=E0213,E0611
#        E0213: Method should have "self" as first argument (no-self-argument)
#        E0611: No name 'BaseModel' in module 'pydantic' (no-name-in-module)
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
import sys
from datetime import time, timedelta
from pathlib import Path
from typing import Callable, Dict, Optional, Union

from pydantic.v1 import Extra, Field, validator

from core_common_configuration import BaseConfEnv, conf_factory

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = [
    "EnableLoggerConf",
    "LoggerConf",
    "FileLoggerConf",
    "logger_conf_factory",
    "file_logger_conf_factory",
    "enable_logger_conf_factory",
]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                Logging Configuration                                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class EnableLoggerConf(BaseConfEnv):
    """
    Configuration of enable and disable the different types of logging.
    """

    enable: bool = Field(
        True,
        description="Flag that indicates whether the logging configuration should be initialized (true) or, "
        "if on the contrary, this configuration is already supposed to be initialized (false).",
    )
    enable_file: bool = Field(True, description="Flag that enables (True) or disables (False) the log to file.")
    enable_stderr: bool = Field(
        False, description="Flag that enables (True) or disables (False) the log to stderr output."
    )


class LoggerConf(BaseConfEnv, extra=Extra.ignore):  # type: ignore
    """This class contains the configuration attributes of the application logs. The attributes of this class are
    updated with the values of the environment variables.

    - sink: An object in charge of receiving formatted logging messages and propagating them to an appropriate endpoint.
    - level: The minimum severity level from which logged messages should be sent to the sink.
    - format: The template used to format logged messages before being sent to the sink.
    - colorize: Whether the color markups contained in the formatted message should be converted to ansi codes for
        terminal coloration, or stripped otherwise. If None, the choice is automatically made based on the sink
        being a tty or not.
    - serialize: Whether the logged message and its records should be first converted to a JSON string before being
        sent to the sink.
    - backtrace: Whether the exception trace formatted should be extended upward, beyond the catching point,
        to show the full stacktrace which generated the error.
    - diagnose: Whether the exception trace should display the variables values to eases the debugging.
        This should be set to False in production to avoid leaking sensitive data.
    - enqueue: Whether the messages to be logged should first pass through a multiprocess-safe queue before reaching
        the sink.
        This is useful while logging to a file through multiple processes.
        This also has the advantage of making logging calls non-blocking.

    Only on logs directed to file path outputs:
    - rotation: A condition indicating whenever the current logged file should be closed and a new one started.
    - retention: A directive filtering old files that should be removed during rotation or end of program.
    - compression: A compression or archive format to which log files should be converted at closure.
    - delay: Whether the file should be created as soon as the sink is configured, or delayed until first logged
        message.
        It defaults to False.

    """

    sink: Union[Path, object]

    level: str = "INFO"
    format: Union[str, Callable] = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>"
        " <r>-</r> <level>{level: <8}</level>"
        " <r>-</r> <cyan>{name}</cyan>.<cyan>{function}</cyan>:<cyan>{line}</cyan>"
        " <r>-</r> <level>{message}</level>"
    )
    colorize: Optional[bool] = True
    serialize: Optional[bool] = False
    backtrace: Optional[bool] = True
    diagnose: Optional[bool] = False
    enqueue: Optional[bool] = True

    @validator("level")
    def upper_validator(cls, value: str):
        return value.upper() if value else value

    @validator("sink", pre=True)
    def sink_validator(cls, value: str):
        return {
            "sys.stdout": sys.stdout,
            "sys.stderr": sys.stderr,
        }.get(value, value)


class FileLoggerConf(LoggerConf):
    """
    This class contains the configuration attributes of the application file logs.
    """

    colorize: Optional[bool] = False
    rotation: Union[str, int, time, timedelta] = "12:00"  # New file is created each day at noon
    retention: Union[str, int, time, timedelta] = "1 month"
    compression: Optional[str] = "zip"
    delay: bool = True


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                            Logging Configuration Factory                                             #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


def enable_logger_conf_factory(
    _env_file: Optional[str] = None, prefix: Optional[str] = None, defaults: Optional[Dict] = None, **kwargs
) -> EnableLoggerConf:
    """This is a factory generating a EnableLoggerConf class specific to a service, loading every value from a generic
    .env file storing variables in uppercase with a service prefix.

    example .env:
       PREFIX_ENABLE=true
       ...

    Args:
        _env_file (str): Configuration file of the environment variables from where to load the values.
        prefix (str): Prefix that the class attributes must have in the environment variables.
        defaults (Optional:Dict): New values to override the default field values for the configuration model.
        kwargs (**Dict): Arguments passed to the Settings class initializer.

    Returns:
        conf (EnableLoggerConf): Object of the required configuration class

    """
    return conf_factory(config_class=EnableLoggerConf, _env_file=_env_file, prefix=prefix, defaults=defaults, **kwargs)


def logger_conf_factory(
    _env_file: Optional[str] = None, prefix: Optional[str] = None, defaults: Optional[Dict] = None, **kwargs
) -> LoggerConf:
    """This is a factory generating a LoggerConf class specific to a service, loading every value from a generic .env
    file storing variables in uppercase with a service prefix.

    example .env:
       PREFIX_LEVEL=INFO
       ...

    Args:
        _env_file (str): Configuration file of the environment variables from where to load the values.
        prefix (str): Prefix that the class attributes must have in the environment variables.
        defaults (Optional:Dict): New values to override the default field values for the configuration model.
        kwargs (**Dict): Arguments passed to the Settings class initializer.

    Returns:
        conf (LoggerConf): Object of the required configuration class

    """
    return conf_factory(config_class=LoggerConf, _env_file=_env_file, prefix=prefix, defaults=defaults, **kwargs)


def file_logger_conf_factory(
    _env_file: Optional[str] = None, prefix: Optional[str] = None, defaults: Optional[Dict] = None, **kwargs
) -> FileLoggerConf:
    """This is a factory generating a FileLoggerConf class specific to a service, loading every value from a generic
    .env file storing variables in uppercase with a service prefix.

    example .env:
       PREFIX_LEVEL=INFO
       PREFIX_COLORIZE=true
       ...

    Args:
        _env_file (str): Configuration file of the environment variables from where to load the values.
        prefix (str): Prefix that the class attributes must have in the environment variables.
        defaults (Optional:Dict): New values to override the default field values for the configuration model.
        kwargs (**Dict): Arguments passed to the Settings class initializer.

    Returns:
        conf (FileLoggerConf): Object of the required configuration class

    """
    return conf_factory(config_class=FileLoggerConf, _env_file=_env_file, prefix=prefix, defaults=defaults, **kwargs)
