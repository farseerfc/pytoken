#!/usr/bin/python
from tokenfc import *
from filter import *
from io import BytesIO 
from st_dot import *

if __name__=="__main__":
    import sys
    for f in sys.argv[1:]:
        tokenseq = tk(f)
        st = ST(tokenseq)
        # print("digraph ST{")
        # draw_tree(st)
        # print("}")
        lst =[] 
        for length,start_set in apply_filter(st,[\
                filter_mcs(),filter_length(25)]):
            if len(start_set)==0:continue
            lst.append((length,start_set))
        lst.sort(key=lambda p:-p[0])
        for length,start_set in lst:
            start = list(start_set)[0]
            print("%d:%s\t%s"%(length,start_set,
                tokenseq[start:start+length]))

    #print(tokenseq) 
