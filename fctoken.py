import tokenize,token


TK_REPR={
    56                     :'Encoding'      ,
    token.AMPER            :'&'             ,
    token.AMPEREQUAL       :'&='            ,
    token.AT               :'@'             ,
    token.CIRCUMFLEX       :'^'             ,
    token.CIRCUMFLEXEQUAL  :'^='            ,
    token.COLON            :':'             ,
    token.COMMA            :','             ,
    token.DEDENT           :'<==<'          ,
    token.DOT              :'.'             ,
    token.DOUBLESLASH      :'//'            ,
    token.DOUBLESLASHEQUAL :'//='           ,
    token.DOUBLESTAR       :'**'            ,
    token.DOUBLESTAREQUAL  :'**='           ,
    token.ELLIPSIS         :'..'            ,
    token.ENDMARKER        :'END'           ,
    token.EQEQUAL          :'=='            ,
    token.EQUAL            :'='             ,
    token.ERRORTOKEN       :'ERR'           ,
    token.GREATER          :'>'             ,
    token.GREATEREQUAL     :'>='            ,
    token.INDENT           :'>==>'          ,
    token.LBRACE           :'{'             ,
    token.LEFTSHIFT        :'<<'            ,
    token.LEFTSHIFTEQUAL   :'<<='           ,
    token.LESS             :'<'             ,
    token.LESSEQUAL        :'<='            ,
    token.LPAR             :'('             ,
    token.LSQB             :'['             ,
    token.MINEQUAL         :'-='            ,
    token.MINUS            :'-'             ,
    token.NAME             :'N'             ,
    token.NEWLINE          :'n'             ,
    token.NOTEQUAL         :'!='            ,
    token.NUMBER           :'1'             ,
    token.N_TOKENS         :'T'             ,
    token.OP               :'O'             ,
    token.PERCENT          :'%'             ,
    token.PERCENTEQUAL     :'%='            ,
    token.PLUS             :'+'             ,
    token.PLUSEQUAL        :'+='            ,
    token.RARROW           :'->'            ,
    token.RBRACE           :'}'             ,
    token.RIGHTSHIFT       :'>>'            ,
    token.RIGHTSHIFTEQUAL  :'>>='           ,
    token.RPAR             :')'             ,
    token.RSQB             :']'             ,
    token.SEMI             :';'             ,
    token.SLASH            :'/'             ,
    token.SLASHEQUAL       :'/='            ,
    token.STAR             :'*'             ,
    token.STAREQUAL        :'*='            ,
    token.STRING           :'S'             ,
    token.TILDE            :'T'             ,
    token.VBAR             :'|'             ,
    token.VBAREQUAL        :'|='            
    } 

FC_NONE     = 0x0
FC_ENCODING = 0x1
# keyword
FC_IF       = 0x100 
FC_DEF      = 0x101
FC_IMPORT   = 0x102
FC_CLASS    = 0x103
# op
FC_EQEQ     = 0x200
FC_EQ       = 0x201

FC_REPR = {
        FC_NONE     : 'none'        ,
        FC_ENCODING : 'encoding'    ,
        FC_IF       : 'if'          ,
        FC_DEF      : 'def'         ,
        FC_IMPORT   : 'import'      ,
        FC_CLASS    : 'class'       ,
        FC_EQEQ     : '=='          ,
        FC_EQ       : '='
        }


            
    NAME_MAP={
            'if'        :   FC_IF       ,
            'def'       :   FC_DEF      ,
            'import'    :   FC_IMPORT   ,
            'class'     :   FC_CLASS 
            }

    def canonize_name(self):
        if self.tk_str in PyToken.NAME_MAP:
            self.fc_type = PyToken.NAME_MAP[self.tk_str]

    OP_MAP = {
            '=='    :   FC_EQEQ     ,
            '='     :   FC_EQ       ,
            }

    def canonize_op(self):
        if self.tk_str in PyToken.OP_MAP:
            self.fc_type = PyToken.OP_MAP[self.tk_str]

    def canonize_encoding(self):
        self.fc_type = PyToken.FC_ENCODING

    TYPE_MAP={
            57                  : canonize_encoding ,
            token.NAME          : canonize_name  ,
            token.OP            : canonize_op
            }


    def canonize(self):
        if self.tk_type in PyToken.TYPE_MAP:
            PyToken.TYPE_MAP[self.tk_type](self)

class PyToken:
    def __init__(self,tk_type,tk_str,bg,end,ln,filename):
        self.fc_type  = PyToken.FC_NONE
        self.tk_type  = tk_type
        self.tk_str   = tk_str
        self.tk_bg    = bg
        self.tk_end   = end
        self.tk_ln    = ln
        self.filename = filename
        self.canonize()

    def __str__(self):
        if self.fc_type != PyToken.FC_NONE:
            return '  '+PyToken.FC_REPR[self.fc_type]
        if self.tk_type in  PyToken.TK_REPR:
            return ' !'+str(self.tk_type)+PyToken.TK_REPR[self.tk_type]
        else:
            return ' #'+str(self.tk_type)+token.tok_name[self.tk_type]



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
