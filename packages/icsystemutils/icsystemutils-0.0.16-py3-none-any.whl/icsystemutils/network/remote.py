from pathlib import Path
import logging

from pydantic import BaseModel

import fabric
import fabric.transfer

logger = logging.getLogger(__name__)


class Host(BaseModel, frozen=True):
    """
    Class representing some network location - can
    be used to put or get files to or from that location
    """

    name: str


def upload(source: Path, host: Host, target: Path, cxn: fabric.Connection | None):
    """
    Upload a file at the source location to the target location
    on the host. Optionally include an existing fabric connection.
    """

    if not cxn:
        cxn = fabric.Connection(host.name)

    cxn.run(f"mkdir -p {target.parent}")
    transfer = fabric.transfer.Transfer(cxn)
    transfer.put(str(source), str(target))
    cxn.close()


def download(host: Host, source: Path, target: Path, cxn: fabric.Connection | None):
    """
    Download a file from the source location on the host to the
    local target location. Optionally use an existing fabric connection.
    """

    if not cxn:
        cxn = fabric.Connection(host.name)

    transfer = fabric.transfer.Transfer(cxn)
    transfer.get(str(source), str(target))
    cxn.close()


def can_connect(cxn) -> bool:
    try:
        cxn.open()
    except Exception as e:
        logger.error(e)
        return False
    cxn.close()
    return True
