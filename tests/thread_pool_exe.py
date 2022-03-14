import time, threading, random
from concurrent.futures import ThreadPoolExecutor

class Executor:
    def __init__(self, workers_count=4):
        self.executor = ThreadPoolExecutor(max_workers=workers_count)
    
    def multiply(self, seq):
        print(seq * 10)
        time.sleep(random.randint(1, 3))
        print('Thread count:', threading.activeCount())
    
    def execute(self, seq):
        self.executor.submit(self.multiply, seq)

exe = Executor(4)

for i in range(100):
    exe.execute(i)
