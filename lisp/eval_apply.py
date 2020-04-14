
from .common import *
from .environment import *
from .parser import unparser

# ----------------- Lambda ------------------------

# lambda function 
class Lambda(object):
    def __init__(self, params, body, creator_env, dummy_env):
        self.params = params 
        self.body = body
        self.lexical_env = creator_env  # for lexical scope
        self.check_params()
    def check_params(self):
        p = self.params
        while not isnil(p):
            if islist(p) and ( isnil(car(p)) or istype(car(p),ATOM_SYMBOL) ): # for symbols and nils
                p = cdr(p)
            elif istype(p,ATOM_SYMBOL): # for dotted rest parameter
                break
            else:    
                raise Exception("Invalid parameter: not nil or symbol")
    def call(self, args, caller_env, dummy_env): 
        # env can be self.env for lexical or caller env for dynamic scope
        return evlast(self.body, Environment(self.params, args, self.lexical_env), caller_env)  


# Just to distinguish lambdas from specials
class Special(Lambda):
    pass


# ----------------- EVAL/APPLY ------------------

# evaluate many statements and return last evaluation
def evmany(args,env,env2):
    r = Cons()
    while not isnil(args):
        x,args = match_car(args)
        r = eval(x,env,env2)
    return r

# evaluate list and return list of evaluations
def evlis(args,env,env2):
    if isnil(args):
        return Cons()
    r = eval(car(args),env,env2)
    if isnil(cdr(args)):
        return Cons(r)
    return Cons(r,evlis(cdr(args),env,env2))

# evaluate list and return last evaluation
def evlast(args,env,env2):
    if isnil(args):
        return Cons()
    r = eval(car(args),env,env2)
    if isnil(cdr(args)):
        return r
    return evlast(cdr(args),env,env2)

# apply
def apply(op,args,env,env2):
    if gettype(op) == ATOM_BUILTIN:
        return getvalue(op)(args,env,env2)
    elif gettype(op) == ATOM_FUNCTION:
        lmbd = getvalue(op)
        return lmbd.call(evlis(args,env,env2),env,env2)
    elif gettype(op) == ATOM_FEXPR:
        lmbd = getvalue(op)
        return lmbd.call(args,env,env2)
    raise Exception("Cannot apply %s: not function or fexpr"%unparser(op))                    

# eval
def eval(e,env,env2):
    if isatom(e):
        if istype(e,ATOM_SYMBOL):
            return find_symbol_id(getvalue(e),env)
        return e
    elif islist(e):
        op,args = match_car(e)
        # if op is list evaluate it
        if islist(op):
            op = eval(op,env,env2)
        # if atom is symbol get it from environment
        if gettype(op)==ATOM_SYMBOL:    
            op = find_symbol_id(getvalue(op),env)
        # apply op on args in env
        return apply(op,args,env,env2)
    # otherwise
    raise Exception("Evaluation error of %s"%unparser(e))        






