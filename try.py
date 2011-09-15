#!/usr/bin/env python2
from tokenize import *

def tk_eat(tk_type,tk_str,bg,end,ln):
    print('Type:%s\t%s-%s\t%s\t%s'%(tk_type,bg,end,repr(tk_str),repr(ln)))

def tk(filename):
    tokenize(open(filename).readline,tk_eat)

   #     try:
   #     for tk_type,tk_str,bg,end,ln in tokenize(open(filename).readline):
   #         print('a')
   #         #print('Type:%s\t%s-%s\t%s\t%s\n'%(tk_type,bg,end,tk_str,ln))
   # except TypeError as te:
   #     return

if __name__=='__main__':
    import sys
    for f in sys.argv[1:]:
        tk(f)
