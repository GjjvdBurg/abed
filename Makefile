#
# Makefile for easier installation and cleanup.
#

PACKAGE=abed
DOC_DIR='./docs/'

.PHONY: help dist

.DEFAULT_GOAL := help

help:
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) |\
		 awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m\
		 %s\n", $$1, $$2}'

install: ## Install for the current user using the default python command
	python setup.py install --user

test: ## Run nosetests using the default nosetests command
	nosetests -v

cover: ## Test unit test coverage using default nosetests
	nosetests --with-coverage --cover-package=$(PACKAGE) \
		--cover-erase --cover-inclusive --cover-branches

clean: ## Clean build dist and egg directories left after install
	rm -rf ./dist ./build ./$(PACKAGE).egg-info
	rm -rf ./abed/*.pyc ./abed/*/*.pyc
	rm -rf ./abed/__pycache__ ./abed/html/__pycache__\
		./abed/results/__pycache__

dist: ## Make Python source distribution
	python setup.py sdist

docs: doc

doc: install ## Build documentation with sphinx
	$(MAKE) -C $(DOC_DIR) html
