# -*- coding: utf-8 -*-

import decimal
import json
from bson import ObjectId

from .util_datetime import get_utc_millis


class ResBase(object):
    def __init__(self, status=200, msg="ok", body=None, seq_num=None):
        self.status = status
        self.msg = msg
        self.seq_num = seq_num or get_utc_millis()
        self.body = body or {}

    def to_dict(self, is_obj2str=False):
        """
        is_obj2str 适用场景：如果body中含有ObjectId之类的值，但是又想生成dict，
        可以加此参数，可以过滤掉ObjectId
        :param is_obj2str:
        :return:
        """
        if is_obj2str:
            self.body = json.loads(json_dumps(doc=self.body))
        return {
            "status": self.status,
            "msg": self.msg,
            "seqnum": self.seq_num,
            "body": self.body,
        }

    def to_json(self):
        return json_dumps(self.to_dict())

    def to_json_exc(self, err_code, err_msg=None):
        self.status = err_code
        self.msg = err_msg
        return json_dumps(self.to_dict())

    def to_json_error(self, err_code, err_msg):
        return self.to_json_exc(err_code, err_msg)


class PageInfo(object):
    def __init__(self, total=0, page_size=0, current_id=None, page=0):
        # 分页类型，page_number，item_id 两种，page一定是从1开始
        self.page_style = "item_id"

        if not current_id and page > 0:
            self.page_style = "page_number"

        self.total = total
        self.page_size = page_size

        # 页码翻页模式
        self.current_page = 0
        self.previous_page = 0
        self.next_page = 0

        if self.page_style == "page_number":
            self.current_page = page

        # id大小翻页模式
        self.current_id = current_id or ""

        # page_info
        self.page_info = {}

    def to_dict(self):
        """
        :return:
        """
        self.page_info = {
            "total": self.total,
            "page_size": self.page_size,
        }

        self.page_info.update({"current": self.current_id})

        if self.page_style == "page_number":
            self.page_info.update({"current": self.current_page})

        return self.page_info


class DecimalEncode(json.JSONEncoder):
    """
    Workaround to encode `Decimal` and ObjectId.

    See:
    https://github.com/simplejson/simplejson/issues/34#issuecomment-5622506
    """

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        elif isinstance(o, ObjectId):
            return str(o)
        return super(DecimalEncode, self).default(o)


def json_dumps(doc):
    try:
        return json.dumps(doc, cls=DecimalEncode)
    except ValueError:
        return ""
