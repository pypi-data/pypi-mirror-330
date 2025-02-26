from ry import Bytes
from ry._types import Buffer
from ry.ryo3 import FsPathLike

async def read_async(path: FsPathLike) -> Bytes: ...
async def write_async(path: FsPathLike, data: Buffer) -> None: ...
