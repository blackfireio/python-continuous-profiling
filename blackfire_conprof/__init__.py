import sys, os
from blackfire_conprof import log
from .version import __version__

logger = log.get_logger(__name__)

def _print_help():
    help_string = '''Usage: blackfire-run <program>
       Enable code instrumentation, run a python program, and starts continuous profiling.
'''
    print(help_string)


def _add_bootstrap_to_pythonpath(bootstrap_dir):
    """
    Add our bootstrap directory to the head of $PYTHONPATH to ensure
    it is loaded before program code
    """
    python_path = os.environ.get('PYTHONPATH', '')

    if python_path:
        new_path = '%s%s%s' % (
            bootstrap_dir, os.path.pathsep, os.environ['PYTHONPATH']
        )
        os.environ['PYTHONPATH'] = new_path
    else:
        os.environ['PYTHONPATH'] = bootstrap_dir

def bootstrap_python():
    ext_dir = os.path.dirname(os.path.abspath(__file__))
    bootstrap_dir = os.path.join(ext_dir, 'bootstrap')

    _add_bootstrap_to_pythonpath(bootstrap_dir)

    logger.debug('PYTHONPATH: %s' % os.environ['PYTHONPATH'])

    cmd = sys.argv[1:]

    if len(cmd) == 0:
        _print_help()
        sys.exit(1)

    executable = sys.argv[1]
    args = sys.argv[2:]

    from shutil import which
    executable_path = which(executable)

    # execl(...) propagates current env. vars to the new process and thus runs 
    # with the new PYTHONPATH
    os.execl(executable_path, executable_path, *args)
