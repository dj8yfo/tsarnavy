import requests
import marshal
import types
import multiprocessing
from model_requests import get_url


class Consumer(multiprocessing.Process):
    def __init__(self, task_queue, result_queue):
        super().__init__()
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                self.task_queue.task_done()
                break
            print(f"{proc_name}: executing {next_task.kwargs}")
            answer = next_task()
            self.result_queue.put(answer)
            self.task_queue.task_done()


class Task:
    def __init__(self, work, *args, **kwargs):
        self.kwargs = kwargs
        self.work_code = marshal.dumps(work.__code__)
        self.args = args

    def __call__(self):
        code = marshal.loads(self.work_code)
        func = types.FunctionType(code, globals(), "work_unit")
        return {
            "result": func(*self.args),
            "args": self.kwargs,
        }

    def __str__(self):
        return f"{self.work_code}: {self.kwargs}"
