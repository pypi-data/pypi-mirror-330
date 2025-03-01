from .ohttpy import Response
from typing import Iterator

def make_chunk_generator(response: Response) -> Iterator[bytes]:
    """
    Convert the response into a chunk-wise python generator
    """
    try:
        while True:
            chunk = response.chunk()
            if chunk is None:
                break
            yield bytes(chunk)
    finally:
        # todo drop the reqwest::response on rust side by implementing close()
        while response.chunk() is not None:
                continue