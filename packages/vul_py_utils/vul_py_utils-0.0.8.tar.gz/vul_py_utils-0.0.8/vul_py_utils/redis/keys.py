import enum

class TaskStatus(enum.Enum):
    pending = 0
    in_process = 1
    done = 2
    failed = 3
    cancelled = 4

    

