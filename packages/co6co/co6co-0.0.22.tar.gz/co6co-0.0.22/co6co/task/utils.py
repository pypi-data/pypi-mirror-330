import time
from functools import wraps


def clock(func):
    """
    装饰器函数，用于计算函数的执行时间
    :param func: 被装饰的函数
    :return: 包装后的函数
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        with Timer(f"{func.__name__}(arg->{args}kwargs:{kwargs})"):
            result = func(*args, **kwargs)  # 调用原始函数并获取返回值
            return result
    return wrapper


class Timer:
    """
    # 示例用法 1 手动启动和停止
    timer = Timer("手动计时")
    timer.start()
    for i in range(1000000):
        pass
    timer.stop()

    # 示例用法 2 使用 with 语句自动管理计时
    with Timer("自动计时"):
        for i in range(1000000):
            pass
    """

    def __init__(self, activity_name="任务"):
        """
        初始化计时器类
        :param activity_name: 计时器描述名称，默认为 "任务"
        """
        self.activity_name = activity_name
        self.start_time = None
        self.end_time = None

    def start(self):
        """
        开始计时
        """
        self.start_time = time.time()
        print(f"{self.activity_name} 开始...")

    def stop(self):
        """
        停止计时并打印耗时
        """
        if self.start_time is None:
            print("请先调用 start() 方法开始计时！")
            return

        self.end_time = time.time()
        elapsed_time = self.end_time - self.start_time
        print(f"{self.activity_name} 结束，耗时：{elapsed_time:.6f} 秒")

    def __enter__(self):
        """
        支持 with 语句的进入方法
        """
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        支持 with 语句的退出方法
        """
        self.stop()
