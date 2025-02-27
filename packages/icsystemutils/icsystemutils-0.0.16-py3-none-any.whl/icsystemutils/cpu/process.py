import os
import psutil
from pydantic import BaseModel


class Process(BaseModel, frozen=True):

    local_rank: int = 0
    pid: int = 0
    username: str


def load(local_rank: int = 0) -> Process:
    pid = os.getpid()

    ps = psutil.Process(pid)
    user = ps.username()

    return Process(local_rank=local_rank, pid=pid, username=user)
