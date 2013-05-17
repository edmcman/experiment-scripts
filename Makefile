all:
	R CMD Sweave stats.Rnw
	pdflatex paper
