#!/usr/bin/python
# -*- coding: utf8 -*-

"""数据库的相关配置"""
from conf.server_conf import ServerBaseConfig


if ServerBaseConfig['env_type'] == 'online':

    DbConfig = {

    }

else:

    DbConfig = {

    }
