# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = _build
GH_PAGES_SOURCES = docs app utils config.py

# Internal variables.
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

.PHONY: clean
clean:
	rm -rf $(BUILDDIR)/*

.PHONY: html
html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

.PHONY: gh-pages
gh-pages:
	cd .. && git checkout gh-pages && git checkout master $(GH_PAGES_SOURCES) && git reset HEAD
	make html
	mv -fv _build/html/* ../
	cd .. && rm -rf $(GH_PAGES_SOURCES)
	git add -A
	git ci -m "Generated gh-pages for `git log master -1 --pretty=short --abbrev-commit`" && git push origin gh-pages ; git checkout master