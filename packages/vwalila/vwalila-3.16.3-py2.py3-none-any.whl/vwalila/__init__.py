# -*- coding: utf-8 -*-

"""
  vwalila - Awesome toolkit for dobechina internal.
"""

import logging

logger = logging.getLogger(__name__)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(
    logging.Formatter("[vwalila %(levelname)-7s] %(message)s")
)
logger.addHandler(console)
logger.setLevel(logging.INFO)


version_info = (3, 16, 3)
__version__ = ".".join([str(v) for v in version_info])
