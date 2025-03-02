# -*- coding: utf-8 -*-

import os
import socket
from ConfigParser import ConfigParser
import traceback
import json


class Config(dict):
    def __init__(self):
        dict.__init__(self, {})
        self.root_path = os.getcwd()
        self['g_ip'] = socket.gethostname()

    def from_ini(self, file_name):
        config_path = os.path.join(self.root_path, file_name)
        assert os.path.isfile(config_path), '缺少 %s 文件' % file_name
        cf = ConfigParser()
        cf.read(config_path)
        config_type = cf.get('sys', 'cfg_type')
        self['debug'] = cf.getboolean('sys', 'debug')
        for x in cf.items(config_type):
            self[x[0]] = x[1]
        self["cfg_type"] = config_type
        return True

    def from_json(self, file_name):
        config_path = os.path.join(self.root_path, file_name)
        assert os.path.isfile(config_path), '缺少 %s 文件' % file_name
        with open(config_path) as f:
            data_str = f.read()
            data_json = json.loads(data_str)
        self.update(data_json)
        return True

    def get_version(self):
        try:
            g_git_head = ''
            g_git_head_hash = ''
            dot_git_path = os.path.join(self.root_path, '.git')
            if os.path.isdir(dot_git_path):
                git_head_path = os.path.join(dot_git_path, 'HEAD')
                with open(git_head_path, 'r') as f:
                    g_git_head = f.readline().strip()
                if g_git_head.startswith('ref:'):
                    git_hash_path = g_git_head[5:]
                    git_hash_path = os.path.join(dot_git_path, git_hash_path)
                    g_git_head = g_git_head.split('/')[-1]
                    with open(git_hash_path, 'r') as f:
                        g_git_head_hash = f.readline().strip()
            git_version_temp = ':'.join([g_git_head, g_git_head_hash])
            return git_version_temp
        except Exception as e:
            err_msg = traceback.format_exc()
            print err_msg
            return ""

config = Config()
config.from_ini('config.ini')
config["g_ip"] = socket.gethostname()
git_version = config.get_version()
config['git_version'] = git_version
if git_version:
    g_git_version = git_version.split(":")
    if len(g_git_version) == 2:
        branch_name = g_git_version[0]
        git_ver = g_git_version[1]
        config['git_ver'] = git_ver
        config['git_branch_name'] = branch_name


def is_in_dev():
    cfg_type = config.get("cfg_type", "")
    if cfg_type == "dev":
        return True
    return False


def is_in_env(env):
    cfg_type = config.get("cfg_type", "")
    if cfg_type == env:
        return True
    return False

WORKER_NAME = config.get("worker_name", "")
FUNC_MONITOR_NAME = "worker_cus_self_health_report"
hostname = socket.gethostname()
FUNC_MONITOR_PREFIX = "___".join([hostname, WORKER_NAME])

machine_type_path = "/etc/oops/machine_type.conf"
try:
    if os.path.isfile(machine_type_path):
        cfg = ConfigParser()
        cfg.read(machine_type_path)
        machine_info = {}
        map(lambda x: machine_info.update({x[0]: x[1]}), cfg.items("sys"))
        machine_id = machine_info.get("machine_id", "")
        device_id = machine_info.get("device_id", "")
        config.update({
            "_machine_id": machine_id,
            "_device_id": device_id,
            "_machine_name": "",
            "_device_name": "",
        })
        host_name = socket.gethostname()
        host_name_list = host_name.split("___")
        if len(host_name_list) == 2:
            machine_name = host_name_list[0]
            device_name = host_name_list[1]
            config.update({
                "_machine_name": machine_name,
                "_device_name": device_name,
            })
except Exception as e:
    """"""
    err_msg = traceback.format_exc()
    print err_msg


try:
    LOG_FILE = config.get("log_file", "")
    app_log_path = LOG_FILE
    if not app_log_path:
        app_log_path = "/var/log/{}/{}.log".format(WORKER_NAME, WORKER_NAME)
        if not os.path.isfile(app_log_path):
            app_log_path = ""
    config.update({"log_file": app_log_path})
except Exception as e:
    """"""
    config.update({"log_file": ""})
    err_msg = traceback.format_exc()
    print err_msg

print config
