import inspect
from typing import TypeVar, Type

import flet as ft
from flet.core.textfield import InputFilter

from husky_spider_utils.config.spider_config import ConfigValueType, SpiderConfig

T = TypeVar('T', bound='SpiderConfig')


class ConfigPage(ft.Column):
    def __init__(self, config: SpiderConfig, config_folder, config_filename):
        super().__init__()
        self.config = config
        self.config_folder = config_folder
        self.config_filename = config_filename
        self.expand = True
        self.alignment = ft.MainAxisAlignment.START
        self.list_view = ft.ListView(expand=True, auto_scroll=True, spacing=10, controls=[])
        self.render_config()

        self.controls = [
            ft.Text("配置", size=20, weight=ft.FontWeight.BOLD),
            ft.Row(alignment=ft.MainAxisAlignment.END, controls=[
                ft.Button("保存配置", on_click=self.save_config)
            ]),
            ft.Container(
                content=self.list_view,
                bgcolor=ft.Colors.WHITE,
                expand=True,
                border_radius=10,
                padding=10,
            )
        ]

    def render_config(self):
        attrs = inspect.getmembers(self.config)
        for attr in attrs:
            controller = self.render_config_value(attr[0], attr[1])
            if controller is not None:
                self.list_view.controls.append(controller)
                print(controller)

    def save_config(self, e):
        for control in self.list_view.controls:
            self.config.__setattr__(control.data, control.value)
        self.config.fun_save_to_yml(self.config_folder, self.config_filename)

    def render_config_value(self, attr: str, value):
        attrs = inspect.getmembers(self.config)
        attrs = [a[0] for a in attrs]
        attr_type = attr.split('_')[0]
        config_value_types = [cvt.value for cvt in ConfigValueType]

        if attr_type in config_value_types:
            attr_name = attr.replace(f"{attr_type}_", "")
            label = attr_name
            options = []
            hint = attr_name

            if f"label_{attr_name}" in attrs:
                label = self.config.__getattribute__(f"label_{attr_name}")
            if f"options_{attr_name}" in attrs:
                options = getattr(self.config, f"options_{attr_name}")
            if f"hint_{attr_name}" in attrs:
                hint = self.config.__getattribute__(f"hint_{attr_name}")
            print(attr_type)
            print(attr_name)
            match attr_type:
                case ConfigValueType.STR.value:
                    return ft.TextField(label=label, value=value, hint_text=hint, data=attr)
                case ConfigValueType.INT.value:
                    return ft.TextField(label=label, value=value, hint_text=hint, data=attr,

                                        input_filter=InputFilter(regex_string=r"[-0-9]", replacement_string="",
                                                                 allow=True))
                case ConfigValueType.FLOAT.value:
                    return ft.TextField(label=label, value=value, hint_text=hint, data=attr,
                                        input_filter=InputFilter(regex_string=r"[-0-9.]", replacement_string="",
                                                                 allow=True))
                case ConfigValueType.BOOL.value:
                    return ft.Checkbox(label=label, value=value, data=attr, )
                case ConfigValueType.SELECT.value:
                    return ft.Dropdown(label=label, value=value, expand=True, data=attr, options=[
                        ft.DropdownOption(
                            i
                        ) for i in options
                    ])
        return None
