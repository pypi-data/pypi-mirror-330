# -*- encoding: utf-8 -*-
import socket

from pyrpc_schedule.meta.key import SOCKET_BIND_IP, SOCKET_BIND_PORT, SOCKET_SHUTDOWN_SLEEP


class SocketTools:
    """
    A utility class that provides static methods for socket-related operations.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Override the __new__ method to implement the singleton pattern.
        If the instance does not exist, create a new instance and initialize it;
        otherwise, return the existing instance.
        :param args: Positional arguments
        :param kwargs: Keyword arguments
        :return: Singleton instance
        """

        if cls._instance is None:
            cls._instance = super(SocketTools, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def get_ipaddr() -> str:
        """
        Retrieves the IP address of the current machine by establishing a UDP connection
        to the specified IP and port.

        Returns:
            str: The IP address of the current machine.
        """
        socket_tools = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_tools.connect((SOCKET_BIND_IP, SOCKET_BIND_PORT))
        return socket_tools.getsockname()[0]

    @staticmethod
    def is_port_open(port: int, ip_addr: str = None) -> bool:
        """
        Checks if a specified port on a given IP address is open by attempting to establish
        a TCP connection.

        Args:
            ip_addr (str): The IP address to check.
            port (int): The port number to check.

        Returns:
            bool: True if the port is closed, False if the port is open.
        """
        if ip_addr is None:
            ip_addr = SocketTools.get_ipaddr()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip_addr, int(port)))
            s.shutdown(SOCKET_SHUTDOWN_SLEEP)
            return False
        except IOError:
            return True
