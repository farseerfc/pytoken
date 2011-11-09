#!/usr/bin/python2
from python_lex import PythonLexer
from functools import total_ordering
from codecs import unicode_escape_encode
from c_lexer import CLexer
from io import open

ENDMARKER = u"ENDMARKER"

TOKENTYPE={}
TYPETOKEN=[]

def token_type(type_str):
    if type_str not in TOKENTYPE:
        TYPETOKEN.append(type_str)
        TOKENTYPE[type_str]=len(TYPETOKEN)-1
    return TOKENTYPE[type_str]


def type_token(token_id):
    return TYPETOKEN[token_id]

assert(token_type(ENDMARKER)==0)

class TokenPly(object):
    def __init__(self,lextoken,filename):
        self.type  = token_type(lextoken.type)
        self.value   = lextoken.value
        self.lexpos    = lextoken.lexpos
        self.lineno    = lextoken.lineno
        self.filename = filename

    def __repr__(self):
        return u"TokenPly(%s,%s,%d,%d,%s)"% (
                type_token(self.type),repr(self.value),
                self.lineno,self.lexpos,repr(self.filename))

    def __eq__(self,other):
        if self.type == 0:
            return other.type== 0 \
                    and other.filename == self.filename
        return self.type == other.type

    def __lt__(self,other):
        if self.type==0:
            if other.type != 0:
                return False
            else: return self.filename < other.filename
        return self.type < other.type

    def __hash__(self):
        if self.type==0:
            return hash(self.filename)
        return self.type

class TokenSeq(object):
    def __init__(self,lst,start=0,length=-1):
        if length==-1:length=len(lst)
        self.start=start
        self.length=length
        if type(lst) == TokenSeq: raise NotImplemented
        if type(lst) == list:
            self.lst=lst
            return
        raise NotImplemented
        self.lst=[]
        for token in lst:
            self.lst.append(token)

    def cano(self):
        if self.start == 0 and self.length == len(self.lst): return
        raise NotImplemented

        self.lst=self.lst[self.start:self.start+self.length]
        self.start=0
        self.length=len(self.lst)

    def __len__(self):
        return self.length

    def __iadd__(self,other):
        if type(other)==TokenSeq:
            self.cano()
            self.lst.extend(other)
            self.length=len(self.lst)
            return self
        else:
            return NotImplemented


    def __getitem__(self,key):
        if type(key)==slice:
            return TokenSeq(self.lst,
                    self.start+key.start,
                    self.start+(key.stop-key.start))
        if key>=self.length: raise IndexError()
        return self.lst[self.start+key]

    def __setitem__(self,key,value):
        self.cano()
        if key>=self.length: raise IndexError()
        self.lst[self.start+key]=value

    def __cmp__(self,other):
        for i in xrange(0,len(self)):
            if self[i] == other[i]:continue
            if self[i] < other[i]: return -1
            if self[i] > other[i]: return 1
        return 0

    def __iter__(self):
        for i in xrange(self.start,self.start+self.length):
            yield self.lst[i]

    def append(self,item):
        self.cano()
        self.lst.append(item)
        self.length=len(self.lst)

    def __repr__(self):
        return ",".join(type_token(x.type) for x in self)

    def __eq__(self,other):
        return self.__cmp__(other) == 0

    def __lt__(self,other):
        return self.__cmp__(other) < 0

TokenSeq = total_ordering(TokenSeq)

def filename_filter(filename,lexer):
    for tok in lexer:
        if lexer.filename == filename:
            yield tok

def clex(filename):
    from c_pre import preprocess
    def errfoo(msg,a,b):
        import sys
        print msg
        sys.exit()
    def typelookup(namd):
        return False
    clex=CLexer(errfoo,typelookup)
    clex.build()
    clex.input(preprocess(filename),filename)
    return filename_filter(filename,clex)

def pylex(filename):
    fl=open(filename)
    lexer=PythonLexer()
    lexer.input(fl.read(),filename)
    fl.close()
    return lexer

LEXER_MAP={"c":clex,"h":clex,"py":pylex}

def tokenize(filename):
    import sys
    print >>sys.stderr, filename
    sys.stderr.flush()

    ext=filename.split(".")
    ext=ext[len(ext)-1]

    lexer=LEXER_MAP[ext](filename)
    ts=TokenSeq([])
    for lextoken in lexer:
        ts.append(TokenPly(lextoken,filename))
    return ts


if __name__==u"__main__":
    import sys
    idx=0
    for filename in sys.argv[1:]:
        for tok in tokenize(filename):
            print u"%d:\t%s"%(idx,tok)
            idx+=1

