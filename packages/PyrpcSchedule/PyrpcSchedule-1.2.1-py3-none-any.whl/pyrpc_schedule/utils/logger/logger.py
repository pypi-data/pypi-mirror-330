# -*- encoding: utf-8 -*-

import os
import logging

from logging.handlers import TimedRotatingFileHandler

from pyrpc_schedule.meta.key import CONFIG_ROOT_PATH_KEY, CONFIG_LOGS_PATH_KEY


class Logger:
    """
    Logger class for logging messages.
    """
    _instance = None

    _config = None
    _logger_pool = {}
    _format_str = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] %(message)s')

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self, config):
        if self._config is None:
            self._config = config
            self._logs_path = os.path.join(config.get(CONFIG_ROOT_PATH_KEY), CONFIG_LOGS_PATH_KEY)
            os.makedirs(self._logs_path, exist_ok=True)

    def _get_log_file_path(self, filename: str, task_id: str = None):
        if task_id is None:
            return os.path.join(self._logs_path, f'{filename}.log')
        else:
            os.makedirs(os.path.join(self._logs_path, f'{filename}'), exist_ok=True)
            return os.path.join(self._logs_path, filename, f'{task_id}.log')

    def logger(self, filename: str, task_id: str = None) -> logging.Logger:
        """
        Get a logger instance for logging messages.
        Args:
            filename (str): The name of the log file.
            task_id (str, optional): The ID of the task. Defaults to None.
        Returns:
            logging.Logger: A logger instance.
        """
        handler = self._get_log_file_path(filename, task_id)
        if handler not in self._logger_pool:
            _logger = logging.getLogger(handler)
            _logger.setLevel(logging.INFO)
            _logger.propagate = False

            th = TimedRotatingFileHandler(filename=handler, when='MIDNIGHT', backupCount=7, encoding='utf-8')
            th.suffix = "%Y-%m-%d.log"
            th.setFormatter(self._format_str)

            if not any(isinstance(h, logging.StreamHandler) for h in _logger.handlers):
                ch = logging.StreamHandler()
                ch.setFormatter(self._format_str)
                _logger.addHandler(ch)

            _logger.addHandler(th)

            self._logger_pool[handler] = _logger
        return self._logger_pool[handler]
