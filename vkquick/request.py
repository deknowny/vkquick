import asyncio
import ssl


class RequestsSession:
    def __init__(self, host: str):
        self.writer = self.reader = None
        self.host = host
        self.lock = asyncio.Lock()

    def _setup_connection(self):
        self.reader, self.writer = await asyncio.open_connection(
            self.host, 443, ssl=ssl.SSLContext()
        )

    async def write(self, body_query: bytes) -> None:
        if self.writer is None:
            await self._setup_connection()
        try:
            self.writer.write(body_query)
        except ConnectionResetError:
            await self._setup_connection()
            self.writer.write(body_query)
        finally:
            await self.writer.drain()

    async def read(self) -> bytes:
        content_length = 0
        async with self.lock:
            while True:
                line = await self.reader.readline()
                if line.startswith(b"Content-Length"):
                    line = line.decode("utf-8")
                    length = ""
                    for i in line:
                        if i.isdigit():
                            length += i
                    content_length = int(length)
                if line == b"\r\n":
                    break

            body = await self.reader.read(content_length)
            return body
