# -*- coding: UTF-8 -*-

from vwalila.log_exc import send_log_exc_request
from vwalila.logger_helper import log
import socket
import traceback
import json
import thread
import requests
from vwalila import mq_config
from vwalila.redisfun import redisfun
from .utils import get_utc_millis
from .es_log import ESLog
from celery.exceptions import TimeoutError

METHOD_NOT_REGISTERED_MAX_RETRY = 0


def _send_no_result_task(job_name, job_data, retry=None):
    """
    不需要返回值的任务
    :param job_name:
    :param job_data:
    :return:
    """
    hosts_name, queue = mq_config.get_host_queue_by_func_name(job_name)
    if not hosts_name or not queue:
        thread.start_new_thread(
            send_log_exc_request,
            ({
                 "log_for": "timeout for NR",
                 "log_type": "error",
                 "memo": "{}: timeout for NR".format(
                     job_name),
             },))
        data = {'status': 998, 'body': {}, 'seqnum': get_utc_millis(),
                'msg': u"{}: timeout for NR".format(job_name)}
        return json.dumps(data)
    celery_app = mq_config.get_celery_app_by_hosts(hosts_name)
    if celery_app:
        async_result = celery_app.send_task(
            job_name, (job_data,), queue=queue)
        try:
            # 忽略结果，try以防有NotRegistered
            async_result.app.Task.ignore_result = True
            async_result.forget()
        except Exception as e:
            err_msg = traceback.format_exc()
            log.error(err_msg)
            if type(e).__name__ == "NotRegistered":
                if not retry:
                    retry = 0
                if retry < METHOD_NOT_REGISTERED_MAX_RETRY:
                    retry += 1
                    return _send_no_result_task(
                        job_name, job_data, retry=retry)
                thread.start_new_thread(
                    send_log_exc_request,
                    ({
                         "log_for": "timeout for NR",
                         "log_type": "error",
                         "memo": "{}: timeout for NR".format(
                             job_name),
                     },))
                data = {'status': 998, 'body': {}, 'seqnum': get_utc_millis(),
                        'msg': u"{}: timeout for NR".format(job_name)}
                return data

            # 非任务未注册的异常，不需要处理
            return {'status': 200, 'body': {}, 'seqnum': get_utc_millis(),
                    'msg': 'ok'}
        else:
            # 没有发生异常，直接返回
            return {'status': 200, 'body': {}, 'seqnum': get_utc_millis(),
                    'msg': 'ok'}


def send_task(job_name, job_data):
    return _send_no_result_task(job_name, job_data)


def send_and_get_task(job_name, job_data, is_inner_task=False):
    hosts_name, queue = mq_config.get_host_queue_by_func_name(job_name)
    if not hosts_name or not queue:
        thread.start_new_thread(
            send_log_exc_request,
            ({
                 "log_for": "timeout for NR",
                 "log_type": "error",
                 "memo": "{}: timeout for NR".format(
                     job_name),
             },))
        data = {'status': 998, 'body': {}, 'seqnum': get_utc_millis(),
                'msg': u"{}: timeout for NR".format(job_name)}
        return json.dumps(data)
    celery_app = mq_config.get_celery_app_by_hosts(hosts_name)
    if not celery_app:
        # 超时5次依旧没找到方法，则显示超时001，实则方法未注册
        thread.start_new_thread(
            send_log_exc_request,
            ({
                 "log_for": "timeout for NR",
                 "log_type": "error",
                 "memo": "{}: timeout for NR".format(
                     job_name),
             },))
        data = {'status': 998, 'body': {}, 'seqnum': get_utc_millis(),
                'msg': u"{}: timeout for NR".format(job_name)}
        return json.dumps(data)
    async_result = celery_app.send_task(job_name, (job_data,), queue=queue)

    try:
        if is_inner_task:
            import celery.result

            with celery.result.allow_join_result():
                result = async_result.get(timeout=15)
                async_result.forget()
                return result
        else:
            result = async_result.get(timeout=30)
            async_result.forget()
            return result
    except TimeoutError:
        # maybe redis restart
        mq_config.re_creat_celery_app_by_hosts(hosts_name)
        raise RuntimeError("Redis reconnect")


