default: draft

all: article draft trans handout beamer pure

draft: main.draft.pdf

handout: main.handout.pdf

trans: main.trans.pdf

beamer: main.beamer.pdf

article: main.article.pdf

main.draft.pdf: main.tex
	echo "\\documentclass[english,xcolor=dvipsnames,10pt,draft]{beamer}" >main.draft.tex
	echo "\\input{main.tex}" >>main.draft.tex
	xelatex main.draft.tex
	xelatex main.draft.tex
	rm -v main.draft.tex

main.trans.pdf: main.tex
	echo "\\documentclass[english,xcolor=dvipsnames,10pt,trans]{beamer}" >main.trans.tex
	echo "\\input{main.tex}" >>main.trans.tex
	xelatex main.trans.tex
	xelatex main.trans.tex
	rm -v main.trans.tex

main.handout.pdf: main.tex
	echo "\\documentclass[english,xcolor=dvipsnames,10pt,handout]{beamer}" >main.handout.tex
	echo "\\input{main.tex}" >>main.handout.tex
	xelatex main.handout.tex
	xelatex main.handout.tex
	rm -v main.handout.tex

main.beamer.pdf: main.tex
	echo "\\documentclass[english,xcolor=dvipsnames,10pt]{beamer}" >main.beamer.tex
	echo "\\input{main.tex}" >>main.beamer.tex
	xelatex main.beamer.tex
	xelatex main.beamer.tex
	rm -v main.beamer.tex

main.article.pdf: main.tex
	echo "\\documentclass{article}" >main.article.tex
	echo "\\usepackage{beamerarticle}" >>main.article.tex
	echo "\\input{main.tex}" >>main.article.tex
	xelatex main.article.tex
	xelatex main.article.tex
	rm -v main.article.tex


pure:
	rm -fv main.{draft,handout,beamer,article,trans}.{aux,log,nav,out,snm,toc,tex}
	rm -fv main.{aux,log,nav,out,snm,toc}
	rm -fv texlog

clean:  pure
	rm -fv main.{draft,handout,beamer,article,trans}.pdf
	rm -fv main.pdf


