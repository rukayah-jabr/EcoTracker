# EcoTracker Utilities

## Logger

The logger utility allows you to log messages to both the console and a file in the project's root 'logs' directory.

### Basic Usage

```python
from eco_tracker.utils.log import get_logger

# Get a logger with the default name (root logger)
logger = get_logger()

# Log messages at different levels
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
```
