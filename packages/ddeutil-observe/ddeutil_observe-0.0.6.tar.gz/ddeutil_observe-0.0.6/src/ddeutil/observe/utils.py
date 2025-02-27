# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

import logging
from functools import lru_cache

from .conf import config


@lru_cache
def get_logger(name: str) -> logging.Logger:  # no cov
    """Return logger with an input module name.

    :param name: A name of module that want to get logging manager
    :rtype: logging.Logger
    """
    logger = logging.getLogger(name)
    formatter = logging.Formatter(
        fmt=(
            "%(asctime)s.%(msecs)03d (%(name)-10s, %(process)-5d, "
            "%(thread)-5d) [%(levelname)-7s] %(message)-120s "
            "(%(filename)s:%(lineno)s)"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    logger.addHandler(stream)
    logger.setLevel(logging.DEBUG if config.log_debug else logging.INFO)
    return logger
