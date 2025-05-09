def deep_merge(dict1, dict2):
    """
    深度合并两个字典，支持任意深度的嵌套。
    """
    for key in dict2:
        if key in dict1:
            if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                # 如果两个字典在同一个键下都是字典，则递归合并
                deep_merge(dict1[key], dict2[key])
            else:
                # 如果不是字典，则直接覆盖
                dict1[key] = dict2[key]
        else:
            # 如果键不存在于 dict1 中，则直接添加
            dict1[key] = dict2[key]
    return dict1