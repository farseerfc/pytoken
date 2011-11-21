#!/usr/bin/python2
from tokenply import *
from filter import *
from common import common
from ngram import filter_ngram,filter_sort_occur

def output_origin(occur,length,end_set,tokenseq):
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
    print u"%f,%d:%s\t%s\t%s"%(occur,length,end_set,
         tokenseq[end-length:end],";".join(pos))

class Ccf:
    def __init__(self):
        self.files={}
        self.file_list=[]
        self.sets=set()
        self.output=[]

    def file_no(self,filename):
        if not filename in self.files:
            self.files[filename]=len(self.files)
            self.file_list.append(filename)
        return self.files[filename]

    def __call__(self,*tup):
        self.append(*tup)

    def append(self,occur,length,end_set,tokenseq):
        self.output.append("#begin{set}")
        for end in end_set:
            start=end-length
            end=end-1
            while tokenseq[start].lexpos<0:start+=1
            while tokenseq[end].lexpos<0:end-=1
            filename=tokenseq[start].filename
            fileno = self.file_no(filename)
            stk=tokenseq[start]
            etk=tokenseq[end]
            self.output.append("0.%d\t%d,%d,%d\t%d,%d,%d\t0"%(fileno,
                stk.lineno,stk.column,stk.lexpos,
                etk.lineno,etk.lineno,etk.column))
        self.output.append("#end{set}")
        
    def get(self):
        result=[]
        result.append("#version: ccfinder 7.3.2")
        result.append("#format: classwise")
        result.append("#langspec: C")

        result.append("#begin{file description}")
        for filename in self.file_list:
            result.append("0.%d\t0\t0\t%s"%(self.file_no(filename),filename))
        result.append("#end{file description}")
        result.append("#begin{syntax error}")
        result.append("#end{syntax error}")
        result.append("#begin{clone}")
        result.extend(self.output)
        result.append("#end{clone}")
        return "\n".join(result)


def st_token(st,tokenseq,terms):
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
        yield (occur,length,end_set,tokenseq)

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

    ccf=Ccf()
    for tup in st_token(st,tokenseq,terms):
        ccf(*tup)
        #output_origin(*tup)
    print ccf.get()
