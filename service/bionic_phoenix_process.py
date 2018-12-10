from enum import Enum
from datetime import datetime

class STATUS(Enum):
    RUNNING = 0
    SUCCESS = 1
    FAILED = 2

class BionicPhoenixProcess:
    def __init__(self, pid, command):
        self.pid = pid
        self.command = command
        self.status = STATUS.RUNNING
        self.start_time = datetime.now()

    def update(self, status):
        if status == 0:
            self.status = STATUS.SUCCESS
        else:
            self.status = STATUS.FAILED

    def to_string(self):
        return str(self.pid) + "\t" + self.start_time.strftime("%H:%M:%S") + "\t" + self.command + "\t" + str(self.status)
