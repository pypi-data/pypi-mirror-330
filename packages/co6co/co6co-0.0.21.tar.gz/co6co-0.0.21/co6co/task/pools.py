
from concurrent.futures import ThreadPoolExecutor
import queue


class limitThreadPoolExecutor(ThreadPoolExecutor):
    """
    限制进程池队列长度（默认队列长度无限）
    防止内存爆满的问题

    """

    def __init__(self, max_workers=None, thread_name_prefix=''):
        super().__init__(max_workers, thread_name_prefix)
        # 不甚至将时无限队列长度
        self._work_queue = queue.Queue(self._max_workers * 2)  # 设置队列大小
