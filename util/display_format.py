#!/usr/bin/env python
# coding=utf-8

"""
description: 格式化各种展示格式
date: 2016-11-16
"""

from datetime import datetime


class DisplayFormatter(object):
    """格式化各种展示格式"""
    @classmethod
    def format_time(cls, create_time):
        """转换为发表时间格式, 规则:
            1). 1分钟以内显示 "刚刚"
            2). 1分钟以上 && 1小时以内, 显示 "xx分钟前"
            3). 2小时以上 && 1天以内, 显示 "xx小时前"
            4). 1天以上 && 1月以内, 显示 "xx天前"
            5). 1月以上 && 1年以内, 显示 "xx月前"
            6). 1年以上, 显示 "xx年前"
        Returuns:
            @str
        """
        time_diff = datetime.now() - create_time
        if time_diff.days == 0:
            if time_diff.seconds < 60:
                return '刚刚'
            elif time_diff.seconds < 3600:
                return '{minutes}分钟前'.format(minutes=int(time_diff.seconds / 60))
            return '{hours}小时前'.format(hours=int(time_diff.seconds / 3600))
        elif time_diff.days < 31:
            return '{days}天前'.format(days=int(time_diff.days))
        elif time_diff.days < 365:
            return '{days}月前'.format(days=int(time_diff.days / 30))
        return '{days}年前'.format(days=int(time_diff.days / 365))
