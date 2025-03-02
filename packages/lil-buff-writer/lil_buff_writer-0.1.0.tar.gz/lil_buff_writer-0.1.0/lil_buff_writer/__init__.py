from typing import Iterable, Tuple, AsyncIterable
import logging

logger = logging.getLogger("lil_buff_writer")

try:
    import aiofiles
except ImportError:
    logger.error("async file writing requires aiofiles")



async def write_message_stream(messages: AsyncIterable[Tuple[bytes, bytes]], file_name: str):
    """
    Write messages to a file in the following format:
    <name: bytes>/<size: u32><content: bytes>

    name is a label for the message
    content is the actual message

    :param messages: An async iterable of tuples containing the name and content of the message
    :param file_name: The name of the file to write the messages to
    """
    buffer = bytearray()
    async for name, content in messages:
        buffer.extend(name)
        buffer.extend(b"/")
        buffer.extend(len(content).to_bytes(4, "little"))
        buffer.extend(content)

    async with aiofiles.open(file_name, "wb") as f:
        await f.write(buffer)


async def write_messages(messages: Iterable[Tuple[bytes, bytes]], file_name: str):
    """
    Write messages to a file in the following format:
    <name: bytes>/<size: u32><content: bytes>

    name is a label for the message
    content is the actual message

    :param messages: An iterable of tuples containing the name and content of the message
    :param file_name: The name of the file to write the messages to
    """
    buffer = bytearray()
    for name, content in messages:
        buffer.extend(name)
        buffer.extend(b"/")
        buffer.extend(len(content).to_bytes(4, "little"))
        buffer.extend(content)

    async with aiofiles.open(file_name, "wb") as f:
        await f.write(buffer)


def write_messages_sync(messages: Iterable[Tuple[bytes, bytes]], file_name: str):
    buffer = bytearray()
    for name, content in messages:
        buffer.extend(name)
        buffer.extend(b"/")
        buffer.extend(len(content).to_bytes(4, "little"))
        buffer.extend(content)

    with open(file_name, "wb") as f:
        f.write(buffer)


def each_chunk(stream) -> Iterable[Tuple[bytes, bytes]]:
    """
    Read messages from a stream in the following format:
    <name: bytes>/<size: u32><content: bytes>
    
    :param stream: The stream to read from
    :return: An iterable of tuples containing the name and content of the message
    """
    name = b""
    buffer = b""
    while True:
        chunk = stream.read(4096)
        buffer += chunk
        if not buffer:
            break

        try:
            name, buffer = buffer.split(b"/", 1)
            while len(buffer) < 4:
                chunk = stream.read(4096)
                if not chunk:
                    break
                buffer += chunk

            size = int.from_bytes(buffer[:4], "little")
            if len(buffer) - 4 < size:
                buffer += stream.read(size - len(buffer) + 4)
                yield name, buffer[4 : size + 4]
                name = b""
                buffer = buffer[size - len(buffer) + 4 :]
            else:
                yield name, buffer[4 : size + 4]
                name = b""
                buffer = buffer[size - len(buffer) + 4 :]

        except ValueError:
            break
