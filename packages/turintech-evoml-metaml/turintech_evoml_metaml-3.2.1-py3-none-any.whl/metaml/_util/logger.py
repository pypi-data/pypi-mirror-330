# !/usr/bin/env python3
# encoding: utf-8
"""
This file defines a logger class that can manage the logging info format: JSON for log configuration
"""

# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import codecs
import logging
import logging.config

from ruamel.yaml import YAML

# ---------------------------------------------------------------------------- #

yaml = YAML(typ="safe", pure=True)


class AdvancedLogger:
    def __init__(self, name: str = __name__):
        log_config = self.__get_yaml_config()
        logging.config.dictConfig(log_config)
        self.logger = logging.getLogger(name)

    def get_logger(self):
        return self.logger

    def __get_yaml_config(self):
        config_file = os.path.join(os.path.dirname(__file__), "log_config.yml")
        # config_file = "metaml/_util/log_config.yml"
        # logging.info("config file: %s", config_file)
        # We use codecs.open because it is equivalent to Python 3 open()
        with codecs.open(config_file, "r", encoding="utf-8") as fd:
            config = yaml.load(fd.read())
        return config
