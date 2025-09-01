SHELL=/bin/bash -euo pipefail
.DEFAULT_GOAL := help

WHEEL_DIR ?= wheel_dist
PYTHON_VERSION?=3.13

COMPOSE=docker compose
ON_PYTHON=$(COMPOSE) run --rm --build python

clean: ## cleans the build artifacts
	rm -Rf build/ dist/ *.egg-info $(WHEEL_DIR)
.PHONY: clean

test:
	$(ON_PYTHON) ./scripts/test.sh
.PHONY: test

update-version:
	./scripts/update-version.sh
.PHONY: update-version

wheel:
	pip wheel --verbose --no-deps --wheel-dir=$(WHEEL_DIR) .
.PHONY: wheel

wheel-check:
	twine check $(WHEEL_DIR)/*
.PHONY: wheel-check

print-version: ## prints the current python conprof version
	@python -c "exec(open('blackfire_conprof/version.py').read()); print(__version__)"
.PHONY: print-version

doc-lint: ## Verify markdown rules
	docker run --rm -v ${PWD}:/data mivok/markdownlint src
.PHONY: doc-lint

build: build-docker clean ## build the python-conprof using a dockerized python runtime
	PYTHON_VERSION=$(PYTHON_VERSION) $(COMPOSE) run --rm python make update-version wheel wheel-check

build-docker:
	PYTHON_VERSION=$(PYTHON_VERSION) $(COMPOSE) build python
.PHONY: build-docker

release: ## release the python conprof
ifdef CI
	buildkite-agent artifact download '$(WHEEL_DIR)/*' .
endif
	./scripts/release.sh $(WHEEL_DIR)
.PHONY: release

print_wheel:
	@echo $(WHEEL_DIR)
.PHONY: print_wheel

##
### Misc
##

help: ## Displays help for Makefile commands
	@grep -hE '(^[a-zA-Z_-]+:.*?##.*$$)|(^###)' $(MAKEFILE_LIST) | grep -vhE '(^###[<>])' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m\n/'
.PHONY: help
