"""
    ------------------------------
    Constants and common functions
    ------------------------------
"""


# ------ Symbol table ------

class Symbol_Table:
    def __init__(self):
        self.next_id = 0
        self.symbol2id_dict = {}
        self.id2symbol_dict = {}


# global symbol table 
symbol_table = Symbol_Table()

def symbol2id(value,new_id=None):
    symbol = value.upper()
    if new_id is not None and new_id>symbol_table.next_id:
        symbol_table.next_id = new_id
    if not symbol in symbol_table.symbol2id_dict:
        symbol_table.symbol2id_dict[symbol] = symbol_table.next_id
        symbol_table.id2symbol_dict[symbol_table.next_id] = symbol
        symbol_table.next_id += 1
    return symbol_table.symbol2id_dict[symbol]

def id2symbol(symbol_id):
    return symbol_table.id2symbol_dict[symbol_id]


# ------ Constants ------

ATOM_SYMBOL = 1
ATOM_STRING = 2
ATOM_NUMBER = 3
ATOM_FUNCTION = 4
ATOM_FEXPR = 5
ATOM_BUILTIN = 6
ATOM_ENVIRONMENT = 7

NEWLINES = "\n\r"
WHITESPACE = " \t"+NEWLINES

TOKEN_NUMBER = "NUMBER"
TOKEN_STRING = "STRING"
TOKEN_SYMBOL = "SYMBOL"
TOKEN_LBRACKET = "LBRACKET"
TOKEN_RBRACKET = "RBRACKET"
TOKEN_QUOTE = "QUOTE"
TOKEN_BACKQUOTE = "BACKQUOTE"
TOKEN_UNQUOTE = "UNQUOTE"
TOKEN_SPLICE_UNQUOTE = "SPLICE-UNQUOTE"
TOKEN_DOT = "DOT"




# ------ Atoms and Conses ------

class Atom:
    def __init__(self,type,value):
        self.type = type
        self.value = value

class Cons:
    def __init__(self,car=None,cdr=None):
        self.car = car
        self.cdr = cdr

def asym(value): return Atom(ATOM_SYMBOL,symbol2id(value))
def astr(value): return Atom(ATOM_STRING,value)
def anum(value): return Atom(ATOM_NUMBER,value)
def afunc(value): return Atom(ATOM_FUNCTION,value)
def afexpr(value): return Atom(ATOM_FEXPR,value)
def abuiltin(value): return Atom(ATOM_BUILTIN,value)
def aenv(env): return Atom(ATOM_ENVIRONMENT,env)

SYMBOLID_NULL               = symbol2id('NULL')
SYMBOLID_FALSE              = symbol2id('FALSE')
SYMBOLID_TRUE               = symbol2id('TRUE')

SYMBOLID_QUOTE              = symbol2id(TOKEN_QUOTE)
SYMBOLID_BACKQUOTE          = symbol2id(TOKEN_BACKQUOTE)
SYMBOLID_UNQUOTE            = symbol2id(TOKEN_UNQUOTE)
SYMBOLID_SPLICE_UNQUOTE     = symbol2id(TOKEN_SPLICE_UNQUOTE)

def afalse(): return Atom(ATOM_SYMBOL,SYMBOLID_FALSE)
def atrue(): return Atom(ATOM_SYMBOL,SYMBOLID_TRUE)



# ------ Utility Functions ------

# Car function
def car(c):
    if isinstance(c,Cons):
        return nvl(c.car)
    return Cons()    

# Cdr function
def cdr(c):
    if isinstance(c,Cons):
        return nvl(c.cdr)
    return Cons()    

# True if c is None or () 
def isnil(c):
    return c is None \
        or isinstance(c,Cons) and c.car is None and c.cdr is None \
        or isinstance(c,Atom) and c.type == ATOM_SYMBOL and c.value == SYMBOLID_NULL 

# True if false atom
def isfalse(c):
    return isinstance(c,Atom) and c.type == ATOM_SYMBOL and c.value == SYMBOLID_FALSE

# True if not false atom
def istrue(c):
    return not isfalse(c)

def isatom(c):
    return isnil(c) or isinstance(c,Atom)

def islist(c):    
    return isnil(c) or isinstance(c,Cons)

def istype(c,t):
    return isinstance(c,Atom) and c.type == t    

# EQ primitive
def is_eq(c1,c2):
    return isnil(c1) and isnil(c2) or isatom(c1) and isatom(c2) and gettype(c1)==gettype(c2) and getvalue(c1)==getvalue(c2)

# EQUAL primitive
def is_equal(c1,c2):
    if is_eq(c1,c2):
        return True
    return islist(c1) and islist(c2) and is_equal(car(c1),car(c2)) and is_equal(cdr(c1),cdr(c2))

# ---

def getvalue(c):
    if isinstance(c,Atom):
        return c.value
    return Cons()

def gettype(c):
    if isinstance(c,Atom):
        return c.type
    return Cons()

# If c is nil then value else c
def nvl(c,value=Cons()):
    if isnil(c):
        return value
    return c

# Returns last cons
def last(c):
    if isinstance(c,Cons) and not isnil(c):
        while isinstance(c,Cons) and c.cdr is not None:
            c = c.cdr
        return c
    return Cons()

# Append cons
def append(c1,c2):
    if isnil(c2):
        return c1
    cc = last(c1)
    if isnil(cc):
        return c2
    if isinstance(cc,Cons):
        cc.cdr = c2
    return c1



