import multiprocessing

from jing.yahooer import Yahooer
from jing.aker import AKER

import pandas as pd

import warnings
warnings.filterwarnings("ignore")

pd.set_option('display.max_columns', None)

# 设置最大重试次数
MAX_RETRIES = 3

def producer(queue, inst):
    """生产者函数，读取股票列表并写入队列"""
    list_path = inst.getListPath()
    n = 0
    try:
        with open(list_path, 'r') as file:
            for line in file:
                code = line.strip()
                print(code)
                queue.put((code, 0))  # (股票代码, 当前重试次数)
                n += 1
    except FileNotFoundError:
        print(f"File '{list_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    print(f"生产者完成：所有任务已加入队列 {n}")

def consumer(queue, failed_queue, inst):
    """消费者函数，从队列获取任务并下载数据"""
    print(f"消费者 starts")
    while True:
        try:
            code, retries = queue.get(timeout=1)  # 从队列获取任务
        except multiprocessing.queues.Empty:
            break  # 队列为空时，退出循环
        
        print(f"消费者 {multiprocessing.current_process().name} 正在下载 {code}...")

        try:
            _ = inst.getK(code)
            print(f"{code} 下载成功")
        except Exception as e:
            print(f"{code} 下载失败: {e}")
            if retries < MAX_RETRIES:
                failed_queue.put((code, retries + 1))  # 重新加入失败队列
            else:
                print(f"{code} 达到最大重试次数，放弃")

def concurrent_download(inst):
    queue = multiprocessing.Queue()
    failed_queue = multiprocessing.Queue()

    # 生产者进程
    producer_process = multiprocessing.Process(target=producer, args=(queue, inst))
    producer_process.start()
    producer_process.join()

    print(f"生产者完成")

    # 启动多个消费者进程
    num_consumers = 5
    consumers = []
    for _ in range(num_consumers):
        print(f"消费者 starts 1")
        p = multiprocessing.Process(target=consumer, args=(queue, failed_queue, inst))
        print(f"消费者 starts 2")
        p.start()
        print(f"消费者 starts 3")
        consumers.append(p)

    # 等待所有消费者完成
    for p in consumers:
        p.join()

    # 处理失败任务（最多重试 MAX_RETRIES 次）
    retry_attempt = 1
    while not failed_queue.empty() and retry_attempt <= MAX_RETRIES:
        print(f"开始第 {retry_attempt} 轮重试...")
        while not failed_queue.empty():
            queue.put(failed_queue.get())

        consumers = []
        for _ in range(num_consumers):
            p = multiprocessing.Process(target=consumer, args=(queue, failed_queue))
            p.start()
            consumers.append(p)

        for p in consumers:
            p.join()

        retry_attempt += 1

    print("所有任务完成")

class D:
    def __init__(self, _market="us") -> None:
        self.market = _market
        if self.market == 'us':
            self.inst = Yahooer()
        elif self.market == 'hk' or self.market == 'cn':
            self.inst = AKER(self.market)
        else:
            self.inst = Yahooer()

    def download(self, _code=""):
        self.code = _code
        if len(_code) > 0:
            self.inst.getK(self.code)
        else:
            self.concurrent_download()

    def concurrent_download(self):
        queue = multiprocessing.Queue()
        failed_queue = multiprocessing.Queue()

        # 生产者进程
        producer_process = multiprocessing.Process(target=producer, args=(queue, self.inst))
        producer_process.start()
        producer_process.join()

        # 启动多个消费者进程
        num_consumers = 5
        consumers = []
        for _ in range(num_consumers):
            p = multiprocessing.Process(target=consumer, args=(queue, failed_queue, self.inst))
            p.start()
            consumers.append(p)

        # 等待所有消费者完成
        for p in consumers:
            p.join()

        print("第一次尝试完成，处理失败任务...")

        # 处理失败任务（最多重试 MAX_RETRIES 次）
        retry_attempt = 1
        while not failed_queue.empty() and retry_attempt <= MAX_RETRIES:
            print(f"开始第 {retry_attempt} 轮重试...")
            while not failed_queue.empty():
                queue.put(failed_queue.get())

            consumers = []
            for _ in range(num_consumers):
                p = multiprocessing.Process(target=consumer, args=(queue, failed_queue))
                p.start()
                consumers.append(p)

            for p in consumers:
                p.join()

            retry_attempt += 1

        print("所有任务完成")

if __name__=="__main__":
    d = D(_market='cn')
    d.download()

