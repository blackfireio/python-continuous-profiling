import unittest
import time
from blackfire_conprof import Profiler

class ProfilerTests(unittest.TestCase):
    def test_profiler_basic(self):
        def foo():
            time.sleep(0.1)
        prof = Profiler(agent_socket="tcp://127.0.0.1:8307")
        prof.start()
        foo()
        prof.stop()
