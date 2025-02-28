# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Rudy Lei <shlei@cisco.com>, Yang Bian <yabian@cisco.com>

import os
import logging
import threading

from logging.handlers import RotatingFileHandler
from aac_init.control_engine.global_cache import context_cache


class StreamThreadFilter(logging.StreamHandler):
    def filter(self, record: logging.LogRecord) -> bool:
        return threading.current_thread() == threading.main_thread()


class LazyLogger:
    def __init__(
        self,
        log_file,
        log_level=None,
        console_stream=False,
        max_size=5 * 1024 * 1024,
        backup_count=1000,
    ):
        self._log_file = log_file
        self._log_level = log_level
        self._console_stream = console_stream
        self._max_size = max_size
        self._backup_count = backup_count
        self._logger = None

    def _setup_logger(self):
        if not self._log_level:
            global_log_level = context_cache.get("log_level")
            log_level = global_log_level if global_log_level else "info"
        else:
            log_level = self._log_level

        log_levels = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL,
        }

        logger_name = (
            self._log_file[:-4] if self._log_file.endswith(".log") else self._log_file
        )
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
        )

        log_dir = os.path.join(context_cache.output_dir, "aac_init_log")
        os.makedirs(log_dir, exist_ok=True)
        log_file_path = os.path.join(log_dir, self._log_file)
        level = log_levels.get(log_level.lower(), logging.DEBUG)

        if self._console_stream and not any(
            isinstance(h, logging.StreamHandler) for h in logger.handlers
        ):
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        if not any(
            isinstance(h, RotatingFileHandler) and h.baseFilename == log_file_path
            for h in logger.handlers
        ):
            file_handler = RotatingFileHandler(
                log_file_path, maxBytes=self._max_size, backupCount=self._backup_count, mode="a"
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        logger.propagate = False
        self._logger = logger

    def __getattr__(self, item):
        if self._logger is None:
            self._setup_logger()
        return getattr(self._logger, item)



def netmiko_session_logger(log_file):
    """
    Setup netmiko session_log path.

    :param log_file: log file name
    """
    log_file_path = os.path.join(context_cache.output_dir, "aac_init_log", log_file)

    return log_file_path
