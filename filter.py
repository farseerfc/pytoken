#!/usr/bin/env python
from st import ST,log

def filter_no():
    return lambda length,start_set: (length,start_set)

def filter_length(mini):
    return lambda length,start_set: \
            (length,start_set) if length>=mini else None

def filter_occurrence(mini):
    return lambda length,start_set: \
            (length,start_set) if len(start_set)>=mini else None

class McsFilter:
    def __init__(self):
        self.end_map = {}

    def __call__(self,length,start_set):
        remove_set =set()
        for start in start_set:
            end = start + length
            if end in self.end_map: 
                if length > self.end_map[end]:
                    log("!!!!!!!!!!!!!!!end map conflict!!!!!!!!!!")
                else:
                    remove_set.add(start)
            self.end_map[end]=length
        start_set = start_set . difference(remove_set)
        if len(start_set) > 0 : return length,start_set
        else: return None

def filter_mcs():
    return McsFilter()

def apply_filter(st,bool_func_set = [filter_no()]):
    for pair in st.root.common():
        #if all(map(lambda x:x(length,start_set),bool_func_set)):
        #    yield length,start_set
        for bool_func in bool_func_set:
            length ,start_set = pair
            pair = bool_func(length,start_set)
            if pair == None: break
        if pair != None: yield pair



if __name__ == "__main__":
    import sys
    string = sys.stdin.read()
    st = ST(string)
    result = []

    for length , start_set in apply_filter(st,
            [filter_mcs()]):
        if len(start_set)==0:continue
        #if length < 2 : continue
        start = list(start_set)[0]
        print("%s\t%d:%s"%(string[start:start+length],length,start_set))


