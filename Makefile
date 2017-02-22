.PHONY: docs test


test:
	python setup.py test

docs:
	rm -f docs/formation.rst
	sphinx-apidoc --no-toc --module-first --force --output-dir=docs/ formation
	$(MAKE) --directory=docs html


servedocs: docs
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .
