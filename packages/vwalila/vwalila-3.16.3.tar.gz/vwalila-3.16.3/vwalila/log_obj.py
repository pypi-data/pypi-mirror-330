# -*- coding: utf-8 -*-

import logging.config


def get_log(log_file=None, debug=False, log_max_bytes=65536,
            log_backup_count=10):
    """

    :param log_file:
    :param debug:
    :param log_max_bytes:
    :param log_backup_count:
    :return:
    """
    handlers_list = []
    handlers = {}
    if debug or not log_file:
        handlers_list.append("console")
        handlers.update({
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            }})
    else:
        handlers_list.append("file")
        handlers.update({
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": log_file,
                "maxBytes": log_max_bytes,
                "backupCount": log_backup_count,
                "encoding": "utf8"
            }})

    log_dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(asctime)s - %(levelname)s - %(module)s - %(filename)s - %(funcName)s - %(message)s"
            }
        },
        "handlers": handlers,
        "loggers": {
            "log_module": {
                "level": "INFO",
                "handlers": handlers_list
            }
        }
    }
    logging.config.dictConfig(log_dict)
    log = logging.getLogger("log_module")
    return log


if __name__ == "__main__":
    """"""
