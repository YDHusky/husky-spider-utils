# Husky Spider utils

## 介绍

本库简单实现了 Selenium 和 requests 的结合，并封装了少部分常用 Selenium 功能。使用 `SeleniumSession` 相关方法会自动更新
cookies（session 和 selenium 互通）。

## 使用

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

## 方法说明

### `__init__` 方法

- **功能**：初始化 `SeleniumSession` 对象。
- **参数**：
    - `selenium_init_url`：Selenium 初始化时访问的 URL，默认为 `"https://cn.bing.com"`。
    - `driver_type`：使用的浏览器类型，可选值为 `"firefox"`、`"chrome"`、`"edge"`，默认为 `"firefox"`。
    - `headers`：自定义请求头，若不传则使用默认请求头。

### `init_headers` 方法

- **功能**：初始化请求头。
- **参数**：
    - `headers`：自定义请求头，若不传则使用默认请求头。

### `init_driver` 方法

- **功能**：初始化 WebDriver。
- **参数**：
    - `driver_type`：使用的浏览器类型，可选值为 `"firefox"`、`"chrome"`、`"edge"`，默认为 `"firefox"`。

### `get` 方法

- **功能**：使用 requests 发起 GET 请求。
- **参数**：
    - `url`：请求的 URL。
    - `**kwargs`：其他参数，如 `params`、`timeout` 等。
- **返回值**：请求的响应对象。

### `post` 方法

- **功能**：使用 requests 发起 POST 请求。
- **参数**：
    - `url`：请求的 URL。
    - `data`：请求体中的数据。
    - `json`：请求体中的 JSON 数据。
    - `**kwargs`：其他参数，如 `timeout` 等。
- **返回值**：请求的响应对象。

### `request` 方法

- **功能**：使用 requests 发起请求。
- **参数**：
    - `url`：请求的 URL。
    - `method`：请求方法，如 `"GET"`、`"POST"` 等。
    - `**kwargs`：其他参数，如 `data`、`json`、`timeout` 等。
- **返回值**：请求的响应对象。

### `get_session_cookies_to_dict` 方法

- **功能**：将 session 的 cookies 转换为字典格式。
- **返回值**：cookies 字典。

### `cookies_to_driver` 方法

- **功能**：将 session 的 cookies 添加到 WebDriver 中，并刷新页面。

### `selenium_get` 方法

- **功能**：使用 WebDriver 访问指定的 URL。
- **参数**：
    - `url`：访问的 URL。

### `selenium_cookies_to_session` 方法

- **功能**：将 WebDriver 的 cookies 添加到 session 中。

### `send_key` 方法

- **功能**：在指定的元素中输入内容。
- **参数**：
    - `value`：元素的定位值。
    - `send_value`：输入的内容。
    - `by`：元素的定位方式，默认为 `By.CSS_SELECTOR`。
    - `timeout`：超时时间，默认为 60 秒。

### `click` 方法

- **功能**：点击指定的元素。
- **参数**：
    - `value`：元素的定位值。
    - `by`：元素的定位方式，默认为 `By.CSS_SELECTOR`。
    - `timeout`：超时时间，默认为 60 秒。

### `hover` 方法

- **功能**：鼠标悬停在指定的元素上。
- **参数**：
    - `value`：元素的定位值。
    - `by`：元素的定位方式，默认为 `By.CSS_SELECTOR`。
    - `timeout`：超时时间，默认为 60 秒。

### `on_input` 方法

- **功能**：静态方法，用于获取用户输入。
- **参数**：
    - `des`：输入提示信息。

### `scroll` 方法

- **功能**：滚动页面到指定的高度。
- **参数**：
    - `height`：滚动的高度，默认为 200。

### `scroll_to_el` 方法

- **功能**：滚动页面到指定的元素。
- **参数**：
    - `element`：指定的元素。

### `scroll_to_el_by_value` 方法

- **功能**：滚动页面到指定的元素。
- **参数**：
    - `value`：元素的定位值。
    - `by`：元素的定位方式，默认为 `By.CSS_SELECTOR`。

### `scroll_to_top` 方法

- **功能**：滚动页面到顶部。

### `scroll_to_bottom_fade` 方法

- **功能**：平滑滚动页面到底部。
- **参数**：
    - `step`：每次滚动的距离（像素），默认为 100。
    - `max_height`：最大滚动高度（像素），默认为页面底部。

### `scroll_to_bottom` 方法

- **功能**：将页面滚动到最底部。

### `save_cookies` 方法

- **功能**：保存 WebDriver 的 cookies 到指定的文件。
- **参数**：
    - `save_path`：保存文件的路径。

### `load_cookies` 方法

- **功能**：加载指定文件中的 cookies 到 WebDriver 和 session 中。
- **参数**：
    - `load_path`：加载文件的路径。