# Croustiistuff - Stuff I need for my projects

## Features
- **Color-coded logging** for better visibility
- **Two modes**: Classic (detailed) and Minimal (clean)
- **Customizable separators** in Minimal mode
- **Debug mode support**

## Installation
```sh
pip install croustiistuff
```

## Usage
### Basic Example
```python
from croustiistuff import Logger

logger = Logger(prefix="MyApp")

logger.success("Operation completed successfully!")
logger.warning("This is a warning message!")
logger.info("Informational message.")
logger.error("An error occurred!")
logger.debug("This is a debug message.")
```

### Changing Modes
```python
logger = Logger(mode="minimal", separator=" - ")
logger.info("This is a minimal log message")
```

## Example Output
### Classic Mode (Default)
```
[MyApp] | [12:34:56] | [SCC] -> [Operation completed successfully!]
[MyApp] | [12:34:56] | [WRN] -> [This is a warning message!]
[MyApp] | [12:34:56] | [INF] -> [Informational message.]
[MyApp] | [12:34:56] | [ERR] -> [An error occurred!]
```

### Minimal Mode
```
12:34:56 [INF] - Informational message.
```

## License
This project is licensed under the MIT License.

