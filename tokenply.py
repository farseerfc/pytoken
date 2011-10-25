#!/usr/bin/python
from python_lex import PythonLexer
from functools import total_ordering
from codecs import unicode_escape_encode
from c_lexer import CLexer

ENDMARKER = "ENDMARKER"

class TokenPly:
    def __init__(self,lextoken,filename):
        self.type  = lextoken.type
        self.value   = lextoken.value
        self.lexpos    = lextoken.lexpos
        self.lineno    = lextoken.lineno
        self.filename = filename

    def __repr__(self):
        return "TokenPly(%s,%s,%d,%d,%s"% (
                self.type,repr(self.value),
                self.lineno,self.lexpos,repr(self.filename))

    def __eq__(self,other):
        if self.type == ENDMARKER:
            return other.type== ENDMARKER \
                    and other.filename == self.filename
        return self.type == other.type

    def __lt__(self,other):
        if self.type==ENDMARKER:
            if other.type != ENDMARKER:
                return False
            else: return self.filename < other.filename
        return self.type < other.type

    def __hash__(self):
        if self.type==ENDMARKER:
            return hash(self.filename)
        return hash(self.type)

@total_ordering
class TokenSeq:
    def __init__(self,lst):
        if type(lst) == list:
            self.lst=lst
            return
        self.lst=[]
        for token in lst:
            self.lst.append(token)

    def __len__(self):
        return len(self.lst)

    def __iadd__(self,other):
        if type(other)==TokenSeq:
            self.lst.extend(other.lst)
            return self
        else:
            return NotImplemented()


    def __getitem__(self,key):
        if type(key)==slice:
            return TokenSeq(self.lst[key])
        return self.lst[key]

    def __delitem__(self,key):
        del self.lst[key]

    def __setitem__(self,key,value):
        self.lst[key]=value

    def __cmp__(self,other):
        for i in range(0,len(self)):
            if self[i] == other[i]:continue
            if self[i] < other[i]: return -1
            if self[i] > other[i]: return 1
        return 0

    def __iter__(self):
        for item in self.lst:
            yield item

    def __reversed__(self):
        for item in reversed(self.lst):
            yield item

    def append(self,item):
        self.lst.append(item)

    def __repr__(self):
        return ",".join(x.type for x in self.lst)

    def __eq__(self,other):
        return self.__cmp__(other) == 0

    def __lt__(self,other):
        return self.__cmp__(other) < 0

def clex(text,filename):
    def errfoo(msg,a,b):
        import sys
        print(msg)
        sys.exit()
    def typelookup(namd):
        return False
    clex=CLexer(errfoo,typelookup)
    clex.build()
    clex.input(text)
    return clex

def pylex(text,filename):
    lexer=PythonLexer()
    lexer.input(text,filename)
    return lexer


def tokenize(filename):
    import sys
    fl=open(filename)
    print(filename,file=sys.stderr)
    sys.stderr.flush()
    lexer=pylex(fl.read(),filename)
    ts=TokenSeq([])
    for lextoken in lexer:
        ts.append(TokenPly(lextoken,filename))
    fl.close()
    return ts


if __name__=="__main__":
    import sys
    idx=0
    for filename in sys.argv[1:]:
        for tok in tokenize(filename):
            print("%d:\t%s"%(idx,tok))
            idx+=1

