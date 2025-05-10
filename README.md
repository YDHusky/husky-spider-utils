# Husky Spider utils

## 介绍

本库简单实现了 Selenium 和 requests 的结合，并封装了少部分常用 Selenium 功能。使用 `SeleniumSession` 相关方法会自动更新
cookies（session 和 selenium 互通）。

## 使用

[中文教程](https://spider.yudream.online)

```bash
pip install husky-spider-utils
```

国内源

```bash
pip install husky-spider-utils -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

```python
from husky_spider_utils import SeleniumSession

session = SeleniumSession(selenium_init_url="https://cn.bing.com")
session.selenium_get("https://cn.bing.com")
```

## 基于该库的脚本(项目)

- **[ITest考试脚本](https://github.com/YDHusky/itest):** itest刷考试脚本(ai版,包含听力)
- **[SYiBanPost](https://github.com/YDHusky/SYiBanPost):** 易班发帖脚本

> 第三方基于该库实现的项目可以联系作者挂在本页

## 更新日志
### 0.2.1

- 修复huskyspider实例化时的driverType[从配置文件获取]

### 0.2.0

- 使用flet实现通过配置类自动生成图形化界面

`test.py`
```python
from husky_spider_utils.config.spider_config import SpiderConfig

from husky_spider_utils.windows.spider_windows import SpiderWindows


class TestConfig(SpiderConfig):
    str_configVersion = "1.1.1"
    str_account_username = ""
    str_account_password = ""


app = SpiderWindows(config_loder=TestConfig, is_selenium_session=False)
import flet as ft

ft.app(app.main_window)
```
打包windows
```bash
flet build windows --module-name test.py
```
更多查看flet

### 0.1.6

- 新增HuskySpider类
- 封装配置文件加载
- 多任务处理器(支持多线程或单线程处理或展示)