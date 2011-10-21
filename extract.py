#!/usr/bin/python

from tokenply import tokenize

if __name__=="__main__":
    import sys
    idx=0
    start=int(sys.argv[1])
    length=int(sys.argv[2])
    end=start+length
    idx=0
    print("(%d,%d)"%(start,end))
    for f in sys.argv[3:]:
        for tok in tokenize(f):
            if idx == start:
                print(tok.filename)
            if idx in range(start,end):
                if tok.value!=None:
                    print(tok.value,end=" ") 
                    if "\n" in tok.value:
                        print(tok.lineno,end=": ")
            idx+=1
                
    
