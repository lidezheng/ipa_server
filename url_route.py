#!/use/bin/env python
# coding=utf-8


from handler import *
from tornado.web import StaticFileHandler


url_route = [

    # ipa文件列表页
    (r'^/$|^/index.html$|^/ipa.html$', main_handler.IpaHtmlHandler),
    # 获取plist详情
    (r'^/plist/(.*)$', main_handler.IpaListHandler),
    # 上传文件
    (r'^/upload', main_handler.UploadHandler),
    # 下载文件
    (r'^/file/(.*)$', StaticFileHandler, {'path': 'file'}),
]
