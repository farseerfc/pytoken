default: draft

all: article draft trans handout beamer 

draft: main.draft.pdf

handout: main.handout.pdf

trans: main.trans.pdf

beamer: main.beamer.pdf

article: main.article.pdf

RM=rm -fv

main.draft.pdf: main.tex
	echo \\documentclass[english,xcolor=dvipsnames,bigger,draft]{beamer} >main.draft.tex
	echo \\input{main.tex} >>main.draft.tex
	xelatex main.draft.tex
	bibtex main.draft
	xelatex main.draft.tex
	$(RM) main.draft.tex

main.trans.pdf: main.tex
	echo \\documentclass[english,xcolor=dvipsnames,bigger,trans]{beamer} >main.trans.tex
	echo \\input{main.tex} >>main.trans.tex
	xelatex main.trans.tex
	bibtex main.trans
	xelatex main.trans.tex
	$(RM) main.trans.tex

main.handout.pdf: main.tex
	echo \\documentclass[english,xcolor=dvipsnames,bigger,handout]{beamer} >main.handout.tex
	echo \\input{main.tex} >>main.handout.tex
	xelatex main.handout.tex
	bibtex main.handout
	xelatex main.handout.tex
	$(RM) main.handout.tex

main.beamer.pdf: main.tex
	echo \\documentclass[english,xcolor=dvipsnames,bigger]{beamer} >main.beamer.tex
	echo \\input{main.tex} >>main.beamer.tex
	xelatex main.beamer.tex
	bibtex main.beamer
	xelatex main.beamer.tex
	xelatex main.beamer.tex
	$(RM) main.beamer.tex

main.article.pdf: main.tex
	echo \\documentclass{article} >main.article.tex
	echo \\usepackage{beamerarticle} >>main.article.tex
	echo \\input{main.tex} >>main.article.tex
	xelatex main.article.tex
	bibtex main.article
	xelatex main.article.tex
	$(RM) main.article.tex

pure:
	rm -fv main.{draft,handout,beamer,article,trans}.{aux,log,nav,out,snm,toc,tex,bbl,blg,vrb}
	rm -fv main.{aux,log,nav,out,snm,toc,bbl,blg,vrb}
	$(RM) texlog
	$(RM) *~

clean:  pure
	rm -fv main.{draft,handout,beamer,article,trans}.pdf
	$(RM) main.pdf


