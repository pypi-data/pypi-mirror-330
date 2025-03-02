# lil_buff_writer

A simple writing utility for storing and retrieving messages.

Messages are formated as such `<name: bytes>/<size: u32><content: bytes>`

Instead of writing out many files, you can pack them into one file.
Writing out a stream of messages to a single blob allows you to write to a single destination instead of searching for files later.


## Features
- Write messages to a file with labeled names and content.
- Parse each of the messages from a stream.

## Installation
```sh
pip install lil_buff_writer
```

## Usage

### Writing Messages

```python
from lil_buff_writer import write_messages

messages = [(b"greeting", b"Hello, World!"), (b"farewell", b"Goodbye!")]
await write_messages(messages, "messages.dat")
```

### Reading Messages

```python
from lil_buff_writer import read_messages

with open("messages.dat", "rb") as f:
    for name, content in read_messages(f):
        print(f"{name.decode()}: {content.decode()}")
```

## License
Apache-2.0