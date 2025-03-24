import io
from setuptools import setup

HOMEPAGE = "https://blackfire.io"
NAME = "blackfire_conprof"

with io.open('README.md', encoding='UTF-8') as f:
    long_description = f.read()

exec(open('blackfire_conprof/version.py').read())
setup(
    name=NAME,
    version=__version__,
    license='MIT',
    author="Blackfire.io",
    packages=['blackfire_conprof', 'blackfire_conprof.bootstrap'],
    author_email="support@blackfire.io",
    install_requires=["ddtrace==3.2.1"],
    description="Blackfire Continuous Profiler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "blackfire-conprof = blackfire_conprof:bootstrap_python",
        ]
    },
    url=HOMEPAGE,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
