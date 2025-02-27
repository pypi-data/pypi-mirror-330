# -*- encoding: utf-8 -*-

import json
import pika
import logging

from pyrpc_schedule.meta.key import CONFIG_RABBIT_KEY


class RabbitMQ:
    """
    A singleton class for interacting with RabbitMQ. It manages the connection,
    queue creation, message sending and receiving operations.
    """
    _instance = None

    _config = None
    _channel = None

    def __new__(cls, *args, **kwargs):
        """
        Override the __new__ method to implement the singleton pattern.
        If the instance doesn't exist, create a new one and initialize it.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            _RabbitMQ: The singleton instance of _RabbitMQ.
        """
        if not cls._instance:
            cls._instance = super(RabbitMQ, cls).__new__(cls)
        return cls._instance

    def __init__(self, config: dict = None):
        """
        Initialize the _RabbitMQ instance.
        Args:
            config (dict): Configuration dictionary for RabbitMQ.
        """
        if self._config is None:
            self._config = config.get(CONFIG_RABBIT_KEY)

    def _mq_channel(self):
        """
        Create and return a new RabbitMQ channel.

        Returns:
            pika.channel.Channel: A new channel object for interacting with RabbitMQ.
        """
        if self._channel is None:
            host, port, user, passwd = self._parse_config()

            credentials = pika.PlainCredentials(user, passwd)
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host, port=port, virtual_host='/', credentials=credentials, heartbeat=0))
            self._channel = connection.channel()
        return self._channel

    def _parse_config(self):
        """
        Parse the RabbitMQ configuration string to extract host, port, user and password.

        Returns:
            tuple: A tuple containing host (str), port (int), user (str) and password (str).
        """
        parts = self._config.split('@')
        user_passwd = parts[0].split('//')[1]
        host_port = parts[1]

        user, passwd = user_passwd.split(':')
        host, port = host_port.split(':')

        return host, int(port), user, passwd

    def _create_queue(self, queue: str):
        """
        Create a queue in RabbitMQ. If an error occurs during creation, log the error.

        Args:
            queue (str): The name of the queue to create.

        Returns:
            pika.channel.Channel: The channel object used to create the queue.
        """
        _mq_channel = self._mq_channel()
        try:
            _mq_channel.queue_declare(queue=queue)
        except Exception as e:
            logging.error(e)

        return _mq_channel

    def send_message(self, queue: str, message: dict):
        """
        Send a message to a specified queue in RabbitMQ.

        Args:
            queue (str): The name of the queue to send the message to.
            message (dict): The message to send. It will be converted to a JSON string if it's not already.
        """
        _mq_channel = self._create_queue(queue=queue)
        if not isinstance(message, str):
            message = json.dumps(message)
        _mq_channel.basic_publish(exchange='', routing_key=queue, body=message)

    def receive_message(self, queue: str, callback):
        """
        Start consuming messages from a specified queue in RabbitMQ.

        Args:
            queue (str): The name of the queue to consume messages from.
            callback (callable): The callback function to handle received messages.
        """
        _mq_channel = self._create_queue(queue=queue)
        _mq_channel.basic_consume(on_message_callback=callback, queue=queue, auto_ack=False)
        _mq_channel.start_consuming()

    def close(self):
        """
        Close the RabbitMQ connection.
        """
        self._channel.close()
