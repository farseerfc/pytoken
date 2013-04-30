#!/usr/bin/python2
from tokenply import *
from filter import *
from common import common
from ngram import filter_ngram,filter_sort_occur
from time import clock


def output_origin(occur, length, end_set, tokenseq):
    pos = []
    for end in end_set:
        start = end - length
        end = end - 1
        while tokenseq[start].lexpos < 0 : start += 1
        while tokenseq[end].lexpos < 0 : end -= 1
        filename = tokenseq[start].filename
        start_lexpos = tokenseq[start].lexpos
        start_lineno = tokenseq[start].lineno
        start_column = tokenseq[start].column
        end_lexpos = tokenseq[end].lexpos
        end_lineno = tokenseq[end].lineno
        end_column = tokenseq[end].column
        pos.append("u%s:(%d,%d,%d,%d,%d,%d)"%(filename,
            start_lexpos, start_lineno, start_column,
            end_lexpos, end_lineno, end_column))
 
    end = list(end_set)[0]
    return u"%f,%d:%s\t%s\t%s"%(occur, length, end_set,
         tokenseq[end-length : end], ";".join(pos))

class ClonePos:
    def __init__(self, fileno,
                 stk_lineno, stk_column, stk_lexpos,
                 etk_lineno, etk_column, etk_lexpos):
        self.fileno = fileno
        self.stk_lineno = stk_lineno
        self.stk_column = stk_column
        self.stk_lexpos = stk_lexpos
        self.etk_lineno = etk_lineno
        self.etk_column = etk_column
        self.etk_lexpos = etk_lexpos

class CloneSet:
    def __init__(self,length, end_set, tokenseq):
        self.length=length
        self.pos = []
        for end in end_set:
            start = end - length
            fileno = tokenseq[start].filename
            stk = tokenseq[start]
            etk = tokenseq[end]
            self.pos.append((fileno,
                stk.lineno, stk.column, stk.lexpos,
                etk.lineno, etk.column, etk.lexpos))
        end = list(end_set)[0]
        self.tokenseq = tokenseq[end-length : end].to_list()

class Ccf:
    def __init__(self, filelist):
        self.files = {}
        self.file_data = {}
        self.filelist = filelist
        self.clonesets=[]
        self.tokenseq=[]

    def file_no(self, filename):
        #if not filename in self.files:
        #    self.files[filename]=len(self.files)
        #    self.file_list.append(filename)
        return self.files[filename]

    def __call__(self, *tup):
        self.append(*tup)

    def append(self, length, end_set):
        self.clonesets.append(CloneSet(length, end_set, self.tokenseq))

    def output_ccf(self):
        for cloneset in self.clonesets:
            yield "#begin{set}"
            for pos in cloneset.pos:
                yield "0.%d\t%d,%d,%d\t%d,%d,%d\t55"%pos
                    #(pos.fileno,
                    #pos.stk_lineno, pos.stk_column, pos.stk_lexpos,
                    #pos.etk_lineno, pos.etk_column, pos.etk_lexpos)
            yield "#end{set}"
        
    def get_ccf(self):
        yield "#version: ccfinder 7.3.2"
        yield "#format: classwise"
        yield "#langspec: C"
        yield "#option: -b 30"
        yield "#option: -e char"
        yield "#option: -k 30"
        yield "#option: -r abcdfikmnoprsuv"
        yield "#option: -c wfg"
        yield "#option: -y"

        yield "#begin{file description}"
        for filename in self.filelist:
            yield "0.%d\t%d\t%d\t%s"%( \
            self.file_no(filename), \
            self.file_data[filename][0], \
            self.file_data[filename][1], \
            filename) 
        yield "#end{file description}"
        yield "#begin{syntax error}"
        yield "#end{syntax error}"
        yield "#begin{clone}"
        for line in self.output_ccf():
            yield line
        yield "#end{clone}"

    def register(self, filename, length, token_nr):
        self.file_data[filename] = (length, token_nr)
        self.files[filename] = len(self.files)


def st_token(st, terms, min_len, grp):
    #for length,end_set in \
            #filter_sort_occur( \
            #filter_ngram(tokenseq, , 4, \
    if grp:
        for length, end_set in \
                filter_gst(terms, 2, \
                filter_mcs( \
                filter_sort_length( \
                filter_length(min_len, \
                common(st))))):
            if len(end_set) == 0:continue
            yield (length, end_set)
    else:
        for length, end_set in \
                filter_mcs( \
                filter_sort_length( \
                filter_length(min_len, \
                common(st)))):
            if len(end_set) == 0:continue
            yield (length, end_set)



def filelist(file_list, min_len=32, grp=True):
    import sys
    #sys.setrecursionlimit(1<<16)
    clk_start = clock()
    terms = []

    #tokenseq = TokenSeq([])
    ccf = Ccf(file_list)
    st = ST(TokenSeq([]))
    last_term = 0

    #from multiprocessing import Pool
    #pool=Pool(processes=4)
    ts_list = map(tokenize, zip(file_list, range(0, len(file_list))))
    file_id = 0

    clk_read = clock()

    for f in file_list:
    #ts =tokenize(f)
        ts = ts_list[file_id]
        #tokenseq += ts
        last_term += len(ts)
        terms.append(last_term - 1)
        ccf.register(f, len(ts), len(open(f).readlines()))
        st.append(ts)
        file_id += 1
    clk_st = clock()

    #print >>sys.stderr,"End Building ST!"
    sys.stderr.flush()

    tokenseq = st.string
    ccf.tokenseq = tokenseq
    for length, end_set in st_token(st, terms, min_len, grp):
        ccf(length, end_set)
        #yield output_origin(occur, length, end_set, tokenseq)
    #for line in ccf.get():
    #    yield line
    
    clk_common = clock()
    print >>sys.stderr,"Read %f ST %f  Common %f Total %f"%(
           clk_read - clk_start,
           clk_st - clk_read,
           clk_common - clk_st,
           clk_common - clk_start)
    return ccf


if __name__==u"__main__":
    import sys
    for line in filelist(sys.argv[2]):
        print line
