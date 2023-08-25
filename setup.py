import io
from setuptools import setup
from blackfire_conprof import VERSION

HOMEPAGE = "https://blackfire.io"
NAME = "blackfire_conprof"

setup(
    name=NAME,
    version=VERSION,
    license='MIT',
    author="Blackfire.io",
    py_modules=['blackfire_conprof'],
    author_email="support@blackfire.io",
    install_requires=["ddtrace==1.13.3"],
    description="Blackfire Continuous Profiler",
    url=HOMEPAGE,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
