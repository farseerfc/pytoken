#!/usr/bin/python2
from tokenply import *
from filter import *
from common import common
from st import log,FCLOG 
FCLOG = True


if __name__==u"__main__":
    import sys
    sys.setrecursionlimit(1<<16)
    terms= []
    file_id = 0
    tokenseq = TokenSeq([])
    log(u"TOKENSEQ:%d"%len(tokenseq))
    for f in sys.argv[1:]:
        file_id +=1
        tokenseq += tokenize(f)
        log(u"TOKENSEQ:%d"%len(tokenseq))
        terms.append(len(tokenseq))
    st=ST(tokenseq)
    log(terms)
    print >>sys.stderr,"End Building ST!"
    sys.stderr.flush()

    for length,start_set in \
            filter_mcs(
            filter_sort_length(
            filter_gst(terms,2,
            filter_length(30,
            common(st))))):
        if len(start_set)==0:continue
        start = list(start_set)[0]
        print u"%d:%s\t%s"%(length,start_set,
            tokenseq[start:start+length])


    log(unicode(terms) +unicode(len(tokenseq)))
