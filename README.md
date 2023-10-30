# Blackfire Continuous Profiler for Python

Blackfire Continuous Profiler continuously collects and uploads profiling data to the Blackfire servers. Once enabled, the profiler collects the relevant profiling information in configurable intervals and periodically uploads it to the Blackfire Agent. Blackfire Agent then forwards this information to the backend.

# How to use
## Prerequisites

* Python >= 3.7.0
* Blackfire Agent >= 2.13.0

## Installation

TODO: After deciding the pkg name

## API

Here is the profiler's API:

```python
Profiler.__init___(self, application_name=None, agent_socket=None, 
                 server_id='', server_token='', labels={})
Profiler.start()
Profiler.stop()
```

`start` starts the continuous profiler probe.
It collects profiling information in the background and periodically uploads it to the Agent until `stop`` is called.

An example using default configuration:

```python
from blackfire_conprof.profiler import Profiler

profiler = Profiler(application_name='my-python-app')
profiler.start()
//...
profiler.stop()
```

## Example

1. Install dependencies

```shell
pip install XXX
```

2. Create `example.py` with the following code

```python
from blackfire_conprof.profiler import Profiler

def foo():
    import time
    time.sleep(1.0)

profiler = Profiler(application_name='my-python-app')
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

# Contributing

Use `make help` to display an overview of useful commands for your dev environment.

