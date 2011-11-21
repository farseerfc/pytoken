#!/usr/bin/python2
#-----------------------------------------------------------------
# pycparser: c_lexer.py
#
# CLexer class: lexer for the C language
#
# Copyright (C) 2008-2011, Eli Bendersky
# License: BSD
#-----------------------------------------------------------------

import re
import sys

import ply.lex
from ply.lex import TOKEN
#from io import open




class CLexer(object):
    u""" A lexer for the C language. After building it, set the
        input text with input(), and call token() to get new 
        tokens.
        
        The public attribute filename can be set to an initial
        filaneme, but the lexer will update it upon #line 
        directives.
    """
    def __init__(self, error_func, type_lookup_func):
        u""" Create a new Lexer.
        
            error_func:
                An error function. Will be called with an error
                message, line and column as arguments, in case of 
                an error during lexing.
                
            type_lookup_func:
                A type lookup function. Given a string, it must
                return True IFF this string is a name of a type
                that was defined with a typedef earlier.
        """
        self.error_func = error_func
        self.type_lookup_func = type_lookup_func
        self.filename = u''
        
        # Allow either "# line" or "# <num>" to support GCC's
        # cpp output
        #
        self.line_pattern = re.compile(u'([ \t]*line\W)|([ \t]*\d+)')

    def build(self, **kwargs):
        u""" Builds the lexer from the specification. Must be
            called after the lexer object is created. 
            
            This method exists separately, because the PLY
            manual warns against calling lex.lex inside
            __init__
        """
        self.lexer = ply.lex.lex(object=self, **kwargs)

    def reset_lineno(self):
        u""" Resets the internal line number counter of the lexer.
        """
        self.lexer.lineno = 1

    def input(self, text,filename):
        self.filename=filename
        self.lexer.filename=filename
        self.lexer.input(text)
    
    #def token(self):
    #    g = self.lexer.token()
    #    return g

    def add_endmarker(self,stream):
        lineno=0
        lexpos=0
        for tok in stream:
            tok.filename=self.filename
            yield tok
            lineno=tok.lineno
            lexpos=tok.lexpos
        end=ply.lex.LexToken()
        end.type="ENDMARKER"
        end.value=None
        end.lineno=lineno
        end.lexpos=lexpos+1
        yield end

    def __iter__(self):
        stream=iter(self.lexer.token,None)
        stream=self.add_endmarker(stream)
        return stream

    ######################--   PRIVATE   --######################
    
    ##
    ## Internal auxiliary methods
    ##
    def _error(self, msg, token):
        location = self._make_tok_location(token)
        self.error_func(msg, location[0], location[1])
        self.lexer.skip(1)
    
    def _find_tok_column(self, token):
        i = token.lexpos
        while i > 0:
            if self.lexer.lexdata[i] == u'\n': break
            i -= 1
        return (token.lexpos - i) + 1
    
    def _make_tok_location(self, token):
        return (token.lineno, self._find_tok_column(token))
    
    ##
    ## Reserved keywords
    ##
    keywords = (
        u'AUTO', u'_BOOL', u'BREAK', u'CASE', u'CHAR', u'CONST', u'CONTINUE',
        u'DEFAULT', u'DO', u'DOUBLE', u'ELSE', u'ENUM', u'EXTERN',
        u'FLOAT', u'FOR', u'GOTO', u'IF', u'INLINE', u'INT', u'LONG', u'REGISTER',
        u'RESTRICT', u'RETURN', u'SHORT', u'SIGNED', u'SIZEOF', u'STATIC', u'STRUCT',
        u'SWITCH', u'TYPEDEF', u'UNION', u'UNSIGNED', u'VOID',
        u'VOLATILE', u'WHILE',
    )

    keyword_map = {}
    for keyword in keywords:
        if keyword == u'_BOOL':
            keyword_map[u'_Bool'] = keyword
        else:
            keyword_map[keyword.lower()] = keyword

    ##
    ## All the tokens recognized by the lexer
    ##
    tokens = keywords + (
        # Identifiers
        u'ID', 
        
        # Type identifiers (identifiers previously defined as 
        # types with typedef)
        u'TYPEID',
        
        # constants 
        u'INT_CONST_DEC', u'INT_CONST_OCT', u'INT_CONST_HEX',
        u'FLOAT_CONST', 
        u'CHAR_CONST',
        u'WCHAR_CONST',
        
        # String literals
        u'STRING_LITERAL',
        u'WSTRING_LITERAL',

        # Operators 
        u'PLUS', u'MINUS', u'TIMES', u'DIVIDE', u'MOD',
        u'OR', u'AND', u'NOT', u'XOR', u'LSHIFT', u'RSHIFT',
        u'LOR', u'LAND', u'LNOT',
        u'LT', u'LE', u'GT', u'GE', u'EQ', u'NE',
        
        # Assignment
        u'EQUALS', u'TIMESEQUAL', u'DIVEQUAL', u'MODEQUAL', 
        u'PLUSEQUAL', u'MINUSEQUAL',
        u'LSHIFTEQUAL',u'RSHIFTEQUAL', u'ANDEQUAL', u'XOREQUAL', 
        u'OREQUAL',

        # Increment/decrement 
        u'PLUSPLUS', u'MINUSMINUS',

        # Structure dereference (->)
        u'ARROW',

        # Conditional operator (?)
        u'CONDOP',
        
        # Delimeters 
        u'LPAREN', u'RPAREN',         # ( )
        u'LBRACKET', u'RBRACKET',     # [ ]
        u'LBRACE', u'RBRACE',         # { } 
        u'COMMA', u'PERIOD',          # . ,
        u'SEMI', u'COLON',            # ; :

        # Ellipsis (...)
        u'ELLIPSIS',
        
        # pre-processor 
        u'PPHASH',      # '#'
    )

    ##
    ## Regexes for use in tokens
    ##
    ##

    # valid C identifiers (K&R2: A.2.3)
    identifier = ur'[a-zA-Z_][0-9a-zA-Z_$]*'

    # integer constants (K&R2: A.2.5.1)
    integer_suffix_opt = ur'(u?ll|U?LL|([uU][lL])|([lL][uU])|[uU]|[lL])?'
    decimal_constant = u'(0'+integer_suffix_opt+u')|([1-9][0-9]*'+integer_suffix_opt+u')'
    octal_constant = u'0[0-7]*'+integer_suffix_opt
    hex_constant = u'0[xX][0-9a-fA-F]+'+integer_suffix_opt
    
    bad_octal_constant = u'0[0-7]*[89]'

    # character constants (K&R2: A.2.5.2)
    # Note: a-zA-Z are allowed as escape chars to support #line
    # directives with Windows paths as filenames (\dir\file...)
    #
    simple_escape = ur"""([a-zA-Z\\?'"])"""
    octal_escape = ur"""([0-7]{1,3})"""
    hex_escape = ur"""(x[0-9a-fA-F]+)"""
    newline_escape= ur"""(\n)"""
    bad_escape = ur"""([\\][^a-zA-Z\\?'"x0-7\n])"""

    escape_sequence = ur"""(\\("""+newline_escape+u'|'+simple_escape+u'|'+octal_escape+u'|'+hex_escape+u'))'
    cconst_char = ur"""([^'\\\n]|"""+escape_sequence+u')'    
    char_const = u"'"+cconst_char+u"'"
    wchar_const = u'L'+char_const
    unmatched_quote = u"('"+cconst_char+u"*\\n)|('"+cconst_char+u"*$)"
    bad_char_const = ur"""('"""+cconst_char+u"""[^'\n]+')|('')|('"""+bad_escape+ur"""[^'\n]*')"""

    # string literals (K&R2: A.2.6)
    string_char = ur"""([^"\\\n]|"""+escape_sequence+u')'    
    string_literal = u'"'+string_char+u'*"'
    wstring_literal = u'L'+string_literal
    bad_string_literal = u'"'+string_char+u'*'+bad_escape+string_char+u'*"'

    # floating constants (K&R2: A.2.5.3)
    exponent_part = ur"""([eE][-+]?[0-9]+)"""
    fractional_constant = ur"""([0-9]*\.[0-9]+)|([0-9]+\.)"""
    floating_constant = u'(((('+fractional_constant+u')'+exponent_part+u'?)|([0-9]+'+exponent_part+u'))[FfLl]?)'

    ##
    ## Lexer states
    ##
    states = (
        # ppline: preprocessor line directives
        # 
        (u'ppline', u'exclusive'),
    )

    
    def t_PPHASH(self, t):
        ur'[ \t]*\#'
        #m = self.line_pattern.match(
        #    t.lexer.lexdata, pos=t.lexer.lexpos)
        
        #if m:
        t.lexer.push_state(u'ppline')
        self.pp_line = self.pp_filename = None
        
            #~ print "ppline starts on line %s" % t.lexer.lineno
        #else:
        #    t.type = u'PPHASH'
        #    return t
    
    ##
    ## Rules for the ppline state
    ##
    @TOKEN(string_literal)
    def t_ppline_FILENAME(self, t):
        if self.pp_line is None:
            pass
            #self._error(u'filename before line number in #line', t)
        else:
            self.pp_filename = t.value.lstrip(u'"').rstrip(u'"')
            #~ print "PP got filename: ", self.pp_filename

    @TOKEN(decimal_constant)
    def t_ppline_LINE_NUMBER(self, t):
        if self.pp_line is None:
            self.pp_line = t.value
        else:
            # Ignore: GCC's cpp sometimes inserts a numeric flag
            # after the file name
            pass

    def t_ppline_NEXTLINE(self,t):
        ur'.*?\\\n'
        t.lexer.lineno+=t.value.count(u'\n')


    def t_ppline_NEWLINE(self, t):
        ur'.*?\n'

        if self.pp_line is None: 
            t.lexer.lineno+=t.value.count(u'\n')
        #    self._error(u'line number missing in #line', t)
        else:
            self.lexer.lineno = int(self.pp_line)
            
            if self.pp_filename is not None:
                self.filename = self.pp_filename
                
        t.lexer.pop_state()

    def t_ppline_PPLINE(self, t):
        ur'line'
        pass

    #def t_ppline_other(self, t):
    #    ur'.*?(\\|\n)'
    #    self.pp_nextline=None

    t_ppline_ignore = u' \t'

    def t_ppline_error(self, t):
        msg = u'invalid #line directive'
        self._error(msg, t)

    ##
    ## Rules for the normal state
    ##
    t_ignore = u' \f\t'

    # Newlines
    def t_NEWLINE(self, t):
        ur'\\?(\n)+'
        t.lexer.lineno += t.value.count(u"\n")

    def t_COMMENT(self,t):
        ur'(/\*(.|\n|@)*?\*/)|(//.*)'
        t.lexer.lineno+=t.value.count(u'\n')

    # Operators
    t_PLUS              = ur'\+'
    t_MINUS             = ur'-'
    t_TIMES             = ur'\*'
    t_DIVIDE            = ur'/'
    t_MOD               = ur'%'
    t_OR                = ur'\|'
    t_AND               = ur'&'
    t_NOT               = ur'~'
    t_XOR               = ur'\^'
    t_LSHIFT            = ur'<<'
    t_RSHIFT            = ur'>>'
    t_LOR               = ur'\|\|'
    t_LAND              = ur'&&'
    t_LNOT              = ur'!'
    t_LT                = ur'<'
    t_GT                = ur'>'
    t_LE                = ur'<='
    t_GE                = ur'>='
    t_EQ                = ur'=='
    t_NE                = ur'!='

    # Assignment operators
    t_EQUALS            = ur'='
    t_TIMESEQUAL        = ur'\*='
    t_DIVEQUAL          = ur'/='
    t_MODEQUAL          = ur'%='
    t_PLUSEQUAL         = ur'\+='
    t_MINUSEQUAL        = ur'-='
    t_LSHIFTEQUAL       = ur'<<='
    t_RSHIFTEQUAL       = ur'>>='
    t_ANDEQUAL          = ur'&='
    t_OREQUAL           = ur'\|='
    t_XOREQUAL          = ur'\^='

    # Increment/decrement
    t_PLUSPLUS          = ur'\+\+'
    t_MINUSMINUS        = ur'--'

    # ->
    t_ARROW             = ur'->'

    # ?
    t_CONDOP            = ur'\?'

    # Delimeters
    t_LPAREN            = ur'\('
    t_RPAREN            = ur'\)'
    t_LBRACKET          = ur'\['
    t_RBRACKET          = ur'\]'
    t_LBRACE            = ur'\{'
    t_RBRACE            = ur'\}'
    t_COMMA             = ur','
    t_PERIOD            = ur'\.'
    t_SEMI              = ur';'
    t_COLON             = ur':'
    t_ELLIPSIS          = ur'\.\.\.'

    t_STRING_LITERAL    = string_literal
    
    # The following floating and integer constants are defined as 
    # functions to impose a strict order (otherwise, decimal
    # is placed before the others because its regex is longer,
    # and this is bad)
    #
    @TOKEN(floating_constant)
    def t_FLOAT_CONST(self, t):
        return t

    @TOKEN(hex_constant)
    def t_INT_CONST_HEX(self, t):
        return t

    @TOKEN(bad_octal_constant)
    def t_BAD_CONST_OCT(self, t):
        msg = u"Invalid octal constant %d" % t.lineno
        self._error(msg, t)

    @TOKEN(octal_constant)
    def t_INT_CONST_OCT(self, t):
        return t

    @TOKEN(decimal_constant)
    def t_INT_CONST_DEC(self, t):
        return t

    # Must come before bad_char_const, to prevent it from 
    # catching valid char constants as invalid
    # 
    @TOKEN(char_const)
    def t_CHAR_CONST(self, t):
        return t
        
    @TOKEN(wchar_const)
    def t_WCHAR_CONST(self, t):
        return t
    
    @TOKEN(unmatched_quote)
    def t_UNMATCHED_QUOTE(self, t):
        msg = u"Unmatched '"
        self._error(msg, t)

    @TOKEN(bad_char_const)
    def t_BAD_CHAR_CONST(self, t):
        msg = u"Invalid char constant %s" % t.value
        self._error(msg, t)

    @TOKEN(wstring_literal)
    def t_WSTRING_LITERAL(self, t):
        return t
    
    # unmatched string literals are caught by the preprocessor
    
    @TOKEN(bad_string_literal)
    def t_BAD_STRING_LITERAL(self, t):
        msg = u"String contains invalid escape code %d" %t.lineno
        self._error(msg, t)

    @TOKEN(identifier)
    def t_ID(self, t):
        t.type = self.keyword_map.get(t.value, u"ID")
        
        if t.type == u'ID' and self.type_lookup_func(t.value):
            t.type = u"TYPEID"
            
        return t
    
    def t_error(self, t):
        msg = u'Illegal character %s in line %d' % (repr(t.value[0]),t.lineno)
        self._error(msg, t)


if __name__ == u"__main__":
    import sys
    text = open(sys.argv[1]).read()
    
   
    def errfoo(msg, a, b):
        sys.write(msg + u"\n")
        sys.exit()
    
    def typelookup(namd):
        return False

    def printme(lst):
        print u" ".join(unicode(x) for x in lst)
    
    clex = CLexer(errfoo, typelookup)
    clex.build()
    clex.input(text)
    
    while 1:
        tok = clex.token()
        if not tok: break
            
        #~ print type(tok)
        printme([tok.value, tok.type, tok.lineno, clex.filename, tok.lexpos])
        
