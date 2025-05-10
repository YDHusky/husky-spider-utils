import flet as ft
import logging

windows_logger = logging.getLogger("GlobalLogger")
windows_logger.setLevel(logging.DEBUG)


# LogPage 类
class LogPage(ft.Column):
    def __init__(self, run):
        super().__init__()
        self.expand = True
        self.alignment = ft.MainAxisAlignment.START
        self.controls = [
            ft.Text("首页", size=20, weight=ft.FontWeight.BOLD),
            ft.Row(controls=[ft.Button("开始运行", expand=True, on_click=run), ]),
            ft.Container(
                content=ft.ListView(expand=True, auto_scroll=True, spacing=10),
                bgcolor=ft.Colors.WHITE,
                expand=True,
                border_radius=10,
                padding=10,
            )
        ]

        # 用于存储日志信息的队列
        self.log_queue = []

        # 将全局 logger 的日志处理器设置为 FletLogHandler
        windows_logger.addHandler(FletLogHandler(self))

    def update_log(self):
        # 更新日志显示
        if self.page:  # 确保 LogPage 已经被添加到页面中
            self.controls[2].content.controls = self.log_queue  # 将队列中的日志信息显示到页面上
            self.update()
            self.controls[2].content.update()  # 更新 ListView

        # self.main_page.update()


# 定义一个日志处理器，用于将日志信息发送到 LogPage
class FletLogHandler(logging.Handler):
    def __init__(self, log_page: LogPage):
        super().__init__()
        self.log_page = log_page
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    def emit(self, record):
        log_entry = self.format(record)
        color = self.get_color(record.levelname)
        log_text = ft.Text(log_entry, color=color, selectable=True)
        self.log_page.log_queue.append(log_text)  # 将日志信息添加到队列中
        self.log_page.update_log()  # 更新日志显示

    @staticmethod
    def get_color(levelname):
        if levelname == "DEBUG":
            return ft.Colors.BLUE
        elif levelname == "INFO":
            return ft.Colors.GREEN
        elif levelname == "WARNING":
            return ft.Colors.YELLOW
        elif levelname == "ERROR":
            return ft.Colors.RED
        elif levelname == "CRITICAL":
            return ft.Colors.PURPLE
        else:
            return ft.Colors.BLACK
