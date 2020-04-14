
from .common import *


# ---------------- ENVIRONMENT ------------------

# return value of next args.car and rest (error if none)
def match_car(args):
    if isnil(args):
        raise Exception("Invalid number of arguments")            
    return car(args), cdr(args)

def match_optional(args):
    if isnil(args):
        return None, args
    return car(args), cdr(args)

# raise error if args is not empty
def match_check_left(args):
    if not isnil(args):
        raise Exception("Invalid number of arguments")    

# Parameter matching (with dotted cdr as rest)
def parameter_matching(params,args,env):
    if not isnil(params):
        if not isnil(car(params)): # if param.car is null ignore this
            symbol_id = getvalue(car(params))
            env.values[symbol_id],args = match_car(args)
        if isinstance(cdr(params),Cons): # if there are more parameters
            parameter_matching(cdr(params),args,env)
            return
        elif isinstance(cdr(params),Atom): # if cdr is atom
            symbol_id = getvalue(cdr(params))
            env.values[symbol_id] = nvl(args,Cons())
            return
        parameter_matching(None,args,env) # if no more parameters
    else:
        match_check_left(args) # check for unmached args left

class Environment:
    def __init__(self,params=Cons(),args=Cons(),parent=None):
        self.parent = parent
        self.values = {}
        parameter_matching(params,args,self)

# global environment
genv = Environment()

def find_symbol_id(symbol_id,env=genv):
    if symbol_id in env.values:
        return env.values[symbol_id]
    elif env.parent is not None:
        return find_symbol_id(symbol_id,env.parent)
    else:
        raise Exception("Symbol %s is not found!"%id2symbol(symbol_id))

def find_environment(symbol_id,env=genv):
    if symbol_id not in env.values and env.parent is not None:
        return find_environment(symbol_id,env.parent)
    return env

def environment2str(env):
    if env is None:
        return 'null'
    s = ''
    for k in env.values.keys():
        s += id2symbol(k) + ' '
    return 'env{'+s.strip()+'}'



