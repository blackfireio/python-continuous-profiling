import unittest
import time
import os
from blackfire_conprof import Profiler

from contextlib import contextmanager

@contextmanager
def _patch_export(export_func):
    from ddtrace.profiling.exporter import http  as dd_http_exporter
    _orig_export = dd_http_exporter.PprofHTTPExporter.export
    try:
        dd_http_exporter.PprofHTTPExporter.export = export_func
        yield
    finally:
        dd_http_exporter.PprofHTTPExporter.export = _orig_export

@contextmanager
def _env(env_var_pairs):
    orig_env = os.environ.copy()
    for k, v in env_var_pairs.items():
        os.environ[k] = v
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(orig_env)

class ProfilerTests(unittest.TestCase):
    def test_profiler_basic(self):
        def foo(t):
            time.sleep(t)

        nexportcalls = 0
        def _export(instance, events, start_time_ns, end_time_ns):
            nonlocal nexportcalls
            from ddtrace.profiling.collector import stack_event
            
            stack_events = events.get(stack_event.StackSampleEvent, [])

            self.assertTrue(len(stack_events) > 0)
            self.assertTrue('foo' in str(stack_events))
            nexportcalls += 1
        
        with _patch_export(_export):
            prof = Profiler(period=0.1)
            prof.start()
            foo(0.5+0.1)
            prof.stop()

        self.assertTrue(nexportcalls >= 5)

    def test_profiler_appname(self):
        with _env({"BLACKFIRE_CONPROF_APP_NAME": 'app1', "PLATFORM_APPLICATION_NAME" : 'app2'}):
            prof = Profiler(application_name='app3')
            self.assertEqual(prof._profiler.service, 'app3')
            prof.stop()

            prof = Profiler()
            self.assertEqual(prof._profiler.service, 'app1')
            prof.stop()

        with _env({"PLATFORM_APPLICATION_NAME" : 'app2'}):
            prof = Profiler()
            self.assertEqual(prof._profiler.service, 'app2')
            prof.stop()
    
    def test_profiler_params(self):
        with _env({"PLATFORM_PROJECT" : 'id-1'}):
            prof = Profiler()
            self.assertTrue('runtime_os' in prof._profiler.tags)
            self.assertTrue('runtime_arch' in prof._profiler.tags)
            self.assertTrue(prof._profiler.tags.get('project_id') == 'id-1')
