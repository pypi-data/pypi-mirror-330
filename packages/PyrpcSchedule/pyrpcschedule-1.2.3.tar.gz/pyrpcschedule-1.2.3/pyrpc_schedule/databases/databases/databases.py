# -*- encoding: utf-8 -*-

from pyrpc_schedule.databases.client.client import MongoClient


class DatabaseTasks(MongoClient):
    """
    DatabaseTasks class is used to manage database task - related operations.
    """


class DatabaseNodes(MongoClient):
    """
    DatabaseNodes class is used to manage database nodes.
    """


class DatabaseServices(MongoClient):
    """
    DatabaseServices class is used to manage database services - related operations.
    """
