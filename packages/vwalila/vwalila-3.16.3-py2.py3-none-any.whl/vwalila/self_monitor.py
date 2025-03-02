# -*- coding: utf-8 -*-
import json
import socket
import thread
import traceback

from .config import config
from celery.signals import (heartbeat_sent, worker_shutting_down,
                            worker_ready, worker_shutdown)
from vwalila.logger_helper import log
from log_exc import send_log_exc_request, send_log_info_request

WORKER_MQ_HOSTS = config.get("worker_mq_hosts", "")
AMQP_DOMAIN = config.get("rabbitmq", "")
REDIS_DOMAIN = config.get("redis", "")
CONFIG_SERVER_DOMAIN = config.get("config_server", "")
WORKER_NAME = config.get("worker_name", "")


def on_signal_heartbeat_sent(**kwargs):
    """"""
    thread.start_new_thread(report_info, ("heartbeat_report",))
    return


def on_signal_worker_ready(**kwargs):
    """"""
    thread.start_new_thread(report_info, ("worker_ready",))
    return


def on_signal_worker_shutting_down(**kwargs):
    """"""
    thread.start_new_thread(report_info, ("worker_shutting_down",))
    return


def on_signal_worker_shutdown(**kwargs):
    """"""
    # 结束，则主线程结束，所以不用thread
    report_info("worker_shutdown")


heartbeat_sent.connect(on_signal_heartbeat_sent)
worker_shutting_down.connect(on_signal_worker_shutting_down)
worker_shutdown.connect(on_signal_worker_shutdown)
worker_ready.connect(on_signal_worker_ready)


def report_info(report_type):
    """
    上报数据
    :return:
    """
    try:
        from .utils import tbl_fun
        from vwalila.utils import util_datetime
        branch_name = config.get("git_branch_name", "")
        git_ver = config.get("git_ver", "")

        machine_id = config.get("_machine_id", "")
        device_id = config.get("_device_id", "")
        machine_name = config.get("_machine_name", "")
        device_name = config.get("_device_name", "")
        data = {
            "report_type": report_type,
            "is_db_ok": 0,
            "is_redis_ok": 0,
            "is_worker_ok": 0,
            "is_rabbitmq_ok": 0,
            "c": util_datetime.get_utc_millis(),
            "m": util_datetime.get_utc_millis(),
            "host_name": socket.gethostname(),
            "project_name": WORKER_NAME,
            "worker_mq_hosts": WORKER_MQ_HOSTS,
            "instance_name": "___".join(
                ["celery@", socket.gethostname(), WORKER_NAME]),
            "git_branch": branch_name,
            "git_ver": git_ver,
            "machine_id": machine_id,
            "device_id": device_id,
            "machine_name": machine_name,
            "device_name": device_name,
        }
        if report_type not in ["worker_shutting_down", "worker_shutdown"]:
            data.update({
                "is_db_ok": is_db_ok(),
                "is_redis_ok": is_redis_ok(),
                "is_worker_ok": is_worker_ok(),
                "is_rabbitmq_ok": is_rabbitmq_ok(),
            })
        if report_type not in ["heartbeat_report"]:
            log.info(json.dumps(data))

        if report_type in ["worker_shutting_down", "worker_shutdown"]:
            send_log_exc_request({
                "log_for": report_type,
                "log_type": "error",
                "memo": report_type,
            })
        # 插入流水记录
        # tbl_fun.get_monitor_worker_log_tbl(False).insert_one(data)
        if device_id:
            doc_device = {}
            doc_device.update(data)
            if "_id" in doc_device:
                del doc_device["_id"]
            tbl_fun.get_monitor_device_log_tbl(False).update_one(
                {"machine_id": machine_id, "device_id": device_id,
                 "project_name": WORKER_NAME},
                {"$set": doc_device}, upsert=True)
    except Exception as e:
        err_msg = traceback.format_exc()
        log.error(err_msg)


