# -*- coding: utf-8 -*-

from . import mongfun
from vwalila.config import config

URL_MONGODB = config.get("mongodb", "")

mongodb_client = mongfun.MongodbClient(URL_MONGODB, connect_timeout_ms=5*1000)


def _get_xxx_xxx_xxx_tbl(db_name, collection_name, is_read_slave=False):
    return mongodb_client.get_mongodb_collection(
        db_name, collection_name, is_read_slave)


def get_mq_config_tbl(is_read_slave=False):
    return _get_xxx_xxx_xxx_tbl(
        "we_config_server_db", "mq_config", is_read_slave)


def get_monitor_worker_log_tbl(is_read_slave=False):
    return _get_xxx_xxx_xxx_tbl(
        "we_oops_db", "monitor_worker_log", is_read_slave)


def get_monitor_device_log_tbl(is_read_slave=False):
    return _get_xxx_xxx_xxx_tbl(
        "we_oops_db", "monitor_device_log", is_read_slave)



