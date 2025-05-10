from husky_spider_utils.husky_spider import HuskySpider
import flet as ft

from husky_spider_utils.windows.pages.config_page import ConfigPage
from husky_spider_utils.windows.pages.log_page import LogPage, windows_logger


class SpiderWindows:
    def __init__(self, spider: HuskySpider, window_title="Husky Spider Utils"):
        self.window_title = window_title
        self.spider = spider
        self.destinations = []
        self.pages = []
        self.log_page = LogPage(self.run)
        self.config_page = ConfigPage(self.spider.config, self.spider.config_folder_path, self.spider.config_filename)
        self.add_page(self.log_page, icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="首页")
        self.add_page(self.config_page, icon=ft.Icons.SETTINGS_OUTLINED, selected_icon=ft.Icons.SETTINGS, label="配置")

        windows_logger.info("本爬虫基于Husky Spider Utils编写! https://spider.yudream.online/husky-spider-utils.html")

    def run(self, e):
        windows_logger.info("程序开始运行!")
        pass

    def main_window(self, page: ft.Page):
        page.title = self.window_title
        page.theme = ft.Theme(font_family="simsun")

        def update_page(e):
            selected_index = e.control.selected_index
            content_area = page.controls[0].controls[2]  # 获取内容区域
            content_area.controls[0] = self.pages[selected_index]  # 更新内容区域的内容
            page.update()
            self.log_page.update_log()

        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=60,
            min_extended_width=100,
            group_alignment=-0.9,
            destinations=[
                *self.destinations
            ],
            on_change=lambda e: update_page(e),
        )
        content_area = ft.Column([self.pages[0]], alignment=ft.MainAxisAlignment.CENTER, expand=True)
        page.add(
            ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=1),
                    content_area,
                ],
                expand=True,
            )
        )

    def add_page(self, page, **kwargs):
        self.destinations.append(ft.NavigationRailDestination(
            **kwargs
        ))
        self.pages.append(page)
