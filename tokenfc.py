#!/usr/bin/python

import tokenize,token
from functools import total_ordering

@total_ordering
class PyToken:
    TK_REPR=dict([
            (57                     ,'Encoding'),
            (token.AMPER            ,'&'),
            (token.AMPEREQUAL       ,'&='),
            (token.AT               ,'@'),
            (token.CIRCUMFLEX       ,'^'),
            (token.CIRCUMFLEXEQUAL  ,'^='),
            (token.COLON            ,':'),
            (token.COMMA            ,','),
            (token.DEDENT           ,'<==<'),
            (token.DOT              ,'.'),
            (token.DOUBLESLASH      ,'//'),
            (token.DOUBLESLASHEQUAL ,'//='),
            (token.DOUBLESTAR       ,'**'),
            (token.DOUBLESTAREQUAL  ,'**='),
            (token.ELLIPSIS         ,'..'),
            (token.ENDMARKER        ,'END'),
            (token.EQEQUAL          ,'=='),
            (token.EQUAL            ,'='),
            (token.ERRORTOKEN       ,'ERR'),
            (token.GREATER          ,'>'),
            (token.GREATEREQUAL     ,'>='),
            (token.INDENT           ,'>==>'),
            (token.LBRACE           ,'{'),
            (token.LEFTSHIFT        ,'<<'),
            (token.LEFTSHIFTEQUAL   ,'<<='),
            (token.LESS             ,'<'),
            (token.LESSEQUAL        ,'<='),
            (token.LPAR             ,'('),
            (token.LSQB             ,'['),
            (token.MINEQUAL         ,'-='),
            (token.MINUS            ,'-'),
            (token.NAME             ,'N'),
            (token.NEWLINE          ,'n'),
            (token.NOTEQUAL         ,'!='),
            (token.NUMBER           ,'1'),
            (token.N_TOKENS         ,'T'),
            (token.OP               ,'O'),
            (token.PERCENT          ,'%'),
            (token.PERCENTEQUAL     ,'%='),
            (token.PLUS             ,'+'),
            (token.PLUSEQUAL        ,'+='),
            (token.RARROW           ,'->'),
            (token.RBRACE           ,'}'),
            (token.RIGHTSHIFT       ,'>>'),
            (token.RIGHTSHIFTEQUAL  ,'>>='),
            (token.RPAR             ,')'),
            (token.RSQB             ,']'),
            (token.SEMI             ,';'),
            (token.SLASH            ,'/'),
            (token.SLASHEQUAL       ,'/='),
            (token.STAR             ,'*'),
            (token.STAREQUAL        ,'*='),
            (token.STRING           ,'S'),
            (token.TILDE            ,'T'),
            (token.VBAR             ,'|'),
            (token.VBAREQUAL        ,'|=')
            ])



    def __init__(self,tk_type,tk_str,bg,end,ln,filename):
        self.tk_type  = tk_type
        self.tk_str   = tk_str
        self.tk_bg    = bg
        self.tk_end   = end
        self.tk_ln    = ln
        self.filename = filename

            
    def __str__(self):
        if self.tk_type in  PyToken.TK_REPR:
            return '!'+str(self.tk_type)+PyToken.TK_REPR[self.tk_type]
        else:
            return '#'+str(self.tk_type)+token.tok_name[self.tk_type]

    def __cmp__(self,other):
        return self.tk_type - other.tk_type

    def __repr__(self):
        return str(self)

    def __eq__(self,other):
        return self.tk_type == other.tk_type

    def __lt__(self,other):
        return self.tk_type < other.tk_type

    def __hash__(self):
        return hash(self.tk_type)

@total_ordering
class TokenSeq:
    def __init__(self,lst=[]):
        self.lst=lst

    def __len__(self):
        return len(self.lst)

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
        return repr(self.lst)

    def __eq__(self,other):
        return self.__cmp__(other) == 0

    def __lt__(self,other):
        return self.__cmp__(other) < 0


def tk_eat(tk_type,tk_str,bg,end,ln,filename):
    #print('Type:%s\t%s-%s\t%s\t%s'%(tk_type,bg,end,repr(tk_str),repr(ln)))
    t = PyToken(tk_type,tk_str,bg,end,ln,filename)
    return t

def tk(filename):
    lst=TokenSeq()
    for tupl in tokenize.tokenize(open(filename,'rb').readline):
        lst.append(tk_eat(*tupl,filename=filename))
    #print('\n'.join(str(x)+'\t'+x.tk_str for x in lst))
    return lst

   #     try:
   #     for tk_type,tk_str,bg,end,ln in tokenize(open(filename).readline):
   #         print('a')
   #         #print('Type:%s\t%s-%s\t%s\t%s\n'%(tk_type,bg,end,tk_str,ln))
   # except TypeError as te:
   #     return

if __name__=='__main__':
    import sys
    for f in sys.argv[1:]:
        nr_token = 0
        for x in tk(f):
            nr_token+=1
            print(str(nr_token)+'\t'+str(x)+'\t'+x.tk_str )
