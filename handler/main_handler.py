# -*- coding:utf-8 -*-

import os
import time
import hashlib
import zipfile
import plistlib
import re
import tornado.web
from model.ipa_model import IpaModel
from util.convert_object import ConvertObject
from util.display_format import DisplayFormatter
from conf.server_conf import FILE_DIR
from conf.server_conf import SERVER_HOST


class IpaNode(object):
    """上传节点信息"""
    def __init__(self, db_record):
        self.id = db_record.id
        self.plist_url = 'https://{}/plist/{}'.format(SERVER_HOST, db_record.filename)
        self.identifier = db_record.identifier
        self.version = db_record.version
        self.file_size = '{:.2f} MB'.format(db_record.file_size / 1024 / 1024)
        self.update_desc = db_record.update_desc
        self.title = '{}.ipa'.format(db_record.title)
        self.ipa_file_url = 'https://{}/file/{}'.format(SERVER_HOST, db_record.filename)
        self.create_time = DisplayFormatter.format_time(create_time=db_record.create_time)


class IpaHtmlHandler(tornado.web.RequestHandler):
    """下载主页面"""
    def get(self):
        ipa_list = IpaModel.get_ipa_list()
        ipa_list = [IpaNode(v) for v in ipa_list]
        latest_ipa = ipa_list[0] if ipa_list else None
        history_ipa_list = ipa_list[1:]
        self.render('ipa.html', latest_ipa=latest_ipa, history_ipa_list=history_ipa_list)      # TODO 优化页面展示，对移动端友好, 参考蒲公英 或者让 客户端同事给个设计

        # result = {
        #     'error_no': 0,
        #     'error_msg': 'success',
        #     'data': {
        #         'ipa_list': [ConvertObject.object_2_dict(v) for v in ipa_list],
        #     },
        # }
        # super(IpaHtmlHandler, self).write(result)


class IpaListHandler(tornado.web.RequestHandler):
    """ipa plist页面"""
    def get(self, filename):
        # 根据ipa_id 获取ipa 信息
        ipa_record = IpaModel.get_by_filename(filename=filename)
        if not ipa_record:
            result = {'error_no': 1, 'error_msg': '未找到文件'}
            super(IpaListHandler, self).write(result)

        ipa_node = IpaNode(ipa_record)
        self.render('ipa.plist', ipa_node=ipa_node)


class UploadHandler(tornado.web.RequestHandler):
    """上传ipa文件"""

    def post(self):
        # 打包描述
        update_desc = self.get_argument('update_desc', '')

        # 接收文件
        filename = self.request.files['file'][0]['filename']
        filebody = self.request.files['file'][0]['body']

        filename = hashlib.md5((str(time.time()) + filename).encode('utf-8')).hexdigest()
        file_full_path = os.path.join(FILE_DIR, filename)
        with open(file_full_path, 'bw') as f:
            f.write(filebody)

        # 获取文件字节数
        file_size = os.path.getsize(file_full_path)
        # 获取ipa文件包信息
        data = self.get_ipa_plist_data(file_full_path)
        data.update({
            'filename': filename,
            'file_size': file_size,
            'update_desc': update_desc,
        })
        IpaModel.create(**data)

        # 清理多余文件
        self.clean_file()

        result = {
            'error_no': 0,
            'error_msg': 'success',
        }
        super(UploadHandler, self).write(result)

    def get_ipa_plist_data(self, file_full_path):
        """获取ipa包信息"""
        ipa_zip_file = zipfile.ZipFile(file_full_path)
        name_list = ipa_zip_file.namelist()
        pattern = re.compile(r'Payload/[^/]*.app/Info.plist')

        plist_path = None
        for path in name_list:
            m = pattern.match(path)
            if m is not None:
                plist_path = m.group()

        if not plist_path:
            return

        plist_data = ipa_zip_file.read(plist_path)
        plist_root = plistlib.loads(plist_data)

        executable = plist_root['CFBundleExecutable']
        identifier = plist_root['CFBundleIdentifier']
        version = plist_root['CFBundleShortVersionString']

        data = {
            'title': executable,
            'identifier': identifier,
            'version': version,
        }
        return data

    def clean_file(self):
        """清理多余文件"""
        ipa_list = IpaModel.get_ipa_list()
        for ipa in ipa_list[20:]:       # 保留最近20次记录
            # 删除多于文件
            filename = ipa.filename
            file_full_path = os.path.join(FILE_DIR, filename)
            if os.path.exists(file_full_path):
                os.remove(file_full_path)

            # 更新数据库记录
            ipa.status = 0
            ipa.save()

        # 清理不在数据库中记录的文件
        valid_file_names = set([v.filename for v in ipa_list])
        for root, dirs, files in os.walk(FILE_DIR):
            # root 表示当前正在访问的文件夹路径
            # files 表示该文件夹下的文件list
            # 遍历文件
            for f in files:
                if 'readme' in f:
                    continue
                    
                if f not in valid_file_names:
                    os.remove(os.path.join(root, f))
        return
