"""
author songjie
"""
from concurrent.futures import ThreadPoolExecutor, as_completed


class Thread(object):
    def __init__(self):
        pass

    def start_thread(self, data, fun, max_worker=15, is_test=False, **kwargs):
        """
        This function can start a thread pool
        :param is_test:
        :param max_worker:
        :param data:
        :param fun:
        :param kwargs:
        :return:
        """
        result = list()
        with ThreadPoolExecutor(max_workers=max_worker) as thread_pool:
            task_list = list()
            for item in data:
                task = thread_pool.submit(fun, item, **kwargs)
                task_list.append(task)
                if is_test:
                    break
            for i in as_completed(task_list):
                result.append(i.result())
        return result
