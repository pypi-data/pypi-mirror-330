from enum import Enum


class JobStatus(str, Enum):
    COMPLETE = "complete"
    FAILED = "failed"
    RUNNING = "running"

    def __str__(self) -> str:
        return str(self.value)
