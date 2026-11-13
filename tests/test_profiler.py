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
    def test_profiler_dd_envvars(self):
        with _env({"DD_PROFILING_ENABLED": '1'}):
            import blackfire_conprof.auto

            # ensure os.environ is preserved
            self.assertEqual(os.environ['DD_PROFILING_ENABLED'], '1')

    def test_profiler_basic_lib_dd(self):
        class _context:
            nexportcalls = 0
        def _upload(*args, **kwargs):
            _context.nexportcalls += 1

        from ddtrace.internal.datadog.profiling import ddup as dd_ddup_exporter
        with _patch(dd_ddup_exporter, "upload", _upload):
            prof = Profiler(period=0.1)
            prof.start()
            prof.stop()
        self.assertTrue(_context.nexportcalls >= 1)

    def test_profiler_basic(self):
        def foo(t):
            time.sleep(t)

        class _context:
            nexportcalls = 0
        def _upload(*args, **kwargs):
            _context.nexportcalls += 1

        from ddtrace.internal.datadog.profiling import ddup
        with _patch(ddup, "upload", _upload):
            prof = Profiler(period=0.1)
            prof.start()
            foo(0.3+0.2)
            prof.stop()

        self.assertTrue(_context.nexportcalls >= 1)

    def test_profiler_not_started_when_dd_profiler_running(self):
        from ddtrace.profiling import Profiler as DDProfiler

        dd_prof = DDProfiler()
        dd_prof.start()
        try:
            prof = Profiler(period=0.1)
            with self.assertLogs('blackfire_conprof.profiler', level='INFO') as logs:
                prof.start()
            self.assertEqual(len(logs.records), 1)
            self.assertEqual(logs.records[0].levelname, 'ERROR')
            self.assertIn('another ddtrace profiler is already running', logs.records[0].getMessage())
        finally:
            dd_prof.stop(flush=False)

    def test_profiler_not_started_in_uwsgi_master(self):
        from ddtrace.internal import uwsgi

        def _check_uwsgi(*args, **kwargs):
            raise uwsgi.uWSGIMasterProcess()

        prof = Profiler(period=0.1)
        with _patch(uwsgi, "check_uwsgi", _check_uwsgi):
            with self.assertLogs('blackfire_conprof.profiler', level='INFO') as logs:
                prof.start()
        self.assertEqual(len(logs.records), 1)
        self.assertEqual(logs.records[0].levelname, 'INFO')
        self.assertIn('Profiling not started in this process', logs.records[0].getMessage())

    def _assert_start_logs(self, prof, levelname, message):
        with self.assertLogs('blackfire_conprof.profiler', level='INFO') as logs:
            prof.start()
        self.assertEqual([r.levelname for r in logs.records], [levelname])
        self.assertIn(message, logs.records[0].getMessage())

    def test_profiler_not_started_with_deprecated_uwsgi_config(self):
        from ddtrace.internal import uwsgi

        def _check_uwsgi(*args, **kwargs):
            raise uwsgi.uWSGIConfigDeprecationWarning()

        with _patch(uwsgi, "check_uwsgi", _check_uwsgi):
            self._assert_start_logs(Profiler(period=0.1), 'INFO', 'Profiling not started in this process')

    def test_profiler_not_started_with_stale_active_instance(self):
        from ddtrace.internal import uwsgi
        from ddtrace.profiling import Profiler as DDProfiler

        def _check_uwsgi(*args, **kwargs):
            raise uwsgi.uWSGIMasterProcess()

        # a stopped profiler still registered as the active one
        with _patch(DDProfiler, "_active_instance", DDProfiler()):
            with _patch(uwsgi, "check_uwsgi", _check_uwsgi):
                self._assert_start_logs(Profiler(period=0.1), 'INFO', 'Profiling not started in this process')

    def test_is_running_without_ddtrace_internals(self):
        from blackfire_conprof.profiler import _is_running

        # an object without ddtrace's status attribute is assumed running
        self.assertTrue(_is_running(object()))

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
        class _context:
            upload_calls = 0

        def _upload(*args, **kwargs):
            _context.upload_calls += 1

        from ddtrace.internal.datadog.profiling import ddup

        # Test with credentials
        with _patch(ddup, "upload", _upload):
            prof = Profiler(server_id='id-1', server_token='token-1', period=0.1)
            self.assertEqual(prof._profiler.api_key, 'id-1:token-1')
            prof.start()
            time.sleep(0.2)
            prof.stop()

        self.assertGreater(_context.upload_calls, 0)

        # Test without token (server_id only)
        prof2 = Profiler(server_id='id-1', period=0.1)
        self.assertEqual(prof2._profiler.api_key, '')
        prof2.stop()
