.PHONY: clean test check publish

.DEFAULT: help
help:
	@echo "make test"
	@echo "       run tests"
	@echo "make clean"
	@echo "       clean python cache files"
	@echo "make doc"
	@echo "       build sphinx documentation"
	# @echo "make publish"
	# @echo "       publish the lib to the pypi repository"


test: 
	python setup.py test

clean-pyc:
	@find . -name '*.pyc' -delete
	@find . -name '__pycache__' -type d | xargs rm -fr
	@find . -name '.pytest_cache' -type d | xargs rm -fr

clean-dist:
	@find . -name 'dist' -type d | xargs rm -fr
	@find . -name 'build' -type d | xargs rm -fr
	@find . -name '*.egg-info' -type d | xargs rm -fr

clean-migrations:
	@find . -name 'migrations' -type d | xargs rm -fr
	@find . -name '*.db' -delete	

clean:clean-pyc clean-dist clean-migrations
	@echo "## Clean all data."

check:
	flake8 --ignore=E501,W291,F405,F403 --exclude=tests,migrations,__init__.py

# doc: 
# 	cd docs; make html

publish: 
	python setup.py publish