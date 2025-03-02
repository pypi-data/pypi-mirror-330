# -*- coding: utf-8 -*-

from vwalila.logger_helper import log
import celery
from vwalila.exc import exception_log
from .signals import register_task_signals
from .decorators import attach_signal_to_task
from .frame import function_list as worker_function_list
from . import mq_config
from vwalila.config import config, FUNC_MONITOR_NAME, FUNC_MONITOR_PREFIX

logger = log

# register signal
register_task_signals()


AMQP_DOMAIN = config.get("rabbitmq", "")
REDIS_DOMAIN = config.get("redis", "")

# Other config
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ['json']

# 结果过期时间
CELERY_TASK_RESULT_EXPIRES = 90
CELERYD_TASK_SOFT_TIME_LIMIT = 60

WORKER_MQ_HOSTS = config.get("worker_mq_hosts", "")
IS_WORKER = config.get("is_worker", 0)


class TaskManage(object):
    def __init__(self, function_obj_list):
        """"""
        # 更新 rabbitmq 地址
        self.mq_domain = AMQP_DOMAIN

        self.backend_domain = REDIS_DOMAIN

        # frame处理的方法列表
        self.function_obj_list = function_obj_list

        # 方法关联mq hosts 名称，全部的worker的function
        self.dic_all_func_name_hosts = {}

        # broker列表（hosts列表），全部worker的hosts
        self.all_broker_list = []

        # hosts名管理celery app 对象，全部worker的hosts
        self.dic_all_broker_hosts = {}

        # 当前worker的function列表
        self.worker_function_list = []

    def register_all_celery_app(self, force_hosts=None):
        """
        broker_list like [
            "worker_fw", "worker_zf"
        ]

        """
        # 获取所有的broker list
        self.get_all_broker_list()

        # self.all_broker_list有变更，需要新增没有注册的broker
        # 只注册未注册过的broker
        if not self.all_broker_list:
            self.all_broker_list = []
        broker_registered_list = self.dic_all_broker_hosts.keys()
        broker_need_register_list = [x for x in self.all_broker_list
                                     if x not in broker_registered_list]
        for broker in broker_need_register_list:
            if IS_WORKER == 1:
                if broker != WORKER_MQ_HOSTS:
                    if broker != force_hosts:
                        continue
            broker_url = "".join((self.mq_domain, broker))
            celery_app = self.reg_app_celery(broker=broker_url)
            self.dic_all_broker_hosts[broker] = celery_app

    def get_celery_app_by_hosts(self, hosts_name):
        """
        根据hosts_name，获取mq hosts 实例
        :param hosts_name:
        :return:
        """
        if not hosts_name:
            return None
        return self.dic_all_broker_hosts.get(hosts_name, None)

    def get_all_broker_list(self):
        """
        取所有broker
        :return:
        """
        self.all_broker_list = mq_config.get_broker_list_from_config_server()

    def get_all_function_list(self):
        """
        取所有broker
        :return:
        """
        self.dic_all_func_name_hosts = \
            mq_config.get_dic_all_func_name_hosts_from_redis()

    def handle_worker_function_list(self):
        """
        处理本项目中需要注册的方法
        :return:
        """
        for function_obj in self.function_obj_list:
            f_name = function_obj.__name__
            if f_name == FUNC_MONITOR_NAME:
                f_name = "___".join([f_name, FUNC_MONITOR_PREFIX])
            hosts_name = self.dic_all_func_name_hosts.get(
                f_name, {}).get("hosts", "")
            queue_name = self.dic_all_func_name_hosts.get(
                f_name, {}).get("queue", "default")
            if not all((function_obj,
                        hosts_name == WORKER_MQ_HOSTS, queue_name)):
                continue
            self.worker_function_list.append({
                "func_obj": function_obj,
                "hosts": hosts_name,
                "queue": queue_name,
            })

    def get_worker_function_list(self):
        """
        获取当前项目需要注册的function_list
        :return:
        """
        return self.worker_function_list

    def run(self):
        """
        # load worker function list
        # 初始化celery app（virtual hosts & broker）
        # 注册task
        :return:
        """
        # 根据all_broker_list，注册celery app
        self.register_all_celery_app()

        # 把方法映射放到本地
        self.get_all_function_list()

        # 洗掉当前worker的function_list
        self.handle_worker_function_list()

    def reg_app_celery(self, broker):
        # set backend and broker
        celery_app = celery.Celery(
            backend=self.backend_domain,
            broker=broker)
        celery_app.conf.update(
            accept_content=CELERY_ACCEPT_CONTENT,
            result_expires=CELERY_TASK_RESULT_EXPIRES,
            task_soft_time_limit=CELERYD_TASK_SOFT_TIME_LIMIT,
            redis_backend_health_check_interval=40,
            redis_retry_on_timeout=True,
            redis_socket_keepalive=True,
            task_protocol=1)  # librabbitmq, no cover
        return celery_app


task_manage = TaskManage(function_obj_list=worker_function_list)
task_manage.run()

# 注册任务
# not to be execute in function or method cause module import error
function_list = task_manage.get_worker_function_list()
app_celery = task_manage.get_celery_app_by_hosts(WORKER_MQ_HOSTS)
for func in function_list:
    func_obj = func.get("func_obj", None)
    hosts = func.get("hosts", "")
    queue = func.get("queue", "default")
    if not any((func_obj, hosts != WORKER_MQ_HOSTS, queue)):
        continue
    arg_count = func_obj.func_code.co_argcount
    arg_name_list = func_obj.func_code.co_varnames[0:arg_count]
    func_name = func_obj.__name__
    if func_name == FUNC_MONITOR_NAME:
        func_name = "___".join([func_name, FUNC_MONITOR_PREFIX])
    if "ignore_result" in arg_name_list:
        app_celery.task(
            bind=True,
            ignore_result=True,
            name=func_name,
            queue=queue)(
            attach_signal_to_task(logger=logger)(exception_log(func_obj)))
    else:
        app_celery.task(
            bind=True,
            name=func_name,
            queue=queue)(
            attach_signal_to_task(logger=logger)(exception_log(func_obj)))

    arg_cache = "worker"
    func_defaults = func_obj.func_defaults
    if func_defaults:
        func_defaults_count = len(func_defaults)
        arg_defaults_list = arg_name_list[arg_count-func_defaults_count:]
        if arg_cache in arg_defaults_list:
            cache_index = arg_defaults_list.index(arg_cache)
            print arg_cache, func_defaults[cache_index]
            print func_obj.__name__
