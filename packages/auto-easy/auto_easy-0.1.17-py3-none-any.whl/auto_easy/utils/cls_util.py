import builtins
import importlib.util
import os
from typing import List

from auto_easy.utils.cache_util import cache_with_custom_time


# from auto_easy.ai.model_mgr import is_builtins


@cache_with_custom_time()
def find_classes_inheriting(dir: str, cls) -> List[type]:
    """
    在指定目录下查找继承自AIItemBase的所有类。
    :param dir: 要查找的目录路径
    :return: 继承自AIItemBase的类的列表
    """
    if not os.path.exists(dir):
        raise Exception("不存在的路径: {}".format(dir))
    if isinstance(cls, type):
        cls = cls.__name__
    if not isinstance(cls, str):
        raise Exception("find_classes_inheriting must use class or class_name")
    result_classes = []
    processed_modules = set()
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                pass
                file_path = os.path.join(root, file)
                module_name = os.path.splitext(file)[0]
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                processed_modules.add(module_name)
                for name, obj in vars(module).items():
                    if isinstance(obj, type):
                        try:
                            if cls in [cls.__name__ for cls in obj.mro()]:
                                result_classes.append(obj)
                        except AttributeError:
                            continue
    # 因为同个文件夹下，不同文件导入的class可能是路径不同，被认为不同的类，这里通过类名统一去重
    unique_class_list = [cls for i, cls in enumerate(result_classes) if
                         cls.__name__ not in [c.__name__ for c in result_classes[:i]]]

    # 排序，将派生类排在前面
    def sort_classes(cls1, cls2):
        return len(cls1.mro()) > len(cls2.mro())

    sorted_class_list = sorted(unique_class_list, key=lambda x: tuple(sort_classes(x, y) for y in unique_class_list),
                               reverse=True)

    return sorted_class_list


def is_class_name(obj, cls):
    mro_list = obj.__class__.__mro__
    mro_name_list = [c.__name__ for c in mro_list]
    return cls.__name__ in mro_name_list


def is_builtins(obj):
    return isinstance(obj, builtins.object)


def cls_to_dict(obj):
    if not hasattr(obj, '__dict__'):
        return obj
    d = vars(obj)
    for k, v in d.items():
        if isinstance(v, list) and len(v) > 0 and is_builtins(v[0]):
            for idx, list_val in enumerate(v):
                v[idx] = cls_to_dict(list_val)
            continue
        if is_builtins(v):
            d[k] = cls_to_dict(v)
            continue
    return d


def set_obj_by_dict(obj, d):
    for k, v in obj.__dict__.items():
        if k in d:
            setattr(obj, k, d[k])


# 判断是对象还是类
def is_cls(v):
    return isinstance(v, type)


def is_actual_subclass(subclass, superclass):
    subclass = subclass
    if not is_cls(subclass):
        subclass = subclass.__class__
    # 判断 subclass 是否是 superclass 的实际子类
    return subclass == superclass or (issubclass(subclass, superclass) and superclass in subclass.__mro__)
