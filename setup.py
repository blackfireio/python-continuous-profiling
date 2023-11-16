import io
from setuptools import setup

HOMEPAGE = "https://blackfire.io"
NAME = "blackfire_conprof"

exec(open('blackfire_conprof/version.py').read())
setup(
    name=NAME,
    version=__version__,
    license='MIT',
    author="Blackfire.io",
    packages=['blackfire_conprof'],
    author_email="support@blackfire.io",
    install_requires=["ddtrace==1.13.3"],
    description="Blackfire Continuous Profiler",
    long_description="Blackfire Continuous Profiler",
    long_description_content_type="test/x-rst",
    url=HOMEPAGE,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
