#!/usr/bin/python2

from tokenply import tokenize

if __name__==u"__main__":
    import sys
    idx=0
    start=int(sys.argv[1])
    length=int(sys.argv[2])
    end=start+length
    idx=0
    print u"(%d,%d)"%(start,end)
    for f in sys.argv[3:]:
        for tok in tokenize(f):
            if idx == start:
                print tok.filename
            if idx in xrange(start,end):
                if tok.value!=None:
                    print tok.value, 
                    if u"\n" in tok.value:
                        print tok.lineno,; sys.stdout.write(u": ")
            idx+=1
                
    
