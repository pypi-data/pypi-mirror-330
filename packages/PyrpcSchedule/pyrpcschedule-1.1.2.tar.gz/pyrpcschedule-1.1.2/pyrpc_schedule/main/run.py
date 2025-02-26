# -*- encoding: utf-8 -*-

import sys
import json
import time
import base64
import psutil
import subprocess
from pathlib import Path

from pyrpc_schedule.meta.key import HTTP_SERVER_FORK_KEY, DEFAULT_HTTP_SERVER_FORK_KEY
from pyrpc_schedule.services.schedule import task_distribution


class ServiceManagement:
    """
    A singleton class responsible for managing services, including service registration and heartbeat detection.
    """
    _instance = None

    _config = None
    _encoded_config: str = None
    _python_name: str = 'python3'
    _python_executable: str = 'python3'

    _service_list = [task_distribution]

    def __new__(cls, *args, **kwargs):
        """
        Overrides the __new__ method to implement the singleton pattern.
        If the singleton instance does not exist, it creates a new instance and initializes it.
        Otherwise, it returns the existing instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            ServiceManagement: The singleton instance of the ServiceManagement class.
        """
        if not cls._instance:
            cls._instance = super(ServiceManagement, cls).__new__(cls)
        return cls._instance

    def __init__(self, config: dict):
        """
        Initializes the service configuration based on the provided configuration dictionary.

        Args:
            config (dict): A dictionary containing the service configuration.
        """
        if self._encoded_config is None:
            self._config = config
            self._encoded_config = base64.b64encode(json.dumps(config).encode('utf-8')).decode('utf-8')
            self._python_executable = sys.executable if 'python' in sys.executable else 'python3'

    def registry(self, services: list):
        """
        Registers a list of services to be managed.

        Args:
            services (list): A list of services to be registered.
        """

        [self._service_list.append(i) for i in services]

    def kill_process(self, script_file_path, target_file_path):
        """
        Kills the specified script file.
        Args:
            script_file_path : script file object
            target_file_path : target file object
        """

        for proc in psutil.process_iter(['name', 'cmdline']):
            try:
                name = proc.name()
                cmdline = proc.cmdline()
                if self._python_name in name:
                    script_file_path_proc = False
                    target_file_path_proc = False
                    for arg in cmdline:
                        if Path(script_file_path).as_posix() in Path(arg).as_posix():
                            script_file_path_proc = True

                        if Path(target_file_path).as_posix() in Path(arg).as_posix():
                            target_file_path_proc = True

                    if script_file_path_proc and target_file_path_proc:
                        proc.kill()
                        time.sleep(0.1)
                        break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

    def start_heartbeat_detection(self):
        """
        Starts the heartbeat detection process. It encodes the configuration,
        terminates any existing heartbeat detection processes, and then starts a new one.

        Returns:
            int: The process ID of the newly started heartbeat detection process.
        """
        from pyrpc_schedule.services.monitoring import heartbeat_detection
        script_file = Path(heartbeat_detection.__file__).resolve()
        self.kill_process(script_file_path=script_file, target_file_path=script_file)

        command = [
            self._python_executable,
            script_file,
            '--config', self._encoded_config
        ]

        process = subprocess.Popen(command)
        return process.pid

    def start_http_server(self):
        """
        Starts the http server process. It encodes the configuration,
        terminates any existing http server processes, and then starts a new one.
        Returns:
            int: The process ID of the newly started http server process.
        """
        from pyrpc_schedule.services.web import run_http_server
        script_file = Path(run_http_server.__file__).resolve()
        self.kill_process(script_file_path=script_file, target_file_path=script_file)

        fork_http_server = self._config.get(HTTP_SERVER_FORK_KEY, DEFAULT_HTTP_SERVER_FORK_KEY)
        if fork_http_server:
            command = [
                self._python_executable,
                script_file,
                '--config', self._encoded_config
            ]
            process = subprocess.Popen(command)
            return process.pid
        else:
            import os
            cmd = '{} {} --config {}'.format(self._python_executable, script_file, self._encoded_config)
            os.system(cmd)

    def start_service(self, service_main_file_path):
        """
        Starts the service and starts the heartbeat detection process.
        Args:
            service_main_file_path : The path to the service main file.
        Returns:
            int: The process ID of the newly started service process.
        """
        from pyrpc_schedule.main.server import run_service
        script_file = Path(run_service.__file__).resolve()
        self.kill_process(script_file_path=script_file, target_file_path=service_main_file_path)

        command = [
            self._python_executable,
            script_file,
            '--config', self._encoded_config,
            '--path', service_main_file_path
        ]

        process = subprocess.Popen(command)
        return process.pid

    def start_worker(self, service_main_file_path, service_pid):
        """
        Starts the service and starts the heartbeat detection process.
        Args:
            service_main_file_path : The path to the service main file.
            service_pid : The process ID of the newly started service process.
        Returns:
            int: The process ID of the newly started service process.
        """
        from pyrpc_schedule.main.worker import run_worker
        script_file = Path(run_worker.__file__).resolve()
        self.kill_process(script_file_path=script_file, target_file_path=service_main_file_path)

        command = [
            self._python_executable,
            script_file,
            '--config', self._encoded_config,
            '--path', service_main_file_path,
            '--service_pid', str(service_pid)
        ]
        process = subprocess.Popen(command)
        return process.pid

    def start_schedule(self):
        """
        Starts the schedule.
        Returns:
            int: The process ID of the newly started schedule process.
        """

        from pyrpc_schedule.services.schedule import run_schedule
        script_file = Path(run_schedule.__file__).resolve()
        self.kill_process(script_file_path=script_file, target_file_path=script_file)

        command = [
            self._python_executable,
            script_file,
            '--config', self._encoded_config
        ]

        process = subprocess.Popen(command)
        return process.pid

    def start(self):
        """
        Starts the service management process. Currently, this method is a placeholder
        and does not perform any actions.
        """
        self.start_heartbeat_detection()
        self.start_schedule()

        for service in self._service_list:
            service_main_file_path = Path(service.__file__).resolve()
            pid = self.start_service(service_main_file_path=service_main_file_path)
            self.start_worker(service_main_file_path=service_main_file_path, service_pid=pid)

        self.start_http_server()
