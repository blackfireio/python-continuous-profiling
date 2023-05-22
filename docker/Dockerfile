ARG PYTHON_VERSION

FROM python:${PYTHON_VERSION}
ENV PYTHONUNBUFFERED=1

# https://github.com/tianon/gosu/blob/master/INSTALL.md
RUN set -eux; \
	apt-get update; \
	apt-get install -y gosu; \
	rm -rf /var/lib/apt/lists/*; \
# verify that the binary works
	gosu nobody true

# py2 might throw permission errors as it by default uses /.cache folder
ENV PYTHON_EGG_CACHE=/opt/python-eggs
