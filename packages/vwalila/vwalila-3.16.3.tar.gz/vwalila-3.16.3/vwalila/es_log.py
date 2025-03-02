# -*- coding: utf-8 -*-

import socket
from .utils import get_utc_millis


class ESLog(object):
    def __init__(self, fun_name, et=None, input=None,
                 output=None, do_ms=None, ip=None):
        """"""
        self.fun = fun_name
        self.et = et or get_utc_millis()
        self.input = input or {}
        self.output = output or {}
        self.do_ms = do_ms or 0
        self.ip = ip or socket.gethostname()

    def gen_es_log_map(self):
        """
        生成ES log
        :return:
        """
        log_map = {
            "fun": self.fun,
            "et": self.et,
            "in": self.input,
            "out": self.output,
            "do_ms": self.do_ms,
            "ip": self.ip,
        }
        return log_map
