#!/usr/bin/env python2
from st import ST


def filter_no(gen):
    for pair in gen:
        yield pair

def filter_length(m,gen):
    for length,end_set in gen:
        if length > m:
            yield (length,end_set)

def filter_occur(m,gen):
    for legnth,end_set in gen:
        if len(end_set) > m:
            yield (length,end_set)

def filter_sort_length(gen):
    lst=[pair for pair in gen]
    lst.sort(key=lambda x:-x[0])
    return lst
    #for pair in lst:
    #    yield pair

def filter_mcs(gen):
    end_map = {}
    for length,end_set in gen:
        remove_set =set()
        for end in end_set:
            #start = end - length
            if end in end_map: 
                if length > end_map[end]:
                    assert(False)
                else:
                    remove_set.add(end)
            end_map[end]=length
        end_set = end_set . difference(remove_set)
        if len(end_set) > 1 : yield length,end_set

def filter_gst(eof_list,min_occur,gen):
    for length,end_set in gen:
        occur = [0 for i in eof_list]
        idx=0
        limit=eof_list[idx]
        for end in end_set:
            while True:
                if end<=limit:
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
        yield length,end_set


if __name__ == u"__main__":
    import sys
    string = sys.stdin.read()
    st = ST(string)
    result = []

    for length , end_set in \
            filter_mcs(
            filter_sort_length(
            filter_length(1,
            st.root.common()))):
        if len(end_set)==0:continue
        #if length < 2 : continue
        end = list(end_set)[0]
        print u"%s\t%d:%s"%(string[end-length:end],length,end_set)


