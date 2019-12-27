#!/usr/bin/python
# -*- coding: utf8 -*-

import os
import socket
# 根据命令行参数设置环境类型
import tornado.options
tornado.options.define('port', default=8100, type=int)
tornado.options.define('env', default='offline', type=str)
tornado.options.define('log_level', default='debug', type=str)
tornado.options.define('log_dir', default='./log', type=str)
tornado.options.define('server_name', default='ipa_server', type=str)
tornado.options.parse_command_line()

# 获取项目路径
BASE_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
FILE_DIR = os.path.join(BASE_DIR, 'file')

# 获取本机IP
LOCAL_IP = socket.gethostbyname(socket.gethostname())


"""服务基础配置"""
ServerBaseConfig = {
    'env_type':         tornado.options.options.env,  # 环境类型, online|offline
    'listen_port':      tornado.options.options.port,  # 默认监听端口
    'log_level':        tornado.options.options.log_level,  # 日志级别, debug|info|warning|error
    'log_dir':          tornado.options.options.log_dir,  # 日志目录
    'http_timeout':     1.0,  # http请求的超时时间, 单位s
    'server_name':      tornado.options.options.server_name,     # 服务器名称
    'ip':               LOCAL_IP,    # 本机ip
}

if ServerBaseConfig['env_type'] == 'online':
    pass
else:
    pass

SERVER_HOST = 'yourdomain.cn'
