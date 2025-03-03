<h1 align="center">zns-logging</h1>

<h3 align="center">A simple and flexible logging library for Python</h3>

# Installation

```bash
pip install zns-logging
```

# Usage

```python
from zns_logging.ZnsLogger import ZnsLogger

logger = ZnsLogger(__name__, "DEBUG")

logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
```

# Output

```
[2025-01-26 23:22:06] [DEBUG   ] [__main__]: This is a debug message
[2025-01-26 23:22:06] [INFO    ] [__main__]: This is an info message
[2025-01-26 23:22:06] [WARNING ] [__main__]: This is a warning message
[2025-01-26 23:22:06] [ERROR   ] [__main__]: This is an error message
[2025-01-26 23:22:06] [CRITICAL] [__main__]: This is a critical message
```

# Change Log

```markdown
1.0.0
- Status: Yanked
- Reason: The `colorama` dependency was missing from `install_requires`, causing errors during logger usage.

1.0.1
- Status: Released
- Changes: Added `colorama` to `install_requires`.

1.0.2
- Status: Released
- Changes: Added description and other metadata to `Setup.py`.

1.0.3
- Status: Released
- Changes: Removed unnecessary variables from `Setup.py`.

1.0.4
- Status: Released
- Changes: Update `zns_logging.py` logic.

1.0.5 & 1.0.6 & 1.0.7
- Status: Yanked
- Reason: Unnecessary releases.

1.0.8
- Status: Released
- Changes: Rename `zns_logging.py` to `ZnsLogging.py` and update logic.

1.0.9
- Status: Released
- Changes: Update automatically create log directory.

1.1.0
- Status: Released
- Changes: Change function `get_logger` to class `ZnsLogger`.

1.1.1
- Status: Released
- Changes: Remove `ZnsLogging.py`.

1.1.2
- Status: Released
- Changes:
    - Update auto create log directory.
    - `log_and_raise` now does not need to pass the caller's name.
```
