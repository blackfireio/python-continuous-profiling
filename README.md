# Blackfire Continuous Profiler for Python

Blackfire Continuous Profiler continuously collects and uploads profiling data to the Blackfire servers. Once enabled, the profiler collects the relevant profiling information in configurable intervals and periodically uploads it to the Blackfire Agent. Blackfire Agent then forwards this information to the backend.

# How to use
## Prerequisites

* Python >= 3.7.0
* Blackfire Agent >= 2.13.0

## Installation

```shell
pip install blackfire_conprof
```

## Example

An example using the whole API interface:

1. Install dependencies

```shell
pip install blackfire_conprof
```

2. Create `example.py` with the following code

```python
from blackfire_conprof.profiler import Profiler

def foo():
    import time
    time.sleep(1.0)

profiler = Profiler(application_name="my-python-app", agent_socket="tcp://127.0.0.1:8307", labels={'my-extra-label': 'data'})
profiler.start()
foo()
profiler.stop()
```

3. Run Blackfire Agent (version 2.13.0 and up)

```
BLACKFIRE_SOCKET="tcp://127.0.0.1:8307" blackfire agent --log-level=4
```

4. Run the example application. (`python example.py`)
5. Profiler will send data to the Agent, and Agent will forward it to the Blackfire backend. Data then can be visualized at https://blackfire.io

# Enabling the profiler

There are two ways to enable the profiler:
 - via Code,
 - via Command Line.

## Code

```python
from blackfire_conprof.profiler import Profiler

profiler = Profiler()
profiler.start()
```

If you are working with gevent or any other library that uses pseudo-threads, and you also need to call

```
import blackfire_conprof.auto
```

as early as possible in your application. Example: for gevent applications to work correctly, this needs 
to be imported before `gevent.monkey.patch_all()`.

## Command line

Run your Python application as following:

```bash
blackfire-conprof python app.py
```

This will automatically enable the profiler just before your application runs.

# Contributing

Use `make help` to display an overview of useful commands for your dev environment.

