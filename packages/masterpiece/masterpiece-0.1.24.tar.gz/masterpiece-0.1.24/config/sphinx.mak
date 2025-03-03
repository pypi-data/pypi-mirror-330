# Minimal makefile for Sphinx documentation

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?= -W
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Files to link from root to docs/source
FILES_TO_LINK = README.rst CONTRIBUTING.rst LICENSE.rst CHANGELOG.rst TODO.rst
STATIC_DIR = _static

# Link creation target (for specific files)
link-files:
	@for file in $(FILES_TO_LINK); do \
		cp "../$$file" "$(SOURCEDIR)/$$file"; \
	done

# Ensure _static folder is copied to docs/source (if it doesn't exist)
copy-static:
	@if [ ! -d "$(SOURCEDIR)/$(STATIC_DIR)" ]; then \
		cp -r $(STATIC_DIR) "$(SOURCEDIR)/$(STATIC_DIR)"; \
	fi

# Ensure _static folder is linked to docs/source (if it doesn't exist)
link-static:
	@if [ ! -e "$(SOURCEDIR)/$(STATIC_DIR)" ]; then \
		cp "../$(STATIC_DIR)" "$(SOURCEDIR)/$(STATIC_DIR)"; \
	fi

# You can add a target to ensure links are created before build
# The 'html' target will work as expected
html: link-files copy-static
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option. $(O) is meant as a shortcut for $(SPHINXOPTS).
%:
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile link-files copy-static link-static
