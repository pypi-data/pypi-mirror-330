import requests
from io import BytesIO
import datetime
from typing import Any
from ohttpy._generators import make_chunk_generator
from .ohttpy import Client, Response

class FileLikeStream:
    """
    Class to convert an OHTTPy response into a file-like stream as required by requests.response.raw.
    """
    def __init__(self, response: Response):
        self._chunk_gen = make_chunk_generator(response)
        self._buffer = bytearray()
        self.closed = False

    def read(self, size=-1) -> bytearray:
        if self.closed:
            raise ValueError("I/O operation on closed file.")

        if size == 0:
            return bytearray()

        # read entirety of remaining response
        if size < 0:
            parts = [self._buffer]
            for chunk in self._chunk_gen:
                parts.append(chunk)
            self._buffer = bytearray()
            return bytearray().join(parts)

        # read chunks until size amount or no more chunks
        while len(self._buffer) < size:
            try:
                chunk = next(self._chunk_gen)
            except StopIteration:
                break
            self._buffer.extend(chunk)

        ret = self._buffer[:size]
        self._buffer = self._buffer[size:]
        return ret

    def close(self) -> None:
        if not self.closed:
            self._chunk_gen.close()
            self.buffer = bytearray()
            self.closed = True


class Session(requests.Session):
    """
    Class to serve as a drop-in replacement from request.Session while enabling OHTTP encapsulation for all HTTP communication.
    """
    def __init__(self) -> None:
        super().__init__()
        self.client = Client()

    def to_bytes(self, data: Any) -> bytes:
        if isinstance(data, bytes):
            return data
        elif isinstance(data, str):
            return data.encode('utf-8')
        elif hasattr(data, 'read'):  # For file-like objects
            return data.read()
        elif data is None:
            return b""
        else:
            raise ValueError("Unsupported data type for conversion to bytes")


    def send(self, request: requests.PreparedRequest, **kwargs: Any) -> requests.Response:
        """
        Encrypt the request body, send the request, and decrypt the response.
        Args:
            request (PreparedRequest): The HTTP request to send.
            **kwargs (Any): Additional arguments for the send method.
        Returns:
            Response: The HTTP response.
        """
        # call binding to OHTTPy client
        response = self.client.send_request(
            method=request.method, url=request.url,
            headers=dict(request.headers), body=self.to_bytes(request.body))

        # translate response into requests.response compatible format
        status_code = response.status_code()
        headers = response.headers()

        # construct a compatible requests.Response object
        ret_response = requests.Response()
        ret_response.status_code = status_code
        ret_response.reason = requests.status_codes._codes[status_code][0].replace("_", " ").title()
        ret_response.headers = requests.structures.CaseInsensitiveDict(headers)

        # below fields are informational...
        ret_response.request = request
        ret_response.url = request.url

        # if streaming is requested, return a file-like streaming object in response
        if kwargs.get("stream", False):
            # simulate a file-like streaming object for compatibility
            ret_response.raw = FileLikeStream(response)
        else:
             # fully load content into memory (normal behavior)
            body = bytes().join([x for x in make_chunk_generator(response)])
            ret_response._content = body
            ret_response.raw = BytesIO(body)  # still provide raw access for consistency

        # set elapsed time (mocked, since we're not timing)
        ret_response.elapsed = datetime.timedelta(seconds=0)

        return ret_response