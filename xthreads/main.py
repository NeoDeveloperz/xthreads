import threading
import queue
import time

class TaskManager:
    def __init__(self, num_threads=4):
        self.task_queue = queue.Queue()
        self.threads = []
        self.num_threads = num_threads
        self._init_threads()

    def _init_threads(self):
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self._worker)
            thread.daemon = True  # Beendet die Threads, wenn das Hauptprogramm beendet wird
            thread.start()
            self.threads.append(thread)

    def _worker(self):
        while True:
            task = self.task_queue.get()
            if task is None:
                break
            task()
            self.task_queue.task_done()

    def add_task(self, task):
        self.task_queue.put(task)

    def wait_completion(self):
        self.task_queue.join()

    def stop_all(self):
        for _ in range(self.num_threads):
            self.task_queue.put(None)
        for thread in self.threads:
            thread.join()
