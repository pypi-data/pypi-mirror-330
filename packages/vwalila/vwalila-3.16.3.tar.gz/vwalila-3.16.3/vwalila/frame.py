# -*- coding: utf-8 -*-
import traceback

import os
from pyfiglet import Figlet
from vwalila.logger_helper import log

from .config import config, FUNC_MONITOR_NAME, FUNC_MONITOR_PREFIX
from . import mq_config

WORKER_MQ_HOSTS = config.get("worker_mq_hosts", "")
AMQP_DOMAIN = config.get("rabbitmq", "")
REDIS_DOMAIN = config.get("redis", "")
CONFIG_SERVER_DOMAIN = config.get("config_server", "")
WORKER_NAME = config.get("worker_name", "")


if not AMQP_DOMAIN:
    log.error(u"未指定rabbitmq地址")
    assert u"未指定rabbitmq地址"

if not REDIS_DOMAIN:
    log.error(u"未指定redis地址")
    assert u"未指定redis地址"

if not CONFIG_SERVER_DOMAIN:
    log.error(u"未指定config_server地址")
    assert u"未指定config_server地址"


class Frame(object):
    def __init__(self, plugin_path=None):
        """
        :plugin_path: 插件路径
        :task_list: 已注册的 task 列表,用来判断 task 名是否冲突
        """

        self.plugin_path = plugin_path or 'worker'
        self.plugin_list = []
        self.task_list = {}
        self.function_list = []

    def _load_plugin(self):
        """加载插件的方法
        """
        assert os.path.isdir(self.plugin_path), '未找到插件目录'
        self.plugin_list.extend(
            [plugin for plugin in os.listdir(self.plugin_path)
             if os.path.isdir('/'.join([self.plugin_path, plugin]))
             if os.path.isfile('/'.join([self.plugin_path, plugin, 'main.py']))
             ])

        assert self.plugin_list, '未找到插件'
        # 遍历插件路径下的插件
        for plugin in self.plugin_list:
            # 加载 worker.plugin.main
            submodule = __import__(
                '.'.join([self.plugin_path, plugin, 'main']))
            # 获得 worker.plugin.main 对象
            submodule_obj = getattr(submodule, plugin).main
            submodule_func = [
                # 列出对象中的函数和导入的模块
                func for func in dir(submodule_obj)
                # 忽略私有函数
                if func[0] != '_'
                # 确认是函数而不是模块
                if hasattr(getattr(submodule_obj, func), '__call__')
                if hasattr(getattr(submodule_obj, func), 'func_code')
                # 确认是本地模块而不是第三方模块
                if getattr(getattr(submodule_obj, func), '__module__').split(
                    '.')[:2] == [self.plugin_path, plugin]
            ]
            assert submodule_func, '没有可加载的 task'
            # 遍历函数
            for func in submodule_func:
                # 函数对象
                task_obj = getattr(submodule_obj, func)
                # 函数名作为 task 名
                task_name = task_obj.__name__
                # 如果和已注册的 task 同名
                if task_name in self.task_list:
                    log.info(u'{} is existed in the {}'.format(
                        task_name, self.task_list[task_name]))
                else:
                    # 将 worker 名放入列表 用来检查worker名冲突
                    self.task_list[task_name] = plugin
                    self.function_list.append(task_obj)

        is_worker = config.get("is_worker", 0)
        if is_worker == 1:
            from vwalila.self_monitor import worker_cus_self_health_report
            self.function_list.append(worker_cus_self_health_report)

    def run(self):
        """走你.
        """
        try:
            # self._boring()
            self._load_plugin()

        except KeyboardInterrupt:
            log('\rShutdown ...')
            log('Bye ~')
        except Exception as e:
            err_msg = traceback.format_exc()
            log.error(err_msg)
            raise e

    def _boring(self):
        """"""
        f = Figlet(width=150)
        font = "letters"
        f.setFont(font=font)
        log(f.renderText(WORKER_NAME))


# 批量更新接口到config_server
def update_config_server(function_obj_list):
    if not function_obj_list:
        log.error(u"没有可加载的 task")
        assert '没有可加载的 task'
    if not WORKER_MQ_HOSTS:
        log.error(u"未指定项目vhosts")
        assert '未指定项目vhosts'
    update_mq_list = []
    for func in function_obj_list:
        queue = "default"
        func_name = func.__name__
        if func_name == FUNC_MONITOR_NAME:
            func_name = "___".join([func_name, FUNC_MONITOR_PREFIX])
            queue = "___".join(["monitor", FUNC_MONITOR_PREFIX])
        doc = {
            "func_name": func_name,
            "hosts": WORKER_MQ_HOSTS,
            "queue": queue,
        }
        update_mq_list.append(doc)
    if update_mq_list:
        if mq_config.update_func_list_to_config_server(update_mq_list):
            log.info(u"finish upload functions successfully.")
        else:
            from log_exc import send_log_exc_request
            send_log_exc_request({
                "log_for": "function_reg",
                "log_type": "error",
                "memo": "connect config_server error.",
            })
            log.error("upload functions failed")
            raise

function_list = []
if os.path.isdir("worker"):
    config.update({"is_worker": 1})
    frame = Frame(plugin_path="worker")
    frame.run()
    function_list = frame.function_list
    update_config_server(function_list)
    # 延迟0.3秒，等待redis稳定更新
    import time
    time.sleep(0.3)
else:
    config.update({"is_worker": 0})
    log.info(u"Warning: not worker, start without task register.")


