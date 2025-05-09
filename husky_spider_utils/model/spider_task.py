class SpiderTask:
    task_list: list = []  # 任务列表

    def __init__(self, spider):
        self.spider = spider

    def execute(self, task):
        """
        单任务执行器
        :param task:
        :return:
        """
        pass

    def on_success(self, task):
        pass