def send_then_wait(job_name, job_data, is_inner_task=False, retry=None):
    es_log = ESLog(fun_name=job_name)
    try:
        seqnum = job_data.get("seqnum", 0)  # 用户开始时间
        if seqnum:
            seqnum = int(seqnum)
        t_now = get_utc_millis()
        if 1.0 * (t_now - seqnum) / 1000 > 30:
            seqnum = t_now - 30000
        elif seqnum > t_now:
            seqnum = t_now

        job_data['seqnum'] = seqnum
        job_data['web_st'] = t_now  # web收到时间
        job_json = json.dumps(job_data)

        es_log.input = job_data
        result = send_and_get_task(job_name=job_name,
                                   job_data=job_json,
                                   is_inner_task=is_inner_task)
        if result:
            rtn = result
            rtnmap = json.loads(rtn)
            if isinstance(rtnmap, dict):
                redis_key = rtnmap.get("redis_key", '')
                if redis_key:
                    rtnmap = json.loads(redisfun.get_key(redis_key))
                    rtnmap.update({'call_redis_key': redis_key})

            worker_et = get_utc_millis()
            es_log.et = worker_et  # web处理完成时间
            es_log.output = rtnmap
            es_log.do_ms = 0
            if rtnmap and "worker_do_ms" in rtnmap:
                es_log.do_ms = rtnmap.get("worker_do_ms", 0)
                del rtnmap["worker_do_ms"]
            try:
                if "worker_ip" in rtnmap:
                    es_log.ip = rtnmap['worker_ip']
                    del rtnmap['worker_ip']
                if "_usi" in rtnmap:
                    del rtnmap['_usi']
                if "ip" in rtnmap:
                    del rtnmap['ip']
            except Exception:
                err_msg = traceback.format_exc()
                log.error(err_msg)

            return rtnmap
        else:
            thread.start_new_thread(
                send_log_exc_request,
                ({
                     "log_for": "timeout",
                     "log_type": "error",
                     "memo": "{}: timeout".format(
                         job_name),
                 },))
            tmp = "{}: timeout".format(job_name)
            return {'status': 110, 'body': {}, 'seqnum': seqnum, 'msg': tmp}
    except Exception as e:
        err_msg = traceback.format_exc()
        log.error(err_msg)
        es_log.output = {
            "msg": "traceback",
            "e_msg": e.message,
            "trace_info": err_msg,
            'status': 102,
            'seqnum': get_utc_millis(),
            'body': {}
        }
        if type(e).__name__ == "NotRegistered":
            if not retry:
                retry = 0
            if retry < METHOD_NOT_REGISTERED_MAX_RETRY:
                retry += 1
                return send_then_wait(job_name,
                                      job_data,
                                      is_inner_task=is_inner_task,
                                      retry=retry)
            # 超时5次依旧没找到方法，则显示超时001，实则方法未注册
            thread.start_new_thread(
                send_log_exc_request,
                ({
                     "log_for": "timeout for NR",
                     "log_type": "error",
                     "memo": "{}: timeout for NR".format(
                         job_name),
                 },))
            return {'status': 998, 'body': {}, 'seqnum': get_utc_millis(),
                    'msg': u"{}: timeout for NR".format(job_name)}
        thread.start_new_thread(
            send_log_exc_request,
            ({"log_for": "timeout",
              "log_type": "error",
              "memo": "{}: timeout".format(
                  job_name),
              },))
        data = {'status': 994, 'body': {}, 'seqnum': get_utc_millis(),
                'msg': str(e)}
        return data
    finally:
        log_map = es_log.gen_es_log_map()
        thread.start_new_thread(send_only_for_log, ('es_idx_log', log_map))


def send_only(job_name, job_data):
    try:
        if job_name == "es_idx_log":
            return send_only_for_log(job_name, job_data)
        if isinstance(job_data, dict):
            job_data = json.dumps(job_data)
        return send_task(job_name=job_name, job_data=job_data)
    except Exception as e:
        err_msg = traceback.format_exc()
        log.error(err_msg)
        data = {'status': 994, 'body': {}, 'seqnum': get_utc_millis(),
                'msg': str(e)}
        return data
    finally:
        """"""


def send_only_for_log(job_name, job_data):
    try:
        thread.start_new_thread(send_es_log_request, (job_data,))

    except Exception as e:
        err_msg = traceback.format_exc()
        log.error(err_msg)
        data = {'status': 998, 'body': {}, 'seqnum': get_utc_millis(),
                'msg': str(e)}
        return data
    finally:
        """"""


def log_error_to_es_with_fun(fun_name, in_dict, err_msg, usi=None):
    """
    记录日志到elasticsearch
    :param fun_name:
    :param in_dict:
    :param err_msg:
    :param usi:
    :return:
    """
    if not in_dict:
        in_dict = {
            "seqnum": get_utc_millis(),
            "web_st": get_utc_millis(),
        }
    log_map = dict()
    log_map['fun'] = fun_name
    log_map['et'] = get_utc_millis()
    log_map['in'] = in_dict

    out_dict = dict()
    out_dict['ip'] = socket.gethostname()
    out_dict['status'] = 100
    out_dict['msg'] = err_msg

    log_map['out'] = out_dict

    if usi and usi.id > 0:
        log_map['usi'] = {'id': usi.id, 'name': usi.name}

    send_only_for_log('es_idx_log', log_map)


def send_es_log_request(job_data):
    """

    :return:
    """
    from .config import config
    domain = config.get("es_log", "")
    out_dict = job_data.get("out", {})
    if "usi" not in job_data and "_usi" in out_dict:
        job_data['usi'] = out_dict.get("_usi", {})
    doc = job_data
    if not domain:
        return
    requests.post(url="{}/es_log_index".format(domain),
                  data=json.dumps(doc), headers={
            'Content-Type': 'application/json'}, timeout=5)
