PYTHON ?= python3
LATEXMK ?= latexmk

.PHONY: paper synopsis fixture manifest verify

paper:
	mkdir -p build/paper
	cd paper/source && $(LATEXMK) -pdf -bibtex -interaction=nonstopmode -halt-on-error -file-line-error -outdir=../../build/paper On_Boundaries_of_Evidence.tex

synopsis:
	mkdir -p build/synopsis
	cd synopsis/source && $(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=../../build/synopsis Technical_Synopsis.tex

fixture:
	$(PYTHON) fixtures/F08_sqrt_square_sign/check_fixture.py

manifest:
	sha256sum -c MANIFEST.sha256

verify: manifest fixture
