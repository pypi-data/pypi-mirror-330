# -*- coding: utf-8 -*-

import socket
import time
import functools
import json
from vwalila.redisfun import redisfun
from vwalila.utils import util_datetime, pf
from .utils.res_base import json_dumps
from vwalila.logger_helper import log

from .signals import (
    TaskCallSignalContext,
    before_task_called,
    after_task_called,
)
from vwalila import utils


def remove_db_session_after_task(task):
    @functools.wraps(task)
    def wrapper(*args, **kwargs):
        try:
            return task(*args, **kwargs)
        finally:
            pass
            # do some db connection close
            # DBSession.remove()

    return wrapper


def attach_signal_to_task(logger=None, debug=False):
    """Attach signal to task, invoked before/after task called."""

    ctx = TaskCallSignalContext()
    ctx.logger = logger or log

    def mid_func(task):
        @functools.wraps(task)
        def wrapper(self, *args, **kwargs):
            suffix = None
            ctx.task = self.name
            if suffix:
                ctx.task = "_".join((self.name, suffix))
            ctx.start_at = time.time()
            ctx.args, ctx.kwargs = args, kwargs
            before_task_called.send(ctx)
            # 20250301 兼容老版本,如果是web_chassis_py3调用,会传递http_call_ver参数
            b_need_redis = False
            if args and (isinstance(args, tuple) or (isinstance(args, list))):
                args_0_json = args[0]
                if isinstance(args_0_json, basestring):
                    args_0_json = json.loads(args_0_json)
                if isinstance(args_0_json, dict):
                    http_call_ver = args_0_json.get("http_call_ver", "")
                    if http_call_ver and http_call_ver == "need_redis_20250301":
                        b_need_redis = True
            # 用redis中转结果集,防止rabbitmq的编解码错误
            redis_key = "task_{}_{}_{}".format(util_datetime.get_utc_millis(), pf.create_random_str(5),
                                               pf.create_random_str(5))
            try:
                out = task(self, *args, **kwargs)
                ctx.end_at = time.time()
                if out and isinstance(out, basestring):
                    try:
                        out = json.loads(out)
                    except:
                        """"""
                if out and isinstance(out, dict):
                    out.update({"worker_do_ms": int(ctx.cost)})
                    out.update({"worker_ip": socket.gethostname()})
                    out = json_dumps(out)

                if b_need_redis:
                    redisfun.set_val(redis_key, out, 60)
                    return json_dumps({"redis_key": redis_key})
                else:
                    return out
            except Exception as exc:
                # 抓住所有 task 异常
                status_code = 100
                self.update_state(state="TASK-ERROR", meta={'exc': str(exc)})
                res_doc = {
                    "msg": str(exc),
                    "status": status_code,
                    "seqnum": utils.get_utc_millis(),
                    "body": {},
                    "status_code": status_code
                }
                if b_need_redis:
                    redisfun.set_val(redis_key, res_doc, 60)
                    return json_dumps({"redis_key": redis_key})
                else:
                    return json_dumps(res_doc)
            finally:
                after_task_called.send(ctx)

        return wrapper

    return mid_func


def attach_kwargs(**kwargs):
    """Attach attributes to task instance"""

    def wrapper(func):
        for attr, value in kwargs.iteritems():
            setattr(func, attr, value)
        return func

    return wrapper


def retry_decorator(ExceptionToCheck, max_tries, delay=5, backoff=2,
                    logger=None):
    def deco_retry(func):
        def wrapper(*args, **kwargs):
            mtries, mdelay = max_tries, delay
            while mtries > 1:
                try:
                    return func(*args, **kwargs)
                except ExceptionToCheck as exc:
                    msg = "%s, Retrying in %d seconds..." % (str(exc), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        log.warning(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return func(*args, **kwargs)

        return wrapper

    return deco_retry
