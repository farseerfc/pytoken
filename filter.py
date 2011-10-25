#!/usr/bin/env python2
from st import ST,log,FCLOG


def filter_no(gen):
    for pair in gen:
        yield pair

def filter_length(m,gen):
    for length,start_set in gen:
        if length > m:
            yield (length,start_set)

def filter_occur(m,gen):
    for legnth,start_set in gen:
        if len(start_set) > m:
            yield (length,start_set)

def filter_sort_length(gen):
    lst=[pair for pair in gen]
    lst.sort(key=lambda x:-x[0])
    for pair in lst:
        yield pair

def filter_mcs(gen):
    end_map = {}
    for length,start_set in gen:
        remove_set =set()
        for start in start_set:
            end = start + length
            if end in end_map: 
                if length > end_map[end]:
                    log(u"!!!!!!!!!!!!!!!end map conflict!!!!!!!!!!")
                else:
                    remove_set.add(start)
            end_map[end]=length
        start_set = start_set . difference(remove_set)
        if len(start_set) > 1 : yield length,start_set

def filter_gst(eof_list,min_occur,gen):
    for length,start_set in gen:
        occur = [0 for i in eof_list]
        idx=0
        limit=eof_list[idx]
        for start in start_set:
            while True:
                if start<limit:
                    occur[idx]=1
                    break
                elif idx < len(eof_list):
                    idx+=1
                    limit=eof_list[idx]
                else:
                    raise RuntimeError(u"start pos %d > limit %d"% \
                        (start,limit))
        nr_occur=sum(occur)
        if nr_occur < min_occur:continue
        yield length,start_set




if __name__ == u"__main__":
    import sys
    string = sys.stdin.read()
    st = ST(string)
    result = []

    for length , start_set in \
            filter_mcs(
            filter_sort_length(
            filter_length(1,
            st.root.common()))):
        if len(start_set)==0:continue
        #if length < 2 : continue
        start = list(start_set)[0]
        print u"%s\t%d:%s"%(string[start:start+length],length,start_set)


