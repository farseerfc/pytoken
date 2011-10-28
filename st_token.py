#!/usr/bin/python2
from tokenply import *
from filter import *
from common import common
from ngram import filter_ngram,filter_sort_occur

if __name__==u"__main__":
    import sys
    #sys.setrecursionlimit(1<<16)
    terms= []
    file_id = 0
    tokenseq = TokenSeq([])
    for f in sys.argv[1:]:
        file_id +=1
        tokenseq += tokenize(f)
        terms.append(len(tokenseq))
    st=ST(tokenseq)
    print >>sys.stderr,"End Building ST!"
    sys.stderr.flush()

    #for length,start_set in \
    for occur,length,start_set in \
            filter_sort_occur(
            filter_ngram(tokenseq,"input",4,
            filter_mcs(
            filter_sort_length(
            filter_gst(terms,2,
            filter_length(64,
            common(st))))))):
        if len(start_set)==0:continue
        start = list(start_set)[0]
        print u"%f,%d:%s\t%s"%(occur,length,start_set,
            tokenseq[start:start+length])


