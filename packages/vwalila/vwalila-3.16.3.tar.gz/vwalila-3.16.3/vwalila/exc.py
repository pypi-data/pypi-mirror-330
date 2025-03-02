# -*- coding: utf-8 -*-

import functools
from vwalila.logger_helper import log
import traceback
from vwalila import mqfun
from .utils import pf
from utils.res_base import ResBase
from celery.exceptions import SoftTimeLimitExceeded

STATUS_TOP_ERR = 500


class ApiBaseException(Exception):
    """Exception base class for web api"""
    status = STATUS_TOP_ERR

    def __init__(self, msg, status=None):
        super(ApiBaseException, self).__init__(msg)
        self.msg = msg
        if status:
            self.status = status

    def to_dict(self):
        rv = dict()
        rv['msg'] = self.msg
        rv['status'] = self.status
        return rv


class NotFoundException(ApiBaseException):
    status = 404


class InvalidParameter(ApiBaseException):
    status = 400


class UnknownError(ApiBaseException):
    status = 500


def exception_log(func):
    """
    异常捕捉
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper(worker, job):
        usi = None
        ret = None
        try:
            arg_count = func.func_code.co_argcount
            rcv = job
            if arg_count == 1:
                rcv = pf.json_to_map(job)
                ret = func(rcv)
            else:
                ret = func(worker, rcv)
        except NotFoundException as e:
            ret = ResBase(status=e.status, msg=e.message).to_json()
        except InvalidParameter as e:
            ret = ResBase(status=e.status, msg=e.message).to_json()
        except UnknownError as e:
            ret = ResBase(status=e.status, msg=e.message).to_json()
        except SoftTimeLimitExceeded as e:
            status = STATUS_TOP_ERR
            ret = ResBase(status=status, msg="exec task timeout").to_json()
        except Exception as e:
            status = STATUS_TOP_ERR
            if hasattr(e, 'status'):
                status = e.status
            msg = "Unknown error"
            if isinstance(e.message, (str, unicode)):
                msg = e.message
            ret = ResBase(status=status, msg=msg).to_json()
            err_msg = traceback.format_exc()
            log.error(err_msg)
            mqfun.log_error_to_es_with_fun(
                worker.name, pf.json_to_map(job), err_msg, usi)
        finally:
            return ret
    return wrapper