def worker_cus_self_health_report(rcv):
    """
    自定义monitor
    :return:
    """
    try:
        from .utils import pf
        purge = pf.str2int(rcv.get("purge", "0"))

        if purge == 1:
            remove_task()

        body = {
            "worker_info": {
                "worker_mq_hosts": WORKER_MQ_HOSTS,
                "config_server": CONFIG_SERVER_DOMAIN,
                "worker_name": WORKER_NAME,
                "process_name": "___".join(["celery@", socket.gethostname(),
                                            WORKER_NAME])
            },
            "monitor_info": {
                "is_db_ok": is_db_ok(),
                "is_redis_ok": is_redis_ok(),
                "is_worker_ok": is_worker_ok(),
            }
        }

        from task_manage import task_manage
        app = task_manage.dic_all_broker_hosts.get(WORKER_MQ_HOSTS, None)

        stats = app.control.inspect().stats()
        conf = app.control.inspect().conf()
        report = app.control.inspect().report()
        active = app.control.inspect().active()

        body.update({
            "stats": stats,
            "conf": conf,
            "report": report,
            "active": active,
        })

        return body
    except Exception as e:
        err_msg = traceback.format_exc()
        log.error(err_msg)
        return {"msg": e.message}


def is_db_ok():
    """
    db连接是否OK
    :return:
    """
    try:
        from .utils import tbl_fun
        mq_info = tbl_fun.get_mq_config_tbl(False).find_one({}, {"_id": 1})
        if mq_info:
            return 1
        return 0
    except Exception as e:
        err_msg = traceback.format_exc()
        log.error(err_msg)
        return 0


def is_redis_ok():
    """
    redis是否ok
    :return:
    """
    try:
        from .redisfun import redisfun
        from vwalila.utils import util_datetime
        t_now = str(util_datetime.get_utc_millis())
        hostname = socket.gethostname()
        key = ":".join(["is_redis_ok", hostname])
        redisfun.set_val(key, t_now, sec=30)
        t_now_temp = redisfun.get_key(key)
        if t_now_temp and t_now_temp == t_now:
            return 1
        return 0
    except Exception as e:
        err_msg = traceback.format_exc()
        log.error(err_msg)
        return 0


def is_worker_ok():
    """
    worker是否OK
    :return:
    """
    try:
        from .task_manage import task_manage
        app = task_manage.dic_all_broker_hosts.get(WORKER_MQ_HOSTS, None)
        ping_list = app.control.ping(timeout=1)
        if not ping_list or not isinstance(ping_list, list):
            return 0
        self_name = "___".join(["celery@", socket.gethostname(), WORKER_NAME])
        for ping_info in ping_list:
            if ping_info.get(self_name, {}).get("ok", "") == "pong":
                return 1
        return 0
    except Exception as e:
        err_msg = traceback.format_exc()
        log.error(err_msg)
        return 0


def is_rabbitmq_ok():
    """
    连接rabbitmq是否正常
    :return:
    """
    try:
        from .task_manage import task_manage
        app = task_manage.dic_all_broker_hosts.get(WORKER_MQ_HOSTS, None)
        stats = app.control.inspect().stats()
        if stats:
            return 1

        # No running Celery workers were found.
        return 0
    except Exception as e:
        err_msg = traceback.format_exc()
        log.error(err_msg)
        return 0


def remove_task():
    """
    移除task
    :return:
    """
    try:
        from .task_manage import task_manage
        app = task_manage.dic_all_broker_hosts.get(WORKER_MQ_HOSTS, None)
        app.control.purge()
        send_log_info_request({
            "log_for": "vhosts_purge",
            "log_type": "info",
            "memo": "{} purge successfully...".format(WORKER_MQ_HOSTS),
        })
    except Exception as e:
        err_msg = traceback.format_exc()
        log.error(err_msg)
        send_log_exc_request({
            "log_for": "vhosts_purge",
            "log_type": "error",
            "memo": "{} purge failed...".format(WORKER_MQ_HOSTS),
        })
        """"""

if __name__ == "__main__":
    """"""
