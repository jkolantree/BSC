PYTHON ?= python3
LATEXMK ?= latexmk
PAPER_PAGES ?= 75
SYNOPSIS_PAGES ?= 2
RELEASE_VERSION ?=
SOURCE_DATE_EPOCH ?= $(shell $(PYTHON) tools/release_identity.py --print-build-epoch)
export SOURCE_DATE_EPOCH

ifneq ($(filter dist dist-development dist-candidate dist-release,$(MAKECMDGOALS)),)
ifneq ($(origin VERSION),undefined)
$(error VERSION is no longer accepted; use RELEASE_VERSION with dist-candidate or dist-release)
endif
endif

.PHONY: paper synopsis fixture fixture-full manifest manifest-refresh inventory-contexts markdown test verify build-check dist dist-development dist-candidate dist-release ci

paper:
	@test -n "$(SOURCE_DATE_EPOCH)"
	mkdir -p build/paper
	cd paper/source && $(LATEXMK) -pdf -bibtex -interaction=nonstopmode -halt-on-error -file-line-error -outdir=../../build/paper On_Boundaries_of_Evidence.tex

synopsis:
	@test -n "$(SOURCE_DATE_EPOCH)"
	mkdir -p build/synopsis
	cd synopsis/source && $(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=../../build/synopsis Technical_Synopsis.tex

fixture:
	$(PYTHON) fixtures/F08_sqrt_square_sign/check_fixture.py
	$(PYTHON) fixtures/F10_coupled_surrogate/check_fixture.py
	$(PYTHON) fixtures/F11_collatz_recursive_sieve/check_fixture.py
	$(PYTHON) fixtures/F12_derived_holonomy_q/check_fixture.py
	$(PYTHON) fixtures/F13_lorentz_auxiliary_passivity/check_fixture.py

fixture-full: fixture
	$(PYTHON) fixtures/F11_collatz_recursive_sieve/check_fixture.py --full-scan

manifest:
	$(PYTHON) tools/verify_manifest.py

manifest-refresh:
	$(PYTHON) tools/update_manifest.py

inventory-contexts:
	$(PYTHON) tools/verify_inventory_contexts.py

markdown:
	$(PYTHON) tools/check_markdown_math.py

test:
	$(PYTHON) -m unittest discover -s tests -v

verify: inventory-contexts manifest fixture markdown test

build-check: paper synopsis
	$(PYTHON) tools/verify_build.py --paper-pages $(PAPER_PAGES) --synopsis-pages $(SYNOPSIS_PAGES)

dist: dist-development

dist-development:
	$(PYTHON) tools/build_archives.py --development

dist-candidate:
	$(PYTHON) tools/build_archives.py --candidate-version "$(RELEASE_VERSION)"

dist-release:
	$(PYTHON) tools/build_archives.py --release-version "$(RELEASE_VERSION)"

ci: verify build-check
