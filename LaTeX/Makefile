#### Makefile for systems using GNU Make

LATEX=xelatex
BIBTEX=bibtex


VzorMP.pdf: VzorMP.tex VzorMP.bib
	$(LATEX) VzorMP
	$(LATEX) VzorMP
	if [ -d "./PDF" ]; then mv VzorMP.pdf PDF; fi

VzorMP.bib: Bibliografie.bib 
	$(LATEX) VzorMP
	$(BIBTEX) VzorMP

%.pdf: %.tex
	$(BIBTEX) $<
	$(BIBTEX) $<

clean:
	$(RM) -v VzorMP.aux
	$(RM) -v VzorMP.bbl
	$(RM) -v VzorMP.blg
	$(RM) -v VzorMP.glg
	$(RM) -v VzorMP.glo
	$(RM) -v VzorMP.gls
	$(RM) -v VzorMP.ist
	$(RM) -v VzorMP.lof
	$(RM) -v VzorMP.log
	$(RM) -v VzorMP.lot
	$(RM) -v VzorMP.out
	$(RM) -v VzorMP.run.xml
	$(RM) -v VzorMP.toc
	$(RM) -v VzorMP-blx.bib
	if [ -d "./temp" ]; then rm  ./temp/* ; fi

mrproper: clean
	$(RM) -v VzorMP.pdf

# install TeX Live on Ubuntu/Debian Linux
install:
	sudo apt-get update
	sudo apt-get install -y texlive-xetex
	sudo apt-get install -y texlive-lang-czechslovak
	sudo apt-get install -y texlive-fonts-extra texlive-latex-extra texlive-fonts-recommended
	sudo apt-get install -y texlive-science texlive-pstricks
	sudo apt-get install -y texlive-bibtex-extra
	sudo apt-get install -y latexmk


