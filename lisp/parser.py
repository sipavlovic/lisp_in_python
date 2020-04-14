

from .common import *
from .environment import environment2str

# ----------- Tokenizer, Parser, Untokenizer ----------------

# Count opening (+1) and closing (-1) brackets; if 0 no then no remaining brackets to close
def bracket_count(tokens):
    cnt = 0
    for t,v in tokens:
        if t==TOKEN_LBRACKET: cnt += 1
        elif t==TOKEN_RBRACKET: cnt -= 1
    return cnt

# Returns next atom token (or empty) and remaining string
def get_atom(s):
    token = ''
    i = 0
    while i<len(s):
        c = s[i]
        if c not in WHITESPACE+"()":
            token += c
            i += 1
            continue
        else:
            break
    return token,s[len(token):]

# Returns string value (without quotes) (or empty) and remaining string (also doing "")
def get_string(s):
    token = ''
    i = 1
    while i<len(s):
        if s[i:i+2]=='""':
            token += '"'
            i += 2
            continue
        c = s[i:i+1]    
        if c in NEWLINES:
            raise Exception("String error: string not closed properly")
        elif c is not '"':
            token += c
            i += 1
            continue
        else:
            i += 1
            break       
    #print("get_string:",token,'<%s>'%s[i:])         
    return token,s[i:]

# Returns comment value
def get_comment(s):
    token = ''
    i = 0
    while i<len(s):
        c = s[i]
        if c not in NEWLINES:
            token += c
            i += 1
            continue
        else:
            break
    return token,s[len(token):]

TOKEN_DICT = {
        '(':TOKEN_LBRACKET,       
        ')':TOKEN_RBRACKET,
        "'":TOKEN_QUOTE,
        "`":TOKEN_BACKQUOTE,
        ",":TOKEN_UNQUOTE,
        ".":TOKEN_DOT
}

# Tokenizer (lexer) function - returns list of tokens
def tokenizer(s):
    tokens = []
    while len(s)>0:
        # splice-unquote
        if s[:2]==",@":
            tokens.append((TOKEN_SPLICE_UNQUOTE,s[:2]))        
            s = s[2:]
            continue     
        # whitespace
        if s[:1] in WHITESPACE:
            s = s[1:]
            continue
        # token dict collection
        if s[:1] in TOKEN_DICT:
            tokens.append((TOKEN_DICT[s[:1]],s[:1]))        
            s = s[1:]
            continue            
        # strings       
        if s[:1]=='"':        
            token,s = get_string(s)
            tokens.append((TOKEN_STRING,token))        
            continue    
        # comments
        if s[:1]==';':        
            token,s = get_comment(s)
            continue                                            
        # atoms: numbers and symbols
        token,s = get_atom(s)
        if len(token)>0:
            try:
                tokens.append((TOKEN_NUMBER,int(token)))        
            except ValueError:
                try:
                    tokens.append((TOKEN_NUMBER,float(token)))        
                except:
                    tokens.append((TOKEN_SYMBOL,token.upper()))        
            continue                            
        raise Exception("Tokenizer error")
    return tokens

# Parser function
def parser(tokens):
    l = parse_next(tokens)
    if len(tokens)>0:
        raise SyntaxError('unparsed tokens remaines: %s'%tokens)
    return l

# Parse next token
def parse_next(tokens):
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    ttype,token = tokens.pop(0)
    if ttype==TOKEN_QUOTE: 
        return Cons(asym(TOKEN_QUOTE),Cons(parse_next(tokens)))
    if ttype==TOKEN_BACKQUOTE: 
        return Cons(asym(TOKEN_BACKQUOTE),Cons(parse_next(tokens)))
    if ttype==TOKEN_UNQUOTE: 
        return Cons(asym(TOKEN_UNQUOTE),Cons(parse_next(tokens)))
    if ttype==TOKEN_SPLICE_UNQUOTE: 
        return Cons(asym(TOKEN_SPLICE_UNQUOTE),Cons(parse_next(tokens)))
    elif ttype==TOKEN_LBRACKET:
        cons = Cons()
        while tokens[0][0] != TOKEN_RBRACKET:
            if tokens[0][0] == TOKEN_DOT:
                tokens.pop(0) # removing dot
                cons = append(cons,parse_next(tokens))
                if tokens[0][0] == TOKEN_RBRACKET:
                    break
                raise SyntaxError('invalid dot syntax')    
            else:
                cons = append(cons,Cons(parse_next(tokens)))
        tokens.pop(0) # removing next right bracket
        return cons
    elif ttype==TOKEN_NUMBER: 
        return anum(token)
    elif ttype==TOKEN_STRING: 
        return astr(token)
    elif ttype in (TOKEN_SYMBOL,TOKEN_DOT): 
        return asym(token)
    elif ttype==TOKEN_RBRACKET:
        raise SyntaxError('unexpected )')
    else: 
        raise SyntaxError('invalid token')    


# unparse s-expr to string representation
def unparser(obj):
    s = ""
    if isinstance(obj,Atom):
        if istype(obj,ATOM_SYMBOL):
            s += '%s'%id2symbol(getvalue(obj))
        elif istype(obj,ATOM_STRING):
            s += '"%s"'%getvalue(obj)
        elif gettype(obj) in (ATOM_NUMBER, ATOM_FUNCTION, ATOM_FEXPR, ATOM_BUILTIN):
            s += '%s'%str(getvalue(obj))
        elif obj.type == ATOM_ENVIRONMENT:
            s += '%s'%environment2str(obj.value)
    elif isinstance(obj,Cons):
        if isnil(obj):
            return "()"
        s += "("
        while True:
            s += '%s '%unparser(car(obj))
            if isnil(cdr(obj)):
                break
            elif isinstance(cdr(obj),Atom):
                s += '. %s'%unparser(cdr(obj))
                break
            obj = cdr(obj)
        s = s.strip() + ")"
    return s


# unparse s-expr to s-expr string representation (for debugging)
def sexpr_unparser(obj):
    s = ""
    if obj is None:
        s += 'null'
    elif isinstance(obj,Atom):
        if obj.type == ATOM_SYMBOL:
            s += '<%s: %s>'%(obj.type,id2symbol(obj.value))
        elif obj.type == ATOM_STRING:
            s += '<%s: "%s">'%(obj.type,obj.value)
        elif obj.type in (ATOM_NUMBER, ATOM_FUNCTION, ATOM_FEXPR, ATOM_BUILTIN):
            s += '<%s: %s>'%(obj.type,str(obj.value))
        elif obj.type == ATOM_ENVIRONMENT:
            s += '<%s: %s>'%(obj.type,environment2str(obj.value))
    elif isinstance(obj,Cons):
        s += "(%s . %s)"%(sexpr_unparser(obj.car),sexpr_unparser(obj.cdr))
    return s


