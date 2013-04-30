#!/usr/bin/python2
from python_lex import PythonLexer
from codecs import unicode_escape_encode
from c_lexer import CLexer
#from io import open

ENDMARKER = u"ENDMARKER"

TOKENTYPE={}
TYPETOKEN=[]

STORE_VALUE=False

def token_type(type_str):
    #return type_str
    if type_str not in TOKENTYPE:
        TYPETOKEN.append(type_str)
        TOKENTYPE[type_str]=len(TYPETOKEN)-1
    return TOKENTYPE[type_str]


def type_token(token_id):
    #return token_id
    return TYPETOKEN[token_id]

#assert(token_type(ENDMARKER)==0)

class TokenPly(object):
    def __init__(self,lextoken,filename,column):
        self.type  = token_type(lextoken.type)
        if STORE_VALUE:
            self.value   = lextoken.value
        self.lexpos    = lextoken.lexpos
        self.lineno    = lextoken.lineno
        self.filename = filename
        self.column = column

    def __repr__(self):
        if STORE_VALUE:
            return u"TokenPly(%s,%s,%d,%d,%d,%s)"% (
                type_token(self.type),repr(self.value),
                self.lineno,self.column,self.lexpos,repr(self.filename))
        else:
            return u"TokenPly(%s,%d,%d,%d,%s)"% (
                type_token(self.type),
                self.lineno,self.column,self.lexpos,repr(self.filename))


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

    def __le__(self,other):
        return (self<other) or (self == other)

    def __gt__(self,other):
        return other < self

    def __ge__(self,other):
        return other <= self

    def __hash__(self):
        if self.type==0:
            return hash(self.filename)
        return hash(self.type)

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

    def to_list(self):
        return [type_token(x.type) for x in self.cano()]

    def cano(self):
        if self.start == 0 and self.length == len(self.lst): return
        return self.lst[self.start:self.start+self.length]
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

    def __le__(self,other):
        return (self < other) or (self == other)

    def __ge__(self,other):
        return other <= self

    def __gt__(self,other):
        return other < self


def filename_filter(filename,lexer):
    for tok in lexer:
        if lexer.filename == filename:
            yield tok

def find_column(ipt,token):
    last_cr=ipt.rfind('\n',0,token.lexpos)
    if last_cr<0:last_cr=0
    return token.lexpos-last_cr

def clex(filename,ipt):
    from c_pre import preprocess
    def errfoo(msg,a,b):
        import sys
        print msg
        sys.exit()
    def typelookup(namd):
        return False
    clex=CLexer(errfoo,typelookup)
    clex.build()
    clex.input(ipt,filename)
    return filename_filter(filename,clex)

def pylex(filename,ipt):
    lexer=PythonLexer()
    lexer.input(ipt,filename)
    return lexer

LEXER_MAP={"c":clex,"h":clex,"py":pylex}

def tokenize(pair): #filename,file_id):
    filename,file_id = pair
    import sys
    print >>sys.stderr, filename
    sys.stderr.flush()

    ext=filename.split(".")
    ext=ext[len(ext)-1]

    fd=open(filename)
    ipt=fd.read().decode("utf-8",errors="ignore")
    fd.close()

    lexer=LEXER_MAP[ext](filename,ipt)
    ts=TokenSeq([])
    for lextoken in lexer:
        ts.append(TokenPly(lextoken,file_id,find_column(ipt,lextoken)))
    return ts


if __name__==u"__main__":
    import sys
    idx=0
    list_file = [line.strip() for line in open(sys.argv[1]).readlines()]
    fileid=0
    for filename in list_file:
        fileid+=1
        for tok in tokenize((filename,fileid)):
            print u"%d:\t%s"%(idx,tok)
            idx+=1

