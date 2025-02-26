# -*- encoding: utf-8 -*-
"""
@Time    : 2025/2/15
@Author  : yanPing
@Email   : zyphhxx@foxmail.com
"""

import os
import json
import logging

from pyrpc_schedule.meta.key import *
from pyrpc_schedule.utils import Cipher, SocketTools, SnowflakeID, Logger, FormatTime

from pyrpc_schedule.main import ServiceManagement
from pyrpc_schedule.rabbit import RabbitMQ, RpcProxy, Message
from pyrpc_schedule.databases import DatabaseTasks, DatabaseNodes, DatabaseServices

__version__ = '1.1.4'
current_dir = os.path.dirname(os.path.abspath(__file__))


class PyrpcSchedule:
    _instance = None

    _message = None
    _rabbitmq = None
    _rpc_proxy = None
    _database_tasks = None
    _database_nodes = None
    _database_services = None
    _service_management = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PyrpcSchedule, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def __init__(self, config: dict, is_cipher: bool = False):
        """
        PyrpcSchedule is a singleton class designed to manage and schedule RPC services.
        It initializes various components such as logging, message queues, RPC proxies,
        and databases based on the provided configuration.

        Example usage:
            import os

            current_dir = os.path.dirname(os.path.abspath(__file__))

            config = {
                'MONGODB_CONFIG': 'mongodb://scheduleAdmin:scheduleAdminPasswrd@127.0.0.1:27017',
                'RABBITMQ_CONFIG': 'amqp://scheduleAdmin:scheduleAdminPasswrd@127.0.0.1:5672',
                'ROOT_PATH': current_dir,
                'ADMIN_USERNAME': 'scheduleAdmin',
                'ADMIN_PASSWORD': 'scheduleAdminPasswrd',
                'DEFAULT_SCHEDULE_TIME': 10
            }

            ps = PyrpcSchedule(config=config)
        """
        if is_cipher:
            self._cipher = Cipher(private_key=config.get(CIPHER_PRIVATE_KEY_KEY))

    def _initialize(self, config, is_cipher=False):
        """
        Initialize the PyrpcSchedule instance.
        Args:
            config (dict): A dictionary containing the configuration for the instance.
            is_cipher (bool): A flag indicating whether the configuration is encrypted. Default is False.
        This method initializes the PyrpcSchedule instance by performing the following steps:

        """
        if is_cipher is False:
            self._config = config
        else:
            self._cipher = Cipher(private_key=config.get(CIPHER_PRIVATE_KEY_KEY))
            cipher_config = self.cipher_rsa_dec(ciphertext=config.get(CIPHER_CIPHERTEXT_KEY))
            config_dict = json.loads(cipher_config)
            config_dict[CONFIG_ROOT_PATH_KEY] = config[CONFIG_ROOT_PATH_KEY]
            self._config = config_dict

        self._ipaddr = SocketTools.get_ipaddr()
        self._datacenter_id: int = int(self._ipaddr.split('.')[-2])
        self._machine_id: int = int(self._ipaddr.split('.')[-1])

        self._snowflake = SnowflakeID(datacenter_id=self._datacenter_id, machine_id=self._machine_id)
        self._logger = Logger(config=self._config)

        self._format_time = FormatTime()

    def cipher_rsa_dec(self, ciphertext: str) -> bytes:
        """
        Decrypt the ciphertext using the RSA private key.

        Returns:
            bytes: The decrypted plaintext.
        """
        if self._cipher:
            return self._cipher.cipher_rsa_dec(ciphertext=ciphertext)
        raise Exception('Error Cipher Not Initialize')

    @property
    def format_time(self) -> FormatTime:
        """
        Get the FormatTime instance for formatting time.
        Returns:
            FormatTime: The FormatTime instance.
        """
        return self._format_time

    @property
    def generate_id(self) -> str:
        """
        Generate a unique ID using the Snowflake algorithm.
        Returns:
            str: The generated ID.
        """
        return self._snowflake.generate_id()

    @property
    def ipaddr(self) -> str:
        """
        Get the IP address of the current machine.
        Returns:
            str: The IP address.
        """
        return self._ipaddr

    def logger(self, filename: str = None, task_id: str = None) -> logging:
        """
        Get a logger instance for logging.
        Args:
            filename (str): The name of the log file.
            task_id (str, optional): The ID of the task. Defaults to None.
        Returns:
            logging: The logger instance.
        """
        if task_id and filename:
            return self._logger.logger(filename=filename, task_id=task_id)
        return self._logger.logger(filename=PROXY_NAME_KEY, task_id=PROXY_NAME_KEY)

    def stop_task(self, task_id: str):
        """
        Stop a task by the given task ID.
        Args:
            task_id (str): The unique identifier of the task.
        Returns:
            None
        """
        if self._database_tasks is None:
            self._database_tasks = DatabaseTasks(config=self._config, table=TABLE_NAME_TASKS)

        self._database_tasks.update_many(
            query={TASK_ID_KEY: task_id}, update_data={TASK_STATUS_KEY: TASK_STOP_STATUS_KEY})

    def retry_task(self, task_id: str):
        """
        Stop a task by the given task ID.
        Args:
            task_id (str): The unique identifier of the task.
        Returns:
            None
        """
        if self._database_tasks is None:
            self._database_tasks = DatabaseTasks(config=self._config, table=TABLE_NAME_TASKS)

        self._database_tasks.update_many(
            query={TASK_ID_KEY: task_id}, update_data={TASK_STATUS_KEY: TASK_WAIT_STATUS_KEY})

    def query_service_list(self, query: dict, field: dict, limit: int, skip_no: int):
        """
        Query the list of services from the database.
        Args:
            query (dict): The query criteria.
            field (dict): The fields to include in the result.
            limit (int): The maximum number of results to return.
            skip_no (int): The number of results to skip.
        Returns:
            list: The list of services.
        """
        if self._database_services is None:
            self._database_services = DatabaseServices(config=self._config, table=TABLE_NAME_SERVICES)
        return self._database_services.query_list_sort(query=query, field=field, limit=limit, skip_no=skip_no)

    def query_task_list(self, query: dict, field: dict, limit: int, skip_no: int):
        """
        Query the list of tasks from the database.
        Args:
            query (dict): The query criteria.
            field (dict): The fields to include in the result.
            limit (int): The maximum number of results to return.
            skip_no (int): The number of results to skip.
        Returns:
            list: The list of services.
        """
        if self._database_tasks is None:
            self._database_tasks = DatabaseTasks(config=self._config, table=TABLE_NAME_TASKS)
        return self._database_tasks.query_list_sort(query=query, field=field, limit=limit, skip_no=skip_no)

    def query_node_list(self, query: dict, field: dict, limit: int, skip_no: int):
        """
        Query the list of nodes from the database.
        Args:
            query (dict): The query criteria.
            field (dict): The fields to include in the result.
            limit (int): The maximum number of results to return.
            skip_no (int): The number of results to skip.
        Returns:
            list: The list of services.
        """
        if self._database_nodes is None:
            self._database_nodes = DatabaseNodes(config=self._config, table=TABLE_NAME_NODES)
        return self._database_nodes.query_list_sort(query=query, field=field, limit=limit, skip_no=skip_no)

    def query_task_status_by_task_id(self, task_id: str):
        """
        Retrieve the task status by the given task ID.

        Args:
            task_id (str): The unique identifier of the task.

        Returns:
            dict: The first document containing the task status information.
        """
        if self._database_tasks is None:
            self._database_tasks = DatabaseTasks(config=self._config, table=TABLE_NAME_TASKS)
        self._database_tasks.query_task_status_by_task_id(task_id=task_id)

    def update_work_max_process(self, worker_name: str, worker_ipaddr: str, worker_max_process: int):
        """
        Update the maximum number of processes for a worker identified by its name and IP address.

        Args:
            worker_name (str): The name of the worker.
            worker_ipaddr (str): The IP address of the worker.
            worker_max_process (int): The new maximum number of processes for the worker.

        Returns:
            None
        """
        if self._database_services is None:
            self._database_services = DatabaseServices(config=self._config, table=TABLE_NAME_SERVICES)

        self._database_services.update_work_max_process(
            worker_name=worker_name, worker_ipaddr=worker_ipaddr, worker_max_process=worker_max_process)

    def rabbit_send_message(self, queue: str, message: dict):
        """
        Send a message to the RabbitMQ server.
        Args:
            queue (str): The name of the queue to send the message to.
            message (dict): The message to be sent.
        Returns:
            None
        """
        if self._rabbitmq is None:
            self._rabbitmq = RabbitMQ(config=self._config)
        self._rabbitmq.send_message(queue=queue, message=message)

    def rabbit_receive_message(self, queue: str, callback):
        """
        Receive a message from the RabbitMQ server.
        Args:
            queue (str): The name of the queue to receive the message from.
            callback: The callback function to process the received message.
        Returns:
            dict: The received message.
        """
        if self._rabbitmq is None:
            self._rabbitmq = RabbitMQ(config=self._config)
        return self._rabbitmq.receive_message(queue=queue, callback=callback)

    def remote_call(self, service_name: str, method_name: str, **params):
        """
        Call a remote method on the specified service.
        Args:
            service_name (str): The name of the service to call.
            method_name (str): The name of the method to call on the service.
            **params: Additional parameters to pass to the method.
        Returns:
            The result of the remote method call.
        """
        if self._rpc_proxy is None:
            self._rpc_proxy = RpcProxy(config=self._config)
        return self._rpc_proxy.remote_call(service_name, method_name, **params)

    def proxy_call(self, service_name: str, method_name: str, **params):
        """
        Call a remote method on the specified service.
        Args:
            service_name (str): The name of the service to call.
            method_name (str): The name of the method to call on the service.
            **params: Additional parameters to pass to the method.
        Returns:
            The result of the remote method call.
        """
        if self._rpc_proxy is None:
            self._rpc_proxy = RpcProxy(config=self._config)

        _name = '{}_{}'.format(PROXY_NAME_KEY, service_name)
        self.logger().info('proxy service : {}'.format(_name))
        return self._rpc_proxy.remote_call(_name, method_name, **params)

    def service_registry(self, services: list):
        """
        Register a list of services.

        Args:
            services (list): A list of service instances to be registered.

        This method registers each service in the provided list with the service management module.

        Each service is expected to have a 'register' method that is called to complete the registration process.
        """
        if self._service_management is None:
            self._service_management = ServiceManagement(config=self._config)
        self._service_management.registry(services=services)

    def service_start(self):
        """
        Start the service management module.

        This method starts the service management module, which is responsible for managing and scheduling services.

        It calls the start method of the _service_management attribute,
        which is an instance of the ServiceManagement class.
        """
        if self._service_management is None:
            self._service_management = ServiceManagement(config=self._config)
        self._service_management.start()

    def send_message(self, queue: str, message: dict, weight: int = TASK_DEFAULT_WEIGHT) -> str:
        """
        Send a message to the queue.
        Args:
            queue (str): The name of the queue to send the message to.
            message (dict): The message to be sent.
            weight (int): The weight of the message. Default is 1.
        Returns:
            str: The task ID associated with the message.
        This method sends the provided message to the specified queue using the RabbitMQ instance.
        """
        if self._message is None:
            self._message = Message(config=self._config)

        return self._message.send_message(queue=queue, message=message, weight=weight)

    def submit_task(self, queue: str, message: dict, weight: int = TASK_DEFAULT_WEIGHT) -> str:
        """
        Submit a task to the specified queue.
        Args:
            queue (str): The name of the queue to submit the task to.
            message (dict): The message to be submitted as a task.
            weight (int): The weight of the task. Default is 1.
        Returns:
            str: The task ID associated with the submitted task.
        This method submits the provided task to the specified queue using the RabbitMQ instance.
        """
        if self._message is None:
            self._message = Message(config=self._config)
        return self._message.submit_task(queue=queue, message=message, weight=weight)
