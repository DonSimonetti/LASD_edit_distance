import datetime
import time
import psutil
import os


class MemoryUsageThread:
    def __init__(self):
        self.running = True

    def __del__(self):
        self.running = False

    def run(self):
        print("Started memory profiling thread\n")

        filename = "mem_usg_" + datetime.datetime.now().strftime("[%H-%M-%S]")

        while self.running:
            proc = psutil.Process(os.getpid())
            file = open(filename, "w")
            _str = datetime.datetime.now().strftime("[%H:%M:%S]").__str__() + " Mem usage: RSS=" + str(
                proc.memory_info().rss) + ", VMS=" + str(proc.memory_info().vms)
            file.close()
            time.sleep(1)
        return
