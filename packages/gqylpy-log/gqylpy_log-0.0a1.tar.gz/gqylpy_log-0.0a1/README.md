[<img alt="LOGO" src="http://www.gqylpy.com/static/img/favicon.ico" height="21" width="21"/>](http://www.gqylpy.com)
[![Release](https://img.shields.io/github/release/gqylpy/gqylpy-log.svg?style=flat-square")](https://github.com/gqylpy/gqylpy-log/releases/latest)
[![Python Versions](https://img.shields.io/pypi/pyversions/gqylpy_log)](https://pypi.org/project/gqylpy_log)
[![License](https://img.shields.io/pypi/l/gqylpy_log)](https://github.com/gqylpy/gqylpy-log/blob/master/LICENSE)
[![Downloads](https://pepy.tech/badge/gqylpy_log)](https://pepy.tech/project/gqylpy_log)

# gqylpy-log
English | [中文](https://github.com/gqylpy/gqylpy-log/blob/master/README_CN.md)

> `gqylpy-log` is a secondary encapsulation of `logging` that allows for more convenient and quick creation of loggers. Using the `gqylpy_log` module, you can rapidly create `logging.Logger` instances and complete a series of logging configurations, making your code cleaner.

<kbd>pip3 install gqylpy_log</kbd>

### Using the Built-in Logger

`gqylpy_log` comes with a built-in logger based on `logging.StreamHandler`. You can directly call it as follows:
```python
import gqylpy_log as glog

glog.debug(...)
glog.info(...)
glog.warning(...)
glog.error(...)
glog.critical(...)
```

Its default configuration is as follows:
```python
{
    "level": "NOTSET",
    "formatter": {
        "fmt": "[%(asctime)s] [%(module)s.%(funcName)s.line%(lineno)d] "
               "[%(levelname)s] %(message)s",
        "datefmt": "%F %T"
    },
    "handlers": [{"name": "StreamHandler"}]
}
```

You can adjust the default logger configuration as needed:
```python
glog.default["level"] = "INFO"
```
However, please note that the default logger is created the first time a logging method is called. To make changes effective, you must modify the configuration before the first call.

### Creating a New Logger

The following example demonstrates how to obtain a logger with three handlers:
```python
import gqylpy_log as glog

log: logging.Logger = glog.__init__(
    "alpha",
    level="DEBUG",
    formatter={"fmt": "[%(asctime)s] [%(levelname)s] %(message)s"},
    handlers=[
        {"name": "StreamHandler"},
        {
            "name": "FileHandler",
            "level": "ERROR",
            "filename": "/var/log/alpha/error.log",
            "encoding": "UTF-8",
            "formatter": {"fmt": "[%(asctime)s] %(message)s", "datefmt": "%c"},
            "options": {"onlyRecordCurrentLevel": True}
        },
        {
            "name": "TimedRotatingFileHandler",
            "level": "INFO",
            "filename": "/var/log/alpha/alpha.log",
            "encoding": "UTF-8",
            "when": "D",
            "interval": 1,
            "backupCount": 7
        }
    ]
)

log.info(...)
```

Alternatively, if you prefer to always call it through the `gqylpy_log` module, specify the `gname` parameter:
```python
glog.__init__(..., gname="alpha")
```
Please note that specifying the `gname` parameter will override and permanently disable the default logger.
