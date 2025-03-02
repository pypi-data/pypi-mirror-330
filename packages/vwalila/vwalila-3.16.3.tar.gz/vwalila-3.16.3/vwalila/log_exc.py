# -*- coding: utf-8 -*-

import json
import requests
from vwalila.logger_helper import log


def send_log_exc_request(data):
    """
    data = {
        "log_for": ["config_server", ],
        "log_type": ["error", "info", "exit"],
        "memo": "",
    }
    :return:
    """
    from .config import config
    domain = config.get("es_log", "")
    if not domain:
        return

    machine_id = config.get("_machine_id", "")
    device_id = config.get("_device_id", "")
    machine_name = config.get("_machine_name", "")
    device_name = config.get("_device_name", "")
    doc = {}
    doc.update({
        "machine_id": machine_id,
        "device_id": device_id,
        "machine_name": machine_name,
        "device_name": device_name,
    })
    if data:
        doc.update(data)
    r = requests.post(url="{}/log_exc".format(domain),
                  data=json.dumps(doc), headers={
            'Content-Type': 'application/json'}, timeout=5)
    log.info(r.text)


def send_log_info_request(data):
    """
    data = {
        "log_for": ["config_server", ],
        "log_type": ["error", "info", ""]
    }
    :return:
    """
    from .config import config
    domain = config.get("es_log", "")
    if not domain:
        return

    machine_id = config.get("_machine_id", "")
    device_id = config.get("_device_id", "")
    machine_name = config.get("_machine_name", "")
    device_name = config.get("_device_name", "")
    doc = {}
    doc.update({
        "machine_id": machine_id,
        "device_id": device_id,
        "machine_name": machine_name,
        "device_name": device_name,
    })
    if data:
        doc.update(data)
    r = requests.post(url="{}/log_info".format(domain),
                  data=json.dumps(doc), headers={
            'Content-Type': 'application/json'}, timeout=5)
    log.info(r.text)


if __name__ == "__main__":
    """"""
