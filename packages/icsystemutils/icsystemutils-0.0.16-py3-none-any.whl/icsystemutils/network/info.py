import socket

from pydantic import BaseModel


class NetworkInfo(BaseModel, frozen=True):

    hostname: str = ""
    ip_address: str = ""


def load() -> NetworkInfo:
    hostname = socket.gethostname()
    return NetworkInfo(hostname=hostname)
