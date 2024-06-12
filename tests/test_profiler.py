import unittest
import time
import os
from blackfire_conprof.profiler import Profiler

from contextlib import contextmanager

@contextmanager
def _patch(klass, name, fn):
    _orig_fn = getattr(klass, name)
    try:
        setattr(klass, name, fn)
        yield
    finally:
        setattr(klass, name, _orig_fn)

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

        class _context:
            nexportcalls = 0
        def _export(instance, events, start_time_ns, end_time_ns):
            from ddtrace.profiling.collector import stack_event
            
            stack_events = events.get(stack_event.StackSampleEvent, [])

            self.assertTrue(len(stack_events) > 0)
            self.assertTrue('foo' in str(stack_events))
            _context.nexportcalls += 1
        
        from ddtrace.profiling.exporter import http  as dd_http_exporter
        with _patch(dd_http_exporter.PprofHTTPExporter, "export", _export):
            prof = Profiler(period=0.1)
            prof.start()
            foo(0.3+0.2)
            prof.stop()

        self.assertTrue(_context.nexportcalls >= 1)

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
            self.assertTrue('probe_version' in prof._profiler.tags)
            self.assertTrue(prof._profiler.tags.get('project_id') == 'id-1')

    def test_profiler_creds(self):
        def _upload(instance, client, path, body, headers):
            self.assertTrue(headers.get('DD-API-KEY').decode()=='id-1:token-1')

        from ddtrace.profiling.exporter import http  as dd_http_exporter
        with _patch(dd_http_exporter.PprofHTTPExporter, "_upload", _upload):
            prof = Profiler(server_id='id-1', server_token='token-1', period=0.1)
            prof.start()
            time.sleep(0.2)
            prof.stop()

        def _upload2(instance, client, path, body, headers):
            self.assertEqual(headers.get('DD-API-KEY'), None)

        # no token
        with _patch(dd_http_exporter.PprofHTTPExporter, "_upload", _upload2):
            prof = Profiler(server_id='id-1', period=0.1)
            prof.start()
            time.sleep(0.2)
            prof.stop()
