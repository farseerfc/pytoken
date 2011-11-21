#!/usr/bin/python2
from tokenply import *
from filter import *
from common import common
from ngram import filter_ngram,filter_sort_occur

def output_origin(occur,length,end_set,pos,tokenseq):
    print u"%f,%d:%s\t%s\t%s"%(occur,length,end_set,
         tokenseq[end-length:end],";".join(pos))

if __name__==u"__main__":
    import sys
    #sys.setrecursionlimit(1<<16)
    terms= []
    file_id = 0
    tokenseq = TokenSeq([])
    for f in sys.argv[2:]:
        file_id +=1
        tokenseq += tokenize(f)
        terms.append(len(tokenseq)-1)
    st=ST(tokenseq)
    print >>sys.stderr,"End Building ST!"
    sys.stderr.flush()

    #for length,end_set in \
    for occur,length,end_set in \
            filter_sort_occur(
            filter_ngram(tokenseq,sys.argv[1],4,
            filter_gst(terms,2,
            filter_mcs(
            filter_sort_length(
            filter_length(24,
            common(st))))))):
        if len(end_set)==0:continue
        pos=[]
        for end in end_set:
            start=end-length
            end=end-1
            while tokenseq[start].lexpos<0:start+=1
            while tokenseq[end].lexpos<0:end-=1
            filename=tokenseq[start].filename
            start_lexpos=tokenseq[start].lexpos
            start_lineno=tokenseq[start].lineno
            start_column=tokenseq[start].column
            end_lexpos=tokenseq[end].lexpos
            end_lineno=tokenseq[end].lineno
            end_column=tokenseq[end].column
            pos.append("%s:(%d,%d,%d,%d,%d,%d)"%(filename,
                start_lexpos,start_lineno,start_column,
                end_lexpos,end_lineno,end_column))

        end = list(end_set)[0]
        output_origin(occur,length,end_set,pos,tokenseq)

