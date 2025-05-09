import inspect
import os.path

import yaml
from yaml import FullLoader

from husky_spider_utils.tool.dict_tool import deep_merge


class SpiderConfig:
    """
    爬虫配置类，需要给每一个值都进行初始化，其次包含_的属性会被转化为tree
    """
    configVersion = '1.0.0'

    def fun_to_dict(self):
        attrs = inspect.getmembers(self)
        config_dict = {}
        for k, v in attrs:
            if not k.startswith('__') and not k.startswith('fun'):
                params = k.split("_")
                config_dict = deep_merge(config_dict, self.fun_create_tree(params, v))
        return config_dict

    def fun_save_to_yml(self, folder="./", file_name="config.yml"):
        yaml.dump(self.fun_to_dict(), open(os.path.join(folder, file_name), 'w'))

    def fun_load_from_yml(self, folder="./", file_name="config.yml"):
        config_dict = yaml.load(open(os.path.join(folder, file_name), 'r'), FullLoader)  # type: dict
        self.fun_load_from_dict(config_dict)

    def fun_load_from_dict(self, config_dict, prefix=""):
        for k, v in config_dict.items():
            full_key = f"{prefix}{k}" if prefix else k
            if isinstance(v, dict):
                # 如果值是字典，则递归处理
                self.fun_load_from_dict(v, prefix=full_key + "_")
            else:
                # 如果值不是字典，则直接设置成员变量
                self.__setattr__(full_key, v)

    def fun_create_tree(self, params: list, value, height=0):
        if height == len(params) - 1:
            return {
                params[height]: value
            }
        else:
            return {
                params[height]: self.fun_create_tree(params, value, height + 1)
            }
