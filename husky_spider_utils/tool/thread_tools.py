import queue
from concurrent.futures import ThreadPoolExecutor


class SpiderThreadPoolExecutor(ThreadPoolExecutor):
    """
    修改线程池修改队列数, 解决线程池占满内存问题
    """

    def __init__(self, max_workers=None, thread_name_prefix=''):
        """
    	重写队列数
    	"""
        super().__init__(max_workers, thread_name_prefix)
        self._work_queue = queue.Queue(self._max_workers * 2)
