# -*- encoding: utf-8 -*-

import sys
import time
import argparse

from pyrpc_schedule.meta.key import ROOT_PATH_KEY, PROXY_NAME_KEY, SYSTEM_DEFAULT_SCHEDULE_TIME_KEY, \
    SYSTEM_SERVICE_NAME_KEY, TASK_ID_KEY, TASK_IS_SUB_TASK_KEY

from pyrpc_schedule.rabbit import RabbitMQ
from pyrpc_schedule.utils import load_config, Logger


class RunSchedule:
    """
    Singleton class for managing the run schedule.
    """
    _instance = None

    _config = None
    _logger = None
    _rabbitmq = None
    _system_default_schedule_time = None

    def __new__(cls, *args, **kwargs):
        """
        Overrides the __new__ method to implement the singleton pattern.
        If the singleton instance does not exist, it creates a new instance and initializes it.
        Otherwise, it returns the existing instance.
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        Returns:
            RunSchedule: The singleton instance of the RunSchedule class.
        """
        if not cls._instance:
            cls._instance = super(RunSchedule, cls).__new__(cls)
        return cls._instance

    def __init__(self, config):
        """
        Initializes the RunSchedule instance.
        Args:
            config (dict): The configuration dictionary.
        """
        if self._config is None:
            self._config = config
            self._rabbitmq = RabbitMQ(config=config)
            self._logger = Logger(config=config).logger(filename=PROXY_NAME_KEY, task_id='Schedule')
            self._system_default_schedule_time = self._config.get(SYSTEM_DEFAULT_SCHEDULE_TIME_KEY, 10)

    def task_distribution(self):
        """
        Distributes tasks based on the configuration.
        """
        self._rabbitmq.send_message(
            queue='{}_task_distribution'.format(SYSTEM_SERVICE_NAME_KEY),
            message={
                'self_config': self._config,
                TASK_ID_KEY: 'task_distribution',
                TASK_IS_SUB_TASK_KEY: False
            }
        )

    def run(self):
        while True:
            try:
                self.task_distribution()
                time.sleep(self._system_default_schedule_time)
            except Exception as e:
                self._logger.error('run schedule error: {}'.format(e))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="run schedule script")

    parser.add_argument("--config", type=str, help="run schedule config")
    args = parser.parse_args()

    configs = load_config(args.config)

    sys.path.append(configs[ROOT_PATH_KEY])

    RunSchedule(config=configs).run()
