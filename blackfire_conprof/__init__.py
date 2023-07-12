import re
import os
import platform
import collections
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

_CustomLabel = collections.namedtuple("_CustomLabel", ["name", "env_var"])
_blackfire_labels = [
    _CustomLabel(name="project_id", env_var="PLATFORM_PROJECT"),
]

class Profiler(object):

    def __init__(self, application_name=None, agent_socket=None, labels={}):
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

        if application_name is None:
            application_name = os.environ.get(
                "BLACKFIRE_CONPROF_APP_NAME") or os.environ.get(
                "PLATFORM_APPLICATION_NAME")
            # if application_name is None, DD fills with the current running module name

        for label in _blackfire_labels:
            # don't override if user defined
            if label in labels:
                continue

            env_value = os.environ.get(label.env_var)
            if env_value:
                labels[label.name] = env_value

        # init default labels
        # runtime, language and runtime_version are already set by DD
        labels["runtime_os"] = "my-os"
        labels["runtime_arch"] = "my-arch"
        
        self._profiler = DDProfiler(
            service=application_name,
            tags=labels,
            url=agent_socket,
        )


    def start(self, *args, **kwargs):
        self._profiler.start(*args, **kwargs)

        logger.info("Started profiling")

    def stop(self):
        self._profiler.stop()

        logger.info("Profiling stopped")
