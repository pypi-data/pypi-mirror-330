# -*- coding: utf-8 -*-

from log_obj import get_log
from .config import config

log_file = config.get("log_file", "")
debug = config.get("debug", False)
log_max_bytes = int(config.get("log_max_bytes", 65536))  # default 64kb
log_backup_count = int(config.get("log_backup_count", 10))

log = get_log(log_file=log_file, debug=debug, log_max_bytes=log_max_bytes,
              log_backup_count=10)


if __name__ == "__main__":
    """"""
