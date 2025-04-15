SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = Dynamic_Factor_Tilted_Portfolio_with_Macro_Stress_Testing
SOURCEDIR     = .
BUILDDIR      = _build

.PHONY: help clean html

help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo "  clean    to clean the generated files"
	@echo "  html     to build the HTML documentation"

clean:
	@echo "Cleaning all generated files..."
	rm -rf $(BUILDDIR)/*

html:
	@echo "Building HTML documentation..."
	$(SPHINXBUILD) -b html $(SOURCEDIR) $(BUILDDIR)/html
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."