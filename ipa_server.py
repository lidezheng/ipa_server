#!/usr/bin/env python
# coding=utf-8

import sys
import os
import tornado.ioloop, tornado.httpserver, tornado.web
from tornado.log import access_log, gen_log
from conf.server_conf import ServerBaseConfig


def init_logger(listen_port):
    """初始化日志配置"""
    import logging
    from tornado.log import access_log, gen_log, app_log, LogFormatter
    from concurrent_log_handler import ConcurrentRotatingFileHandler
    access_log.propagate = False
    gen_log.propagate = False
    app_log.propagate = False

    fmt = ('%(color)s[%(levelname)1.1s %(asctime)s {listen_port}:%(module)s:%(lineno)d:'
        '%(funcName)s]%(end_color)s %(message)s'.format(listen_port=listen_port))
    formatter = LogFormatter(color=False, datefmt=None, fmt=fmt)

    accessLogHandler = logging.handlers.ConcurrentRotatingFileHandler(
        ServerBaseConfig['log_dir'] + '/access.log',
        maxBytes=512*1024*1024,
        backupCount=10)
    accessLogHandler.setFormatter(formatter)
    access_log.addHandler(accessLogHandler)

    serverLogHandler = logging.handlers.ConcurrentRotatingFileHandler(
        ServerBaseConfig['log_dir'] + '/server.log',
        maxBytes=128*1024*1024,
        backupCount=5)

    serverLogHandler.setFormatter(formatter)
    gen_log.addHandler(serverLogHandler)
    app_log.addHandler(serverLogHandler)

    access_log.setLevel(logging.INFO)
    gen_log.setLevel(getattr(logging, ServerBaseConfig['log_level'].upper()))
    app_log.setLevel(getattr(logging, ServerBaseConfig['log_level'].upper()))


def handler_format_access(handler):
    """输出handler的标准日志"""
    log_data = handler.format_log() if hasattr(handler, 'format_log') else ''
    if handler.get_status() < 400:
        log_method = access_log.info
    elif handler.get_status() < 500:
        log_method = access_log.warning
    else:
        log_method = access_log.error

    log_method('status=%d tc=%.2fms method=%s uri=%s remote=%s %s',
        handler.get_status(), 1000.0 * handler.request.request_time(),
        handler.request.method, handler.request.uri, handler.request.remote_ip, log_data)
    return


def main():
    # 检查日志目录不存在则创建
    if not os.path.isdir(ServerBaseConfig['log_dir']):
        os.mkdir(ServerBaseConfig['log_dir'])

    settings = {
        'static_path': os.path.join(os.path.dirname(__file__), 'static'),
        'template_path': os.path.join(os.path.dirname(__file__), 'template'),
        'debug': bool(ServerBaseConfig['env_type'] == 'local'),
    }

    # web服务
    from url_route import url_route
    app = tornado.web.Application(
        handlers=url_route,
        log_function=handler_format_access,
        **settings)

    # 监听端口
    listen_port = ServerBaseConfig['listen_port']
    init_logger(listen_port=listen_port)

    http_server = tornado.httpserver.HTTPServer(app, max_buffer_size=504857600, max_body_size=504857600)
    http_server.listen(listen_port)

    gen_log.info('ipa server start at port: %s, env_type: %s, log_level: %s, log_dir: %s',
        listen_port, ServerBaseConfig['env_type'],
        ServerBaseConfig['log_level'], ServerBaseConfig['log_dir'])
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':

    main()
