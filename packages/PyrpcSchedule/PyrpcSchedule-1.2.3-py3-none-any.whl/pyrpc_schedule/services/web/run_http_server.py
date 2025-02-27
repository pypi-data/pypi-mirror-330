# -*- encoding: utf-8 -*-

import os
import sys
import argparse
from datetime import timedelta
from flask import Flask, render_template, request, jsonify, session

from pyrpc_schedule.meta.key import ADMIN_USERNAME_KEY, ADMIN_PASSWORD_KEY, DEFAULT_USERNAME_KEY, \
    DEFAULT_PASSWORD_KEY, ROOT_PATH_KEY, SERVICE_IPADDR_KEY, SERVICE_NAME_KEY, WORKER_MAX_PROCESS_KEY, \
    PROXY_NAME_KEY, TABLE_NAME_TASKS, TABLE_NAME_SERVICES, TABLE_NAME_NODES, TASK_ID_KEY, TASK_STATUS_KEY, \
    TASK_WAIT_STATUS_KEY, TASK_STOP_STATUS_KEY

from pyrpc_schedule.utils import load_config, Logger, SocketTools
from pyrpc_schedule.databases import DatabaseTasks, DatabaseServices, DatabaseNodes

current_dir = os.path.dirname(os.path.abspath(__file__))


