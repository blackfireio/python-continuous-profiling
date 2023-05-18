SHELL=/bin/bash -euo pipefail
.DEFAULT_GOAL := help

##
### Tests
##

clean:
	rm -Rf build/ && rm -Rf dist/ && cd src/ && find . -name '*.pyc' -delete
.PHONY: clean

install: ## Runs tests suite
	python setup.py install
.PHONY: install

test: install
	python -m unittest discover -vf
.PHONY: test

doc-lint: ## Verify markdown rules
	docker run --rm -v ${PWD}:/data mivok/markdownlint src
.PHONY: doc-lint


##
### Misc
##

help: ## Displays help for Makefile commands
	@grep -hE '(^[a-zA-Z_-]+:.*?##.*$$)|(^###)' $(MAKEFILE_LIST) | grep -vhE '(^###[<>])' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m\n/'
.PHONY: help
