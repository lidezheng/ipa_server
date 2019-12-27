#!/usr/bin/env python
# coding=utf-8
from datetime import datetime
from decimal import Decimal


class ConvertObject(object):
    """结构体对象的转换"""

    @staticmethod
    def object_2_dict(input_object, witharr=False):
        """将结构体对象序列化为dict结构"""
        if input_object.__class__.__name__ in ('list', 'tuple', 'set'):
            output_list = [ConvertObject.object_2_dict(v,witharr) for v in input_object]
            return output_list

        if input_object.__class__.__name__ in ('dict',):
            output_dict = dict((k, ConvertObject.object_2_dict(v,witharr))
                for k,v in input_object.items())
            return output_dict

        if hasattr(input_object, '__dict__'):
            output_dict = dict((k, ConvertObject.object_2_dict(v,witharr))
                for k,v in input_object.__dict__.items())
            if witharr:
                output_dict['__class__'] = input_object.__class__.__name__
                output_dict['__module__'] = input_object.__module__
            return output_dict

        # 日期类型转换
        if isinstance(input_object, datetime):
            return input_object.strftime('%Y-%m-%d %H:%M:%S')
        # decimal数据类型转换成float型
        if isinstance(input_object, Decimal):
            return float(input_object)

        return input_object

    @staticmethod
    def dict_2_object(input_dict):
        """将dict结构反序列化为结构体对象, 要求结构体具有无参构造函数"""
        import sys
        if input_dict.__class__.__name__ == 'list':
            return [ConvertObject.dict_2_object(v) for v in input_dict]

        if input_dict.__class__.__name__ == 'dict':
            if '__class__' in input_dict and '__module__' in input_dict:
                class_name = input_dict.pop('__class__')
                module_name = input_dict.pop('__module__')
                __import__(module_name)
                output_object = getattr(sys.modules[module_name], class_name)()
                for k in input_dict:
                    output_object.__setattr__(k, ConvertObject.dict_2_object(input_dict[k]))
                return output_object
            else:
                return dict((k, ConvertObject.dict_2_object(v)) for k,v in input_dict.items())

        return input_dict

    @staticmethod
    def object_2_json(input_object, witharr=False):
        """将结构体对象序列化为json字符串"""
        import json
        output_dict = ConvertObject.object_2_dict(input_object=input_object, witharr=witharr)
        return json.dumps(output_dict)

    @staticmethod
    def json_2_object(input_json):
        """将json字符串反序列化为结构体对象, 要求结构体具有无参构造函数"""
        import json
        return ConvertObject.dict_2_object(input_dict=json.loads(input_json))
