# -*- coding: utf-8 -*-

import json
import traceback

import requests
from .redisfun import redisfun
from .config import config
from vwalila.logger_helper import log


REDIS_MQ_FUNC_NAME_HOSTS = "mq_func_name_hosts"

CONFIG_SERVER_DOMAIN = config.get("config_server", "")

CONFIG_SERVER_REFRESH = "/".join([CONFIG_SERVER_DOMAIN,
                                  "refresh_mq_config"])
CONFIG_SERVER_UPDATE = "/".join([CONFIG_SERVER_DOMAIN,
                                 "update_mq_config"])
CONFIG_SERVER_GET_MQ_CONFIG = "/".join([CONFIG_SERVER_DOMAIN,
                                        "get_mq_config"])
CONFIG_SERVER_GET_MQ_BROKER = "/".join([CONFIG_SERVER_DOMAIN,
                                        "get_mq_broker"])

REQUEST_TIMEOUT = 10

REQUEST_MAX_RETRY = 2


def get_mq_config(retry=None):
    """
    从config_server获取所有broker_list
    :param retry:
    :return:
    """
    res = None
    try:
        r = requests.get(url=CONFIG_SERVER_GET_MQ_CONFIG,
                         timeout=REQUEST_TIMEOUT)
        res = r.json()
    except Exception as e:
        err_msg = traceback.format_exc()
        log.error(err_msg)
    finally:
        if not res or res.get("status", 0) not in ["200", 200]:
            if not retry:
                retry = 0
            if retry < REQUEST_MAX_RETRY:
                retry += 1
                return get_broker_list_from_config_server(retry=retry)
            return None
        mq_config_info = res.get("body", {})
        return mq_config_info


def get_broker_list_from_config_server(retry=None):
    """
    从config_server获取所有broker_list
    :param retry:
    :return:
    """
    res = None
    try:
        r = requests.get(url=CONFIG_SERVER_GET_MQ_BROKER, timeout=REQUEST_TIMEOUT)
        res = r.json()
    except Exception as e:
        err_msg = traceback.format_exc()
        log.error(err_msg)
    finally:
        if not res or res.get("status", 0) not in ["200", 200]:
            if not retry:
                retry = 0
            if retry < REQUEST_MAX_RETRY:
                retry += 1
                return get_broker_list_from_config_server(retry=retry)
            return None
        broker_list = res.get("body", [])
        if not isinstance(broker_list, list):
            broker_list = []
        if "worker_other" not in broker_list:
            broker_list.append("worker_other")
        if "other" not in broker_list:
            broker_list.append("other")
        broker_list = list(set(broker_list))
        return broker_list


def update_func_list_to_config_server(func_list, retry=None):
    """
    把本地function更新到config server
    :param func_list:
    :param retry:
    :return:
    """
    if not func_list:
        return None

    data = {
        "func_list": func_list
    }
    res = None
    try:
        r = requests.post(url=CONFIG_SERVER_UPDATE,
                          json=data, timeout=REQUEST_TIMEOUT)
        res = r.json()
    except Exception as e:
        err_msg = traceback.format_exc()
        log.error(err_msg)
    finally:
        if not res or res.get("status", 0) not in ["200", 200]:
            if not retry:
                retry = 0
            if retry < REQUEST_MAX_RETRY:
                retry += 1
                return update_func_list_to_config_server(func_list,
                                                         retry=retry)
            return None
        return True


def refresh_redis_mq_config(retry=None):
    """
    发送指令让config server更新redis
    :param retry:
    :return:
    """
    res = None
    try:
        r = requests.get(url=CONFIG_SERVER_REFRESH, timeout=REQUEST_TIMEOUT)
        res = r.json()
    except Exception as e:
        err_msg = traceback.format_exc()
        log.error(err_msg)
    finally:
        if not res or res.get("status", 0) not in ["200", 200]:
            if not retry:
                retry = 0
            if retry < REQUEST_MAX_RETRY:
                retry += 1
                return get_broker_list_from_config_server(retry=retry)
            return None
        return True


