# -*- encoding: utf-8 -*-

import time
import argparse

from pyrpc_schedule.meta.key import NODE_IPADDR_KEY, PROXY_NAME_KEY, TABLE_NAME_NODES

from pyrpc_schedule.databases import DatabaseNodes
from pyrpc_schedule.utils import load_config, Logger
from pyrpc_schedule.services.monitoring.system_info import NodeInfo


class HeartbeatDetection:
    """
    A class responsible for performing heartbeat detection.
    It continuously monitors the node's information and updates the database accordingly.
    """

    def __init__(self, config: dict):
        """
        Initialize the HeartbeatDetection instance.

        Args:
            config (dict): Configuration dictionary containing necessary settings.
        """

        self._logger = Logger(config=config).logger(filename=PROXY_NAME_KEY, task_id='HeartbeatDetection')
        self._database_nodes = DatabaseNodes(config=config, table=TABLE_NAME_NODES)

    def start(self):
        """
        Start the heartbeat detection process.
        This method runs in an infinite loop, periodically checking the node's information
        and updating the database. If an exception occurs, it logs the error and continues.
        """
        while True:
            try:

                node_info = NodeInfo()
                self._logger.info(f"{node_info.node}")

                self._database_nodes.update_many(
                    query={NODE_IPADDR_KEY: node_info.ipaddr},
                    update_data=node_info.node,
                    upsert=True
                )

                time.sleep(60)
            except Exception as e:
                self._logger.error(f"[HeartbeatDetection] {e}")
                time.sleep(60)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="run heartbeat detection script")

    parser.add_argument("--config", type=str, help="heartbeat detection config")
    args = parser.parse_args()

    configs = load_config(args.config)

    HeartbeatDetection(configs).start()
