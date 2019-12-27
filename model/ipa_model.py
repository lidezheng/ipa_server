# -*- coding:utf-8 -*-

import datetime
from peewee import *

db = SqliteDatabase('ipa.db')


class BaseModel(Model):
    class Meta:
        database = db


class IpaModel(BaseModel):
    """ipa信息表"""
    class Meta:
        db_table = 'ipa'
        database = db

    id = AutoField(primary_key=True)
    filename = CharField(default='', verbose_name='ipa唯一名字的md5', max_length=64)
    title = CharField(default='', verbose_name='标题', max_length=128)
    identifier = CharField(default='', verbose_name='ipa标识符', max_length=128)
    version = CharField(default='', verbose_name='ipa版本号', max_length=128)
    update_desc = CharField(default='', verbose_name='打包描述', max_length=256)
    file_size = IntegerField(default=0, verbose_name='文件字节数')

    status = SmallIntegerField(verbose_name='状态', default=1)
    create_time = DateTimeField(verbose_name='创建时间', default=datetime.datetime.now)
    update_time = DateTimeField(verbose_name='更新时间', default=datetime.datetime.now)

    @classmethod
    def get_by_filename(cls, filename):
        return cls.select().\
            where(cls.filename == filename, cls.status == 1).\
            order_by(cls.id.desc()).first()

    @classmethod
    def get_ipa_list(cls):
        return cls.select().\
            where(cls.status == 1).\
            order_by(cls.id.desc())


# 初始化数据库
if not IpaModel.table_exists():
    IpaModel.create_table()