def get_celery_app_by_hosts(hosts_name, times=None):
    """
    根据hosts_name，获取mq hosts 实例
    :param hosts_name:
    :param times:
    :return:
    """
    if not hosts_name:
        return None
    # must import lazily
    from task_manage import task_manage
    celery_app = task_manage.dic_all_broker_hosts.get(hosts_name, None)
    if not celery_app:
        # 找不到，说明本地可能不是最新的，有worker没上报过方法映射
        task_manage.register_all_celery_app(force_hosts=hosts_name)
        if not times:
            times = 1
        if times < 2:
            # 最多执行1次
            times += 1
            return get_celery_app_by_hosts(hosts_name=hosts_name, times=times)
        return None
    return celery_app


def get_celery_app_by_func_name(func_name, times=None):
    """
    根据func_name，获取mq hosts 实例
    :param func_name:
    :param times:
    :return:
    """
    if not func_name:
        return None

    dic_all_func_name_hosts = redisfun.get_key(REDIS_MQ_FUNC_NAME_HOSTS)
    if not dic_all_func_name_hosts:
        # 发送远程更新redis指令
        refresh_redis_mq_config()
        if not times:
            times = 1
        if times < 2:
            # 最多执行1次
            times += 1
            return get_celery_app_by_func_name(func_name=func_name,
                                               times=times)
        return None

    dic_all_func_name_hosts = json.loads(dic_all_func_name_hosts)
    func_info = dic_all_func_name_hosts.get(func_name, {})
    hosts_name = func_info.get("hosts", "")
    if not hosts_name:
        # 说明有worker 没上报过方法映射
        return None
    return get_celery_app_by_hosts(hosts_name)


def get_host_queue_by_func_name(func_name, times=None):
    """
    根据func_name，获取mq hosts 实例
    :param func_name:
    :param times:
    :return:
    """
    if not func_name:
        return None, None

    dic_all_func_name_hosts = redisfun.get_key(REDIS_MQ_FUNC_NAME_HOSTS)
    if not dic_all_func_name_hosts:
        # 发送远程更新redis指令
        refresh_redis_mq_config()
        if not times:
            times = 1
        if times < 2:
            # 最多执行1次
            times += 1
            return get_celery_app_by_func_name(func_name=func_name,
                                               times=times)
        return None, None

    dic_all_func_name_hosts = json.loads(dic_all_func_name_hosts)
    func_info = dic_all_func_name_hosts.get(func_name, {})
    hosts_name = func_info.get("hosts", "")
    queue = func_info.get("queue", "")
    if not hosts_name or not queue:
        # 说明有worker 没上报过方法映射
        return None, None
    return hosts_name, queue


def get_dic_all_func_name_hosts_from_redis(times=None):
    """
    从redis中取所有的func_name映射hosts
    :return:
    """
    dic_all_func_name_hosts = redisfun.get_key(REDIS_MQ_FUNC_NAME_HOSTS)
    if not dic_all_func_name_hosts:
        # 发送远程更新redis指令
        refresh_redis_mq_config()
        if not times:
            times = 1
        if times < 2:
            # 最多执行1次
            times += 1
            return get_dic_all_func_name_hosts_from_redis(times=times)
        return None
    dic_all_func_name_hosts = json.loads(dic_all_func_name_hosts)
    return dic_all_func_name_hosts


def re_creat_celery_app_by_hosts(hosts_name):
    """
    某些情况下，redis可能断连，需要重建celery_app
    根据hosts_name，获取mq hosts 实例
    :param hosts_name:
    :return:
    """
    from task_manage import task_manage

    broker_url = "".join((task_manage.mq_domain, hosts_name))
    celery_app = task_manage.reg_app_celery(broker=broker_url)
    task_manage.dic_all_broker_hosts[hosts_name] = celery_app
