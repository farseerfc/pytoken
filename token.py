import tokenize,token


class PyToken:
    TK_REPR=dict([
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
        self.tk_bg       = bg
        self.tk_end      = end
        self.tk_ln       = ln
        self.filename = filename

    def canonize(self):
        if self.tk_type == token.NAME:
            

    def __str__(self):
        if self.tk_type in  PyToken.TK_REPR:
            return PyToken.TK_REPR[self.tk_type]
        else:
            return ' '+token.tok_name[self.tk_type]



def tk_eat(tk_type,tk_str,bg,end,ln,filename):
    #print('Type:%s\t%s-%s\t%s\t%s'%(tk_type,bg,end,repr(tk_str),repr(ln)))
    t = PyToken(tk_type,tk_str,bg,end,ln,filename)
    return t

def tk(filename):
    lst=[]
    for tupl in tokenize.tokenize(open(filename,'rb').readline):
        lst.append(tk_eat(*tupl,filename=filename))
    print('\n'.join(str(x)+'\t'+x.tk_str for x in lst))

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
