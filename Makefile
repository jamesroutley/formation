.PHONY: docs test

test:
	python setup.py test
	echo "For a more detailed coverage report, open htmlcov/index.html"

docs:
	rm -f docs/formation.rst
	sphinx-apidoc --no-toc --module-first --force --output-dir=docs/ formation
	$(MAKE) --directory=docs html

servedocs: docs
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .
