"""
From: https://www.open-open.com/blog/5035946046738849687.html

下面线程池代码片段，实现了线程池的雏形，展现了基本原理
"""


import time
import threading
from queue import Queue



class WorkManager(object):

    
    def __init__(self, work_num=1000, thread_num=2):
        self.work_queue = Queue()
        self.threads = []
        self.__init_work_queue(work_num)
        self.__init_thread_pool(thread_num)


    # 初始化线程
    def __init_thread_pool(self, thread_num):
        for i in range(thread_num):
            self.threads.append(Work(self.work_queue))

    # 初始化工作队列
    def __init_work_queue(self, jobs_num):
        for i in range(jobs_num):
            self.add_job(do_job, i)

    # 添加一项工作入队
    def add_job(self, func, *args):
        self.work_queue.put((func, list(args)))

    # 检查剩余队列任务
    def check_queue(self):
        return self.work_queue.qsize()

    # 等待所有线程运行完毕
    def wait_all_complete(self):
        for item in self.threads:
            if item.is_alive():item.join()


class Work(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()

    def run(self):
        # 让创建的线程在一定条件下关闭退出
        while True:
            try:
                # 任务异步出队，Queue内部实现了同步机制
                do, args = self.work_queue.get(block=False)
                do(args)
                # 通知系统任务完成
                self.work_queue.task_done()
            except Exception as errmsg:
                print(f"errmsg: {errmsg}")
                break


# 具体要做的事情
def do_job(args):
    print(f"Args: {args}")
    time.sleep(0.1)
    print(f"{threading.current_thread()}\t{list(args)}")


if __name__ == "__main__":
    start = time.time()
    work_manageer = WorkManager(10, 2) # or work_manager = WorkManager(10000, 2)
    work_manageer.wait_all_complete()
    end = time.time()
    print("cost all time: ", end-start)