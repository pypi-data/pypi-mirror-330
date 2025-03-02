# -*- coding: utf-8 -*-

import json
import random
import string


def str2int(value):
    """
    转换为整数
    :param value:
    :return:
    """
    try:
        return int(float(value))
    except Exception:
        # print e
        return 0


def to_json(doc):
    """
    转换成utf-8的json字符串
    :param doc:
    :return:
    """
    return json.dumps(doc)


def json_to_map(json_str):
    """
    json字符串转dict
    :param json_str:
    :return:
    """
    if isinstance(json_str, (str, unicode)):
        if json_str:
            return json.loads(json_str)
        else:
            return {}
    else:
        return json_str


def del_map_key(doc, key_name):
    """
    删除map中key
    :param doc:
    :param key_name:
    :return:
    """
    if not isinstance(doc, dict):
        return
    if not key_name:
        return
    if key_name in doc:
        del doc[key_name]


def del_map_key_list(doc, key_name_list):
    """
    删除map中key list
    :param doc:
    :param key_name_list:
    :return:
    """
    if not isinstance(doc, dict):
        return
    if not isinstance(key_name_list, (list, tuple, set)):
        return
    for key_name in key_name_list:
        del_map_key(doc, key_name)


def str_or_not_to_utf8(s):
    if not isinstance(s, (str, unicode)):
        s = str(s)
    if not isinstance(s, unicode):
        s = s.decode("utf-8")
    return s.encode("utf-8")


def create_random_str(num):
    """
    创建指定个数的随机字符串
    :param num:
    :return:
    """
    return ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(num))


if __name__ == "__main__":
    """"""


