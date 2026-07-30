PYTHON ?= python3
LATEXMK ?= latexmk
PAPER_PAGES ?= 50
SYNOPSIS_PAGES ?= 2
VERSION ?= 1.1.0
SOURCE_DATE_EPOCH ?= 1785369600

.PHONY: paper synopsis fixture manifest manifest-refresh markdown test verify build-check dist ci

paper:
	mkdir -p build/paper
	cd paper/source && $(LATEXMK) -pdf -bibtex -interaction=nonstopmode -halt-on-error -file-line-error -outdir=../../build/paper On_Boundaries_of_Evidence.tex

synopsis:
	mkdir -p build/synopsis
	cd synopsis/source && $(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=../../build/synopsis Technical_Synopsis.tex

fixture:
	$(PYTHON) fixtures/F08_sqrt_square_sign/check_fixture.py

manifest:
	$(PYTHON) tools/verify_manifest.py

manifest-refresh:
	$(PYTHON) tools/update_manifest.py

markdown:
	$(PYTHON) tools/check_markdown_math.py

test:
	$(PYTHON) -m unittest discover -s tests -v

verify: manifest fixture markdown test

build-check: paper synopsis
	$(PYTHON) tools/verify_build.py --paper-pages $(PAPER_PAGES) --synopsis-pages $(SYNOPSIS_PAGES)

dist:
	$(PYTHON) tools/build_archives.py --version $(VERSION) --source-date-epoch $(SOURCE_DATE_EPOCH)

ci: verify build-check
