# TrueGIXERJ_Utils

A collection of small but useful utility functions for use across multiple types of projects. Originally made for personal use, but made publicly available for anyone who might find them useful. This package will be continuously expanded with functions that I need — or may need — across different projects, so I don’t have to rewrite them every time (i'm lazy).

And yes, British spelling throughout, because I’m British.

## Features

Currently, TrueGIXERJ_Utils includes:

### `colours.py`

Functions to return coloured terminal text using ANSI escape codes, useful for logging or styling console output.

``red(text: str) -> str``: Returns the input text in red.

``yellow(text: str) -> str``: Returns the input text in yellow.

``green(text: str) -> str``: Returns the input text in green.

``cyan(text: str) -> str:`` Returns the input text in cyan.

Example usage:

```py
from TrueGIXERJ_Utils.colours import red
print(red("Error: Something went wrong!"))
```

### `files.py`

File utility functions, currently including:

``sanitise(filename: str) -> str``: Cleans up a filename by:

* Removing non-ASCII characters

* Stripping special characters not allowed in filenames

* Removing trailing spaces and dots

* Avoiding reserved names in Windows (e.g., CON, PRN, NUL, etc.)

Example usage:

```py
from TrueGIXERJ_Utils.files import sanitise
clean_name = sanitise("my*illegal:file?.txt")
print(clean_name)  # Output: myillegalfile.txt
```

### `logger.py`

Pre-made logging functionality, uses `colours.py` to colour the output of various logging levels.
The following logging levels exist and are appropriately coloured:

* `DEBUG` - Cyan
* `INFO` - Cyan
* `SUCCESS` - Green
* `WARNING` - Yellow
* `ERROR` - Red
* `CRITICAL` - Red

Example usage:

```py
from TrueGIXERJ_Utils.logger import logger
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.success("This is a success message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical error message")
```

## Installation

This package is available on PyPI, and can be installed by running:

``pip install TrueGIXERJ-Utils``

Alternatively, it can be manually installed by cloning the git repository:

``git clone https://github.com/YourUsername/TrueGIXERJ_Utils.git``

## Usage

Simply import the necessary modules and use the functions as described above.

```py
from TrueGIXERJ_Utils.colours import red, green
from TrueGIXERJ_Utils.files import sanitise
from TrueGIXERJ_Utils.logger import logger

print(red("This is an error message"))
print(sanitise("illegal:file/name.txt"))
logger.success("Yippee!")
```

## Project Structure

```
TrueGIXERJ_Utils/
├── __init__.py
├── colours.py
├── files.py
└── logger.py
```
## License

This project is licensed under the GNU General Public License v3.0. See the LICENCE file for details.

## Contributing

Due to the nature of the project, I will be updating it on an "as and when" basis. However; if you have any suggestions or improvements, feel free to submit a pull request or open an issue on GitHub. Or just come and shout at me loudly on my personal [Discord](https://discord.gg/zkhuwD5).