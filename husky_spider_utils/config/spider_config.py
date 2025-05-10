import inspect
import json
import os.path
from enum import Enum

import yaml
from yaml import FullLoader

from husky_spider_utils.tool.dict_tool import deep_merge


class SpiderConfig:
    """
    爬虫配置类，需要给每一个值都进行初始化，其次包含_的属性会被转化为tree
    """
    str_configVersion = '1.0.0'
    select_driverType = "edge"
    label_configVersion = "配置版本号"
    options_driverType = ['edge', 'chrome', 'firefox']
    label_driverType = "浏览器类型"
    hint_configVersion = "配置版本号"

    def __repr__(self):
        return json.dumps(self.fun_to_dict())

    def fun_to_dict(self) -> dict:
        attrs = inspect.getmembers(self)
        config_dict = {}
        config_value_types = [cvt.value for cvt in ConfigValueType]
        for k, v in attrs:
            if not k.startswith('__') and not k.startswith('fun'):
                params = k.split("_")
                if params[0] in config_value_types:
                    params.pop(0)
                    config_dict = deep_merge(config_dict, self.fun_create_tree(params, v))
        return config_dict

    def fun_save_to_yml(self, folder="./", file_name="config.yml"):
        yaml.dump(self.fun_to_dict(), open(os.path.join(folder, file_name), 'w'))

    def fun_load_from_yml(self, folder="./", file_name="config.yml"):
        config_dict = yaml.load(open(os.path.join(folder, file_name), 'r'), FullLoader)  # type: dict
        self.fun_load_from_dict(config_dict)

    def fun_load_from_dict(self, config_dict, prefix=""):
        config_value_types = [cvt.value for cvt in ConfigValueType]

        for k, v in config_dict.items():
            full_key = f"{prefix}{k}" if prefix else k
            if isinstance(v, dict):
                self.fun_load_from_dict(v, prefix=full_key + "_")
            else:
                attrs = inspect.getmembers(self)
                for attr_k, _ in attrs:
                    if full_key in attr_k and attr_k.split("_")[0] in config_value_types:
                        self.__setattr__(attr_k, v)
                        break

    def fun_create_tree(self, params: list, value, height=0):
        if height == len(params) - 1:
            return {
                params[height]: value
            }
        else:
            return {
                params[height]: self.fun_create_tree(params, value, height + 1)
            }


class ConfigValueType(Enum):
    STR = "str"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    LIST = "list"
    SELECT = "select"
