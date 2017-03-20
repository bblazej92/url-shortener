# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXBUILD   = sphinx-build
BUILDDIR      = docs/_build
SOURCEDIR     = docs
CONFIGDIR     = docs
GH_PAGES_SOURCES = docs app utils config.py Makefile

.PHONY: clean
clean:
	rm -rf $(BUILDDIR)/*

.PHONY: html
html:
	$(SPHINXBUILD) -b html -c ${CONFIGDIR} ${SOURCEDIR} $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

.PHONY: gh-pages
gh-pages:
	git checkout gh-pages && git checkout master $(GH_PAGES_SOURCES) && git reset HEAD
	make html
	rm -rf _sources _static
	mv -fv --backup=off ${BUILDDIR}/html/* .
	rm -rf $(GH_PAGES_SOURCES)
	git add -A
	git commit -m "Generated gh-pages for `git log master -1 --pretty=short --abbrev-commit`" && git push origin gh-pages ; git checkout master