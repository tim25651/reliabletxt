# reliabletxt

Reader and writer for ReliableTXT UTF-8 text files, with a Rust core exposed to Python
through PyO3.

## Prerequisites

- Python >=3.10, \<3.15

## Installation

```shell
pip install git+https://github.com/audivir/reliabletxt
```

## Usage

```python
from reliabletxt import ReliableTxtDocument

document = ReliableTxtDocument.load("input.txt")
document.text
document.save("output.txt")
```

## Acknowledgments

Ported from [stenway/ReliableTXT-Python](https://github.com/Stenway/ReliableTXT-Python) by
Stefan John / Stenway, originally released under the MIT license. See `NOTICE` for details.
This port keeps only UTF-8 and drops the byte order mark: it is no longer required on read
and no longer written on save.

## License

MIT
