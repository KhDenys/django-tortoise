.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

define DETOXME_PYSCRIPT
import sys
if __name__ == "__main__":
    envs = [env.strip() for env in sys.stdin.readlines()]
    print(
        "detox -e " + ",".join(env for env in envs[:-1]) + "; "
        "tox -e " + envs[-1]
    )
endef
export DETOXME_PYSCRIPT
DETOXME := python -c "$$DETOXME_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts


clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr example_project/.eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	find .tmp ! -name '.gitignore' ! -name '.tmp' -exec rm -fr {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

isort:
	isort --verbose --recursive src tests example_project setup.py

lint: ## check style with flake8
	flake8 src tests setup.py manage.py
	isort --verbose --check-only --diff --recursive src tests example_project setup.py
	python setup.py check --strict --metadata --restructuredtext
	check-manifest  --ignore .idea,.idea/* .

test: ## run tests quickly with the default Python
	pytest

tox: ## run tests on every Python version with tox
	tox --skip-missing-interpreters --recreate
	
detox: ## run tests on every Python version with tox
	#detox --skip-missing-interpreters --recreate
	tox -l | $(DETOXME) | sh

coverage: ## check code coverage quickly with the default Python
	coverage run --source src --parallel-mode setup.py test

coverage-report: coverage ## check code coverage and view report in the browser
	coverage combine --append
	coverage report -m
	coverage html
	$(BROWSER) tmp/coverage/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/django_tortoise*.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ -H "Api docs" src */migrations/*
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

docs-view: docs ## generate Sphinx HTML documentation, including API docs
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

upload: clean ## package and upload a release
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install

sync: ## Sync master and develop branches in both directions
	git checkout develop
	git pull origin develop --verbose
	git checkout master
	git pull origin master --verbose
	git checkout develop
	git merge master --verbose
	git checkout master
	git merge develop --verbose
	git checkout develop

bump: ## increment version number
	bumpversion patch

upgrade: ## upgrade frozen requirements to the latest version
	pipenv install -r requirements/production.txt
	pipenv install --dev -r requirements/development.txt
	pipenv lock --requirements > requirements/lock/production.txt
	pipenv lock --requirements --dev | grep -v '/fakturownia-python' -- > requirements/lock/development.txt
	sort requirements/lock/production.txt -o requirements/lock/production.txt
	sort requirements/lock/development.txt -o requirements/lock/development.txt
	git add Pipfile Pipfile.lock requirements/lock/*.txt
	git commit -m "Requirements upgrade"

release: lint upgrade detox sync bump dist ## build new package version release and sync repo
	git checkout develop
	git merge master --verbose
	git push origin develop --verbose
	git push origin master --verbose

publish: release upload ## release and upload new version

locales:
	# https://docs.djangoproject.com/en/1.11/ref/django-admin/#django-admin-makemessages
	python manage.py makemessages -v 3 --no-wrap --ignore ".*" --locale=pl_PL
	python manage.py compilemessages -v 3