class HttpServer:
    """
    A class representing an HTTP server.
    """

    def __init__(self, config: dict):
        """
        Initialize the HTTP server.
        Args:
            config (dict): A dictionary containing the server configuration.
        """

        self._logger = Logger(config=config).logger(filename=PROXY_NAME_KEY, task_id='HttpServer')
        self._database_tasks = DatabaseTasks(config=config, table=TABLE_NAME_TASKS)
        self._database_service = DatabaseServices(config=config, table=TABLE_NAME_SERVICES)
        self._database_nodes = DatabaseNodes(config=config, table=TABLE_NAME_NODES)

        self._username = config.get(ADMIN_USERNAME_KEY, DEFAULT_USERNAME_KEY)
        self._password = config.get(ADMIN_PASSWORD_KEY, DEFAULT_PASSWORD_KEY)

        self._app = Flask(__name__, template_folder=os.path.join(current_dir, 'templates'))
        self._app.config['SECRET_KEY'] = 'PyrpcSchedule'
        self._app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
        self._app.config['DEBUG'] = False

        self._logger.info('HttpServer init start')
        self._add_url_rule()
        port = 5673
        while True:
            if SocketTools().is_port_open(port):
                break
            port += 1

        self._app.run(host='0.0.0.0', port=port)

    def _add_url_rule(self):
        """
        Adds URL rules to the Flask application.
        """
        self._app.add_url_rule('/', 'index', self.index)
        self._app.add_url_rule('/login', 'login', self.login, methods=['GET', 'POST', 'DELETE'])
        self._app.add_url_rule('/resource_management', 'resource_management',
                               self.resource_management, methods=['GET', 'POST'])
        self._app.add_url_rule('/server_management', 'server_management',
                               self.server_management, methods=['GET', 'POST', 'PUT'])
        self._app.add_url_rule('/task_management', 'task_management',
                               self.task_management, methods=['GET', 'POST', 'PUT', 'DELETE'])
        self._app.add_url_rule('/sub_task_management', 'sub_task_management',
                               self.sub_task_management, methods=['GET', 'POST'])

    def index(self):
        """
        Renders the index template.
        Returns:
            str: The rendered index template.
        """
        if session.get('is_login') == f'{self._username}_{self._password}':
            return render_template('home.html')
        return render_template('login.html')

    def login(self):
        """
        Handles the login functionality.
        Returns:
            str: The rendered login template.
        """

        if request.method == 'POST':
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            if username == self._username and password == self._password:
                session['is_login'] = f'{self._username}_{self._password}'
                return jsonify(success=True)
            else:
                return jsonify(success=False, message="Invalid username or password")
        if request.method == "DELETE":
            session['is_login'] = False
            return render_template('login.html')
        return render_template('login.html')

    def resource_management(self):
        """
        Handles the resource management functionality.
        Returns:
            str: The rendered resource management template.
        """
        if session.get('is_login') == f'{self._username}_{self._password}':
            if request.method == 'POST':
                limit = request.json.get('limit')
                page = request.json.get('page')
                ipaddr = request.json.get('ipaddr')

                skip_no = int(limit) * (int(page) - 1)
                query = {}
                if ipaddr and ipaddr != '':
                    query.setdefault("ipaddr", ipaddr)

                count, data = self._database_nodes.query_list_sort(
                    query=query, field={'_id': 0}, limit=limit, skip_no=skip_no)
                return {'code': 0, 'msg': 'ok', 'count': count, 'data': data}

            return render_template('resource_management.html')
        return render_template('login.html')

    def server_management(self):
        """
        Handles the server management functionality.
        Returns:
            str: The rendered server management template.
        """
        if session.get('is_login') == f'{self._username}_{self._password}':
            if request.method == 'POST':
                limit = request.json.get('limit')
                page = request.json.get('page')

                service_name = request.json.get(SERVICE_NAME_KEY)
                service_ipaddr = request.json.get(SERVICE_IPADDR_KEY)

                skip_no = int(limit) * (int(page) - 1)
                query = {}
                if service_ipaddr and service_ipaddr != '':
                    query.setdefault(SERVICE_IPADDR_KEY, service_ipaddr)

                if service_name and service_name != '':
                    query.setdefault(SERVICE_NAME_KEY, service_name)

                count, data = self._database_service.query_list_sort(
                    query=query, field={'_id': 0}, limit=limit, skip_no=skip_no)
                return {'code': 0, 'msg': 'ok', 'count': count, 'data': data}

            if request.method == 'PUT':
                service_name = request.json.get(SERVICE_NAME_KEY)
                service_ipaddr = request.json.get(SERVICE_IPADDR_KEY)
                worker_max_process = request.json.get(WORKER_MAX_PROCESS_KEY)

                self._database_service.update_work_max_process(
                    worker_name=service_name, worker_ipaddr=service_ipaddr, worker_max_process=worker_max_process)
                return {'code': 0, 'msg': 'update successful'}

            return render_template('server_management.html')
        return render_template('login.html')

    def task_management(self):
        """
        Handles the task management functionality.
        Returns:
            str: The rendered task management template.
        """
        if session.get('is_login') == f'{self._username}_{self._password}':
            if request.method == 'POST':
                page = request.json.get('page')
                limit = request.json.get('limit')

                task_id = request.json.get('task_id')
                task_status = request.json.get('task_status')

                skip_no = int(limit) * (int(page) - 1)
                query = {'body.is_sub_task': False}
                if task_id and task_id != '':
                    query.setdefault("task_id", task_id)

                if task_status and task_status != '':
                    query.setdefault("status", task_status)

                count, data = self._database_tasks.query_list_sort(
                    query=query, field={'_id': 0}, limit=limit, skip_no=skip_no)

                return {'code': 0, 'msg': 'ok', 'count': count, 'data': data}

            if request.method == 'PUT':
                task_id = request.json.get('task_id')
                self._database_tasks.update_many(
                    query={TASK_ID_KEY: task_id}, update_data={TASK_STATUS_KEY: TASK_WAIT_STATUS_KEY})

            if request.method == 'DELETE':
                task_id = request.json.get('task_id')
                self._database_tasks.update_many(
                    query={TASK_ID_KEY: task_id}, update_data={TASK_STATUS_KEY: TASK_STOP_STATUS_KEY})

            return render_template('task_management.html')
        return render_template('login.html')

    def sub_task_management(self):
        """
        Handles the subtask management functionality.
        Returns:
            str: The rendered task management template.
        """
        if session.get('is_login') == f'{self._username}_{self._password}':
            if request.method == 'POST':
                page = request.json.get('page')
                limit = request.json.get('limit')
                task_id = request.json.get('task_id')
                source_id = request.json.get('source_id')

                skip_no = int(limit) * (int(page) - 1)
                query = {'body.source_id': source_id}
                if task_id and task_id != '':
                    query.setdefault("task_id", task_id)

                count, data = self._database_tasks.query_list_sort(
                    query=query, field={'_id': 0}, limit=limit, skip_no=skip_no)
                return {'code': 0, 'msg': 'ok', 'count': count, 'data': data}
            return render_template('task_management.html')
        return render_template('login.html')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="run service script")

    parser.add_argument("--config", type=str, help="service config")
    parser.add_argument("--path", type=str, help="service path")
    args = parser.parse_args()

    configs = load_config(args.config)

    sys.path.append(configs[ROOT_PATH_KEY])

    HttpServer(config=configs)
