import os.path
import shutil
from typing import TypeVar, Type
from loguru import logger
from requests import Response

from husky_spider_utils import SeleniumSession
from husky_spider_utils.config.spider_config import SpiderConfig
from husky_spider_utils.model.spider_task import SpiderTask
from husky_spider_utils.tool.thread_tools import SpiderThreadPoolExecutor

T = TypeVar('T', bound='SpiderConfig')


class HuskySpider:
    session: SeleniumSession

    def __init__(self,
                 is_need_config=True,
                 config_loder: Type[T] = SpiderConfig,
                 config_folder_path="./",
                 config_filename="config.yml",
                 temp_folder_path="./temp",
                 download_folder_path="./download",
                 is_selenium_session=True,
                 **selenium_session_kwargs):
        if is_selenium_session:
            self.session = SeleniumSession(**selenium_session_kwargs)
        self.temp_folder_path = temp_folder_path
        self.download_folder_path = download_folder_path
        self.config: T = config_loder()
        self.init_config(is_need_config, config_loder, config_folder_path, config_filename)
        self.records: list = []
        self.init_temp_folder(temp_folder_path)
        self.init_download_folder(download_folder_path)

    def init_temp_folder(self, temp_folder_path="./"):
        """
        初始化临时文件夹
        :param temp_folder_path: 临时文件夹路径
        :return:
        """
        if not os.path.exists(temp_folder_path):
            os.makedirs(temp_folder_path)
            open(os.path.join(temp_folder_path, "records.txt"), "w", encoding="utf-8").close()
        self.records = open(os.path.join(temp_folder_path, "records.txt"), "r", encoding="utf-8").read().split("\n")
        self.records.remove("")
        self.records = list(set(self.records))

    def init_download_folder(self, download_folder_path="./"):
        """
        初始化下载文件夹
        :param download_folder_path: 下载文件夹路径
        :return:
        """
        if not os.path.exists(download_folder_path):
            os.makedirs(download_folder_path)

    def init_config(self, is_need_config=True, config_loder: Type[T] = SpiderConfig,
                    config_folder_path="./",
                    config_filename="config.yml", ):
        """
        配置文件初始化
        :param is_need_config: 是否需要config
        :param config_loder: config加载器
        :param config_folder_path: config保存文件夹
        :param config_filename: config文件名
        :return:
        """
        if not isinstance(config_loder, type) or not issubclass(config_loder, SpiderConfig):
            raise Exception("config_loder需要是或者继承SpiderConfig")
        if is_need_config:
            default_version = self.config.configVersion
            if not os.path.exists(os.path.join(config_folder_path, config_filename)):
                os.makedirs(config_folder_path)
                self.config.fun_save_to_yml(config_folder_path, config_filename)
            self.config.fun_load_from_yml(config_folder_path, config_filename)
            version = self.config.configVersion
            if version != default_version:
                shutil.move(os.path.join(config_folder_path, config_filename),
                            os.path.join(config_folder_path, f"old_{config_filename}"))
                self.config.configVersion = default_version
                self.config.fun_save_to_yml(config_folder_path, config_filename)
                logger.warning("配置文件版本不一致，已经覆盖最新版配置，请修改配文件!")

    def execute_record(self, record, task: SpiderTask):
        """
        执行下载任务
        :param record: 记录(任务子项唯一值)
        :param task: 执行器
        :return: 执行时间
        """

        if record in self.records:
            logger.debug(f"[{record}]任务已经被执行，跳过本次执行!")
            return record
        task.execute(record)
        open(os.path.join(self.temp_folder_path, "records.txt"), "a", encoding="utf-8").write(record + "\n")
        logger.debug(f"[{record}]任务执行完毕!")
        return record

    def execute_task(self, task: SpiderTask, is_multi_thread=False, max_thread=8, is_tqdm_bar=False):
        """
        任务执行器
        :param task: 任务
        :param is_multi_thread: 是否启用多线程
        :param max_thread: 最大线程数
        :param is_tqdm_bar: 是否启用tqdm进度条[控制台进度条]显示进度(需要按照tqdm)
        :return:
        """
        bar = None
        if is_tqdm_bar:
            from tqdm import tqdm
            bar = tqdm(total=len(task.task_list))

        if is_multi_thread:
            import concurrent.futures

            executor = SpiderThreadPoolExecutor(max_thread)
            futures = []
            for record in task.task_list:
                future = executor.submit(self.execute_record, record, task)
                futures.append(future)
            for future in concurrent.futures.as_completed(futures):
                record = future.result()
                task.on_success(record)
                if bar:
                    bar.update()
                    bar.set_description(record)
            executor.shutdown()
        else:
            for record in task.task_list:
                self.execute_record(record, task)
                task.on_success(record)
                if bar:
                    bar.update()
                    bar.set_description(record)

    def download_from_res(self, res: Response, filename):
        """
        从res中下载文件
        :param res:
        :param filename:
        :return:
        """
        path = os.path.join(self.download_folder_path, filename)
        with open(path, "wb") as f:
            f.write(res.content)


