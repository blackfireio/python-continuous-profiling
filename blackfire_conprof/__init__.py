import re
import os
import platform
from ddtrace.profiling import Profiler as DDProfiler
from blackfire_conprof import log

DEFAULT_APPLICATION_NAME = "n/a"

logger = log.get_logger(__name__)


def _get_default_agent_socket():
    plat = platform.system()
    if plat == 'Windows':
        return 'tcp://127.0.0.1:8307'
    elif plat == 'Darwin':
        if platform.processor() == 'arm':
            return 'unix:///opt/homebrew/var/run/blackfire-agent.sock'
        else:
            return 'unix:///usr/local/var/run/blackfire-agent.sock'
    else:
        return 'unix:///var/run/blackfire/agent.sock'


def parse_network_address_string(agent_socket):
    pattern = re.compile(r'^([^:]+)://(.*)')
    matches = pattern.findall(agent_socket)
    if not matches:
        return None, None
    network, address = matches[0]
    return network, address


class Profiler(object):

    def __init__(self, application_name=None, agent_socket=None):
        agent_socket = agent_socket or os.environ.get(
            'BLACKFIRE_AGENT_SOCKET', _get_default_agent_socket()
        )

        network, address = parse_network_address_string(agent_socket)
        if network is None or address is None:
            raise ValueError(
                "Could not parse agent socket value: [%s]" % agent_socket
            )
        if network == "tcp":
            agent_socket = "http://%s" % (address)

        self._profiler = DDProfiler(
            service=application_name or DEFAULT_APPLICATION_NAME,
            url=agent_socket,
        )

    def start(self, *args, **kwargs):
        self._profiler.start(*args, **kwargs)

        logger.info("Started profiling")

    def stop(self):
        self._profiler.stop()

        logger.info("Profiling stopped")
