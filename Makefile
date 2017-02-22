.PHONY: docs

docs:
	sphinx-apidoc --no-toc --module-first --force --output-dir=docs/ formation
	$(MAKE) --directory=docs html
