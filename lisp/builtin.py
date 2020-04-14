
from .parser import *
from .environment import *
from .eval_apply import *
from .repl import *

# ---

def builtin_test_report(args,env,env2):
    total = 0
    passed = 0
    failed = 0
    errors = 0
    while not isnil(args):
        total = total + 1
        test,args = match_car(args)
        print("%d) Testing %s ... "%(total,unparser(test)),end='')
        try:
            if istrue(eval(test,env,env2)):
                print("Passed")
                passed = passed + 1
            else:
                print("Failed")        
                failed = failed + 1
        except:
            print("Error")        
            errors = errors + 1
            traceback.print_exc()
    print("Total %d -> passed: %d, failed: %d, errors: %d."%(total,passed,failed,errors))
    if total==passed:
        return atrue()
    return afalse()

# ----

def builtin_quote(args,env,env2):
    value,args = match_car(args)
    match_check_left(args)
    return value

# ignore until unquote or splice_unquote
def bq_eval(c,env,env2):
    if isatom(c) or isnil(c):
        return c
    else: # list
        if istype(car(c),ATOM_SYMBOL) and getvalue(car(c))==SYMBOLID_UNQUOTE:
            return eval(car(cdr(c)),env,env2)
        else:
            result = Cons()
            while not isnil(c):
                cc = car(c)
                if istype(car(cc),ATOM_SYMBOL) and getvalue(car(cc))==SYMBOLID_SPLICE_UNQUOTE:
                    result = append(result, eval(car(cdr(cc)),env,env2) )
                else:
                    result = append(result, Cons(bq_eval(car(c),env,env2)) )
                c = cdr(c)
            return result
        

def builtin_backquote(args,env,env2):
    x,args = match_car(args)
    match_check_left(args)
    return bq_eval(x,env,env2)

def builtin_unquote(args,env,env2):
    raise Exception("Invalid use of unquote")

def builtin_splice_unquote(args,env,env2):
    raise Exception("Invalid use of splice-unquote")

# ----

def builtin_parse(args,env,env2):
    x,args = match_car(args)
    match_check_left(args)
    return parser(tokenizer(getvalue(x)))

def builtin_unparse(args,env,env2):
    x,args = match_car(args)
    match_check_left(args)
    return astr(unparser(eval(x,env,env2)))

# ----

def builtin_set_excl(args,env,env2):
    var,args = match_car(args)
    value,args = match_car(args)
    match_check_left(args)
    value = eval(value,env,env2)
    v = getvalue(var)
    e = find_environment(v,env)
    e.values[v] = value
    return value

def builtin_define(args,env,env2):
    var,args = match_car(args)
    if istype(var,ATOM_SYMBOL):
        value,args = match_car(args)
        match_check_left(args)
        value = eval(value,env,env2)
        v = getvalue(var)
        env.values[v] = value
        return value
    elif islist(var):
        var2,params = match_car(var)
        v = getvalue(var2)
        body = args
        f = afunc(Lambda(params,body,env,env2))
        env.values[v] = f
        return f
    else:
        raise Exception("Invalid parameter type for variable")

def builtin_fexpr(args,env,env2):
    var,args = match_car(args)
    if islist(var):
        var2,params = match_car(var)
        v = getvalue(var2)
        body = args
        f = afexpr(Special(params,body,env,env2))
        env.values[v] = f
        return f
    else:
        raise Exception("Invalid parameter type for variable")


# ----

def builtin_lambda(args,env,env2):
    params,body = match_car(args)
    return afunc(Lambda(params,body,env,env2))

def builtin_special(args,env,env2):
    params,body = match_car(args)
    return afexpr(Special(params,body,env,env2))

def builtin_source(args,env,env2):
    name,args = match_car(args)
    match_check_left(args)
    lmbd = eval(name,env,env2)
    lmbd = getvalue(eval(name,env,env2))
    if isinstance(lmbd,Lambda):
        return Cons(lmbd.params,Cons(car(lmbd.body)))
    raise Exception("Invalid parameter: not lambda or special")

# ----

def builtin_car(args,env,env2):
    value,args = match_car(args)
    match_check_left(args)
    return car(eval(value,env,env2))

def builtin_cdr(args,env,env2):
    value,args = match_car(args)
    match_check_left(args)
    return cdr(eval(value,env,env2))

def builtin_cons(args,env,env2):
    x,args = match_car(args)
    y,args = match_car(args)
    match_check_left(args)
    return Cons(eval(x,env,env2),eval(y,env,env2))

def builtin_list(args,env,env2):
    return evlis(args,env,env2)

# ----

def builtin_is_null(args,env,env2):
    x,args = match_car(args)
    match_check_left(args)
    if isnil(eval(x,env,env2)):
        return atrue()
    return afalse()    

def builtin_is_atom(args,env,env2):
    x,args = match_car(args)
    match_check_left(args)
    if isatom(eval(x,env,env2)):
        return atrue()
    return afalse()  

def builtin_is_list(args,env,env2):
    x,args = match_car(args)
    match_check_left(args)
    if islist(eval(x,env,env2)):
        return atrue()
    return afalse()  

def builtin_is_false(args,env,env2):
    while not isnil(args):
        if not isfalse(eval(car(args),env,env2)):
            return afalse()
        args = cdr(args)
    return atrue()

def builtin_is_true(args,env,env2):
    while not isnil(args):
        if not istrue(eval(car(args),env,env2)):
            return afalse()
        args = cdr(args)
    return atrue()

# --

def builtin_is_symbol(args,env,env2):
    x,args = match_car(args)
    match_check_left(args)
    if istype(eval(x,env,env2),ATOM_SYMBOL):
        return atrue()
    return afalse()  

def builtin_is_number(args,env,env2):
    x,args = match_car(args)
    match_check_left(args)
    if istype(eval(x,env,env2),ATOM_NUMBER):
        return atrue()
    return afalse()  

def builtin_is_string(args,env,env2):
    x,args = match_car(args)
    match_check_left(args)
    if istype(eval(x,env,env2),ATOM_STRING):
        return atrue()
    return afalse()  

def builtin_is_function(args,env,env2):
    x,args = match_car(args)
    match_check_left(args)
    if istype(eval(x,env,env2),ATOM_FUNCTION):
        return atrue()
    return afalse()  

def builtin_is_fexpr(args,env,env2):
    x,args = match_car(args)
    match_check_left(args)
    if istype(eval(x,env,env2),ATOM_FEXPR):
        return atrue()
    return afalse()  

def builtin_is_builtin(args,env,env2):
    x,args = match_car(args)
    match_check_left(args)
    if istype(eval(x,env,env2),ATOM_BUILTIN):
        return atrue()
    return afalse()  

def builtin_is_environment(args,env,env2):
    x,args = match_car(args)
    match_check_left(args)
    if istype(eval(x,env,env2),ATOM_ENVIRONMENT):
        return atrue()
    return afalse()  

# --

def builtin_or(args,env,env2):
    while not isnil(args):
        if istrue(eval(car(args),env,env2)):
            return atrue()
        args = cdr(args)
    return afalse()

def builtin_not(args,env,env2):
    x,args = match_car(args)
    match_check_left(args)    
    if istrue(x):
        return afalse()
    return atrue()

# ----

def builtin_cmp_eq(args,env,env2):
    i = 0
    l = None
    while not isnil(args):
        x = getvalue(eval(car(args),env,env2))
        args = cdr(args)
        if i>0 and not l==x:
            return afalse()
        l = x
        i += 1
    return atrue()

def builtin_cmp_neq(args,env,env2):
    i = 0
    l = []
    while not isnil(args):
        x = getvalue(eval(car(args),env,env2))
        args = cdr(args)
        if i>0 and x in l:
            return afalse()
        l.append(x)
        i += 1
    return atrue()

def builtin_cmp_gt(args,env,env2):
    i = 0
    l = None
    while not isnil(args):
        x = getvalue(eval(car(args),env,env2))
        args = cdr(args)
        if i>0 and not l>x:
            return afalse()
        l = x
        i += 1
    return atrue()

def builtin_cmp_ge(args,env,env2):
    i = 0
    l = None
    while not isnil(args):
        x = getvalue(eval(car(args),env,env2))
        args = cdr(args)
        if i>0 and not l>=x:
            return afalse()
        l = x
        i += 1
    return atrue()

def builtin_cmp_lt(args,env,env2):
    i = 0
    l = None
    while not isnil(args):
        x = getvalue(eval(car(args),env,env2))
        args = cdr(args)
        if i>0 and not l<x:
            return afalse()
        l = x
        i += 1
    return atrue()

def builtin_cmp_le(args,env,env2):
    i = 0
    l = None
    while not isnil(args):
        x = getvalue(eval(car(args),env,env2))
        args = cdr(args)
        if i>0 and not l<=x:
            return afalse()
        l = x
        i += 1
    return atrue()

# ----

def builtin_plus(args,env,env2):
    r = 0
    while not isnil(args):
        r += getvalue(eval(car(args),env,env2))
        args = cdr(args)
    return anum(r)

def builtin_minus(args,env,env2):
    x,args = match_car(args)
    if isnil(args):
        return anum(-getvalue(eval(x,env,env2)))
    r = getvalue(eval(x,env,env2))
    while not isnil(args):
        r -= getvalue(eval(car(args),env,env2))
        args = cdr(args)
    return anum(r)

def builtin_multiply(args,env,env2):
    r = 1
    while not isnil(args):
        r *= getvalue(eval(car(args),env,env2))
        args = cdr(args)
    return anum(r)
    
def builtin_divide(args,env,env2):
    x,args = match_car(args)
    if isnil(args):
        return anum(1/getvalue(eval(x.env,env2)))
    r = getvalue(eval(x,env,env2))
    while not isnil(args):
        r /= getvalue(eval(car(args),env,env2))
        args = cdr(args)
    return anum(r)
    
# ----

def builtin_eval(args,env,env2):
    x,args = match_car(args)
    e,args = match_optional(args)
    match_check_left(args)
    if e is not None:
        e = getvalue(eval(e,env,env2,env2))
    else:
        e = env
    return eval(eval(x,env,env2),e,env2)

def builtin_apply(args,env,env2):
    f,args = match_car(args)
    x,args = match_car(args)
    e,args = match_optional(args)
    match_check_left(args)
    a = eval(x,env,env2)
    if e is not None:
        e = getvalue(eval(e,env,env2))
    else:
        e = env
    if not islist(a):
        raise Exception("Apply argument %s is not list"%unparser(a))
    return apply(eval(f,env,env2),a,e,env2)

def builtin_deval(args,env,env2):
    x,args = match_car(args)
    match_check_left(args)
    return eval(eval(x,env,env2),env2,env2)


# ----

def builtin_begin(args,env,env2):
    return evlast(args,env,env2)


def builtin_let(args,env,env2):
    varlist,body = match_car(args)
    e = Environment(parent=env)
    while not isnil(varlist):
        a = car(varlist)
        if isinstance(a,Atom) and gettype(a)==ATOM_SYMBOL and not isnil(a):
            e.values[a.value]=Cons()
        elif isinstance(a,Cons):
            varname,a = match_car(a)
            varvalue,a = match_car(a)
            match_check_left(a)
            if isinstance(varname,Atom) and istype(varname,ATOM_SYMBOL) and not isnil(varname):
                e.values[getvalue(varname)]=eval(varvalue,e,env2)
            else:
                raise Exception("Invalid variable %s in LET assigment"%unparser(varname))                
        else:        
            raise Exception("Wrong parameters in LET assigment")                
        varlist = cdr(varlist)
    return evlast(body,e,env2)

def builtin_cond(args,env,env2):
    while not isnil(args) and not isnil(car(args)):
        a = car(args)
        if islist(a):
            condition = eval(car(a),env,env2)
            if istrue(condition):
                eresult = evlast(cdr(a),env,env2)
                return eresult
        else:
            raise Exception("Cond argument %s is not list"%unparser(a))
        args = cdr(args)
    return Cons()

def builtin_while(args,env,env2):
    cond,args = match_car(args)
    r = Cons()
    while istrue(eval(cond,env,env2)):
        r = evlast(args,env,env2)
    return r

def builtin_match(args,env,env2):
    p_params,args = match_car(args)
    p_args,body = match_car(args)
    p_params = eval(p_params,env,env2)
    p_args = eval(p_args,env,env2)
    e = Environment(parent=env)
    parameter_matching(p_params,p_args,e)
    return evlast(body,e,env2)

# ---

def builtin_display(args,env,env2):
    value = Cons()
    while not isnil(args):
        value,args = match_car(args)
        value = eval(value,env,env2)
        if (istype(value,ATOM_STRING)):
            print(getvalue(value),end='')
        else:
            print(unparser(value),end='')
    return value

def builtin_newline(args,env,env2):
    match_check_left(args)
    print()
    return Cons()

def builtin_read(args,env,env2):
    match_check_left(args)
    l = repl.sexpr_read()
    c = parser(l)
    return c

# ---

def builtin_env_lexical(args,env,env2):
    match_check_left(args)
    return aenv(env)

def builtin_env_dynamic(args,env,env2):
    match_check_left(args)
    return aenv(env2)

def builtin_env_root(args,env,env2):
    match_check_left(args)
    while env.parent is not None:
        env = env.parent
    return aenv(env)

def builtin_env_parent(args,env,env2):
    match_check_left(args)
    if env.parent is not None:
        return aenv(env.parent)
    return Cons()

def builtin_env_keys(args,env,env2):
    p_env,args = match_car(args)
    match_check_left(args)
    e = eval(p_env,env,env2)
    r = Cons()
    if istype(e,ATOM_ENVIRONMENT):
        for key_id in getvalue(e).values.keys():
            r = append(r,Cons(asym(id2symbol(key_id))))
    else:
        raise Exception("Environment expected!")
    return r

def builtin_env_find(args,env,env2):
    p_env,args = match_car(args)
    p_var,args = match_car(args)
    match_check_left(args)
    e = eval(p_env,env,env2)
    if not istype(e,ATOM_ENVIRONMENT):
        raise Exception("Environment expected!")
    if not isatom(p_var):
        p_var = eval(p_var,env,env2)
    if not istype(p_var,ATOM_SYMBOL):
        raise Exception("Invalid parameter: variable symbol expected!")
    v_id = getvalue(p_var)
    e = getvalue(e)
    while e is not None:
        if v_id in e.values:
            return aenv(e)
        e = e.parent
    return Cons()

def builtin_env_get(args,env,env2):
    p_env,args = match_car(args)
    p_var,args = match_car(args)
    match_check_left(args)
    e = eval(p_env,env,env2)
    if not istype(e,ATOM_ENVIRONMENT):
        raise Exception("Environment expected!")
    if not isatom(p_var):
        p_var = eval(p_var,env,env2)
    if not istype(p_var,ATOM_SYMBOL):
        raise Exception("Invalid parameter: variable symbol expected!")
    v_id = getvalue(p_var)
    e = getvalue(e)
    if v_id in e.values:
        return e.values[v_id]
    return Cons()    
    

def builtin_env_set(args,env,env2):
    p_env,args = match_car(args)
    p_var,args = match_car(args)
    p_value,args = match_car(args)
    match_check_left(args)
    e = eval(p_env,env,env2)
    if not istype(e,ATOM_ENVIRONMENT):
        raise Exception("Environment expected!")
    if not isatom(p_var):
        p_var = eval(p_var,env,env2)
    if not istype(p_var,ATOM_SYMBOL):
        raise Exception("Invalid parameter: variable symbol expected!")
    v = eval(p_value,env,env2)
    v_id = getvalue(p_var)
    e = getvalue(e)
    e.values[v_id] = v
    return v

def builtin_env_del(args,env,env2):
    p_env,args = match_car(args)
    p_var,args = match_car(args)
    match_check_left(args)
    e = eval(p_env,env,env2)
    if not istype(e,ATOM_ENVIRONMENT):
        raise Exception("Environment expected!")
    if not isatom(p_var):
        p_var = eval(p_var,env,env2)
    if not istype(p_var,ATOM_SYMBOL):
        raise Exception("Invalid parameter: variable symbol expected!")
    v_id = getvalue(p_var)
    e = getvalue(e)
    if v_id in e.values:
        del e.values[v_id]
    return aenv(e)

def builtin_env_new(args,env,env2):
    p_parent,args = match_car(args)
    match_check_left(args)
    e = eval(p_parent,env,env2)
    if not istype(e,ATOM_ENVIRONMENT):
        raise Exception("Environment expected!")
    return aenv(Environment(parent=getvalue(e)))

# ---

def builtin_load(args,env,env2):
    filename,args = match_car(args)
    match_check_left(args)
    fname = getvalue(eval(filename,env,env2))
    return load(fname,env,env2)

# ---

def builtin_eq(args,env,env2):
    x,args = match_car(args)
    y,args = match_car(args)
    match_check_left(args)
    if is_eq(eval(x,env,env2),eval(y,env,env2)):
        return atrue()
    return afalse()

def builtin_equal(args,env,env2):
    x,args = match_car(args)
    y,args = match_car(args)
    match_check_left(args)
    if is_equal(eval(x,env,env2),eval(y,env,env2)):
        return atrue()
    return afalse()


# ---

def builtin_quit(args,env,env2):
    match_check_left(args)
    repl.loop = False
    return Cons()

# ---- Global Enviroment Values ----

genv.values.update({

    # -- Constants --
    symbol2id('null'): Cons(),
    symbol2id('false'): afalse(),
    symbol2id('true'): atrue(),
    symbol2id('#t'): atrue(),
    symbol2id('#f'): afalse(),
    symbol2id('dot'): asym('dot'),
    symbol2id('.'): asym('dot'),


    # -- Builtins --

    # ---
    symbol2id('test-report'): abuiltin(builtin_test_report),
    # ---
    SYMBOLID_QUOTE: abuiltin(builtin_quote),    
    SYMBOLID_BACKQUOTE: abuiltin(builtin_backquote),
    SYMBOLID_UNQUOTE: abuiltin(builtin_unquote),
    SYMBOLID_SPLICE_UNQUOTE:  abuiltin(builtin_splice_unquote),
    # ---
    symbol2id('parse'): abuiltin(builtin_parse),
    symbol2id('unparse'): abuiltin(builtin_unparse),
    # --
    symbol2id('set!'): abuiltin( builtin_set_excl),
    symbol2id('define'): abuiltin( builtin_define),
    symbol2id('fexpr'): abuiltin( builtin_fexpr),
    # --
    symbol2id('lambda'): abuiltin(builtin_lambda),
    symbol2id('special'): abuiltin(builtin_special),
    symbol2id('source'): abuiltin(builtin_source),
    # --
    symbol2id('car'): abuiltin(builtin_car),
    symbol2id('cdr'): abuiltin(builtin_cdr),
    symbol2id('cons'): abuiltin(builtin_cons),
    symbol2id('list'): abuiltin(builtin_list),
    # --
    symbol2id('null?'): abuiltin(builtin_is_null),
    symbol2id('atom?'): abuiltin(builtin_is_atom),
    symbol2id('list?'): abuiltin(builtin_is_list),
    symbol2id('false?'): abuiltin(builtin_is_false),
    symbol2id('true?'): abuiltin(builtin_is_true),
    # --
    symbol2id('symbol?'): abuiltin(builtin_is_symbol), 
    symbol2id('number?'): abuiltin(builtin_is_number), 
    symbol2id('string?'): abuiltin(builtin_is_string), 
    symbol2id('function?'): abuiltin(builtin_is_function), 
    symbol2id('fexpr?'): abuiltin(builtin_is_fexpr), 
    symbol2id('builtin?'): abuiltin(builtin_is_builtin), 
    symbol2id('environment?'): abuiltin(builtin_is_environment),
    # --
    symbol2id('and'): abuiltin(builtin_is_true), # same as "true?" function
    symbol2id('or'): abuiltin(builtin_or),
    symbol2id('not'): abuiltin(builtin_not),
    # ---
    symbol2id('='): abuiltin(builtin_cmp_eq),
    symbol2id('!='): abuiltin(builtin_cmp_neq),
    symbol2id('>'): abuiltin(builtin_cmp_gt),
    symbol2id('>='): abuiltin(builtin_cmp_ge),
    symbol2id('<'): abuiltin(builtin_cmp_lt),
    symbol2id('<='): abuiltin(builtin_cmp_le),
    # --
    symbol2id('+'): abuiltin(builtin_plus),
    symbol2id('-'): abuiltin(builtin_minus),
    symbol2id('*'): abuiltin(builtin_multiply),
    symbol2id('/'): abuiltin(builtin_divide),
    # --
    symbol2id('eval'): abuiltin(builtin_eval),
    symbol2id('apply'): abuiltin(builtin_apply),
    symbol2id('deval'): abuiltin(builtin_deval),
    # --
    symbol2id('begin'): abuiltin(builtin_begin),
    symbol2id('let'): abuiltin(builtin_let),
    symbol2id('cond'): abuiltin(builtin_cond),
    symbol2id('while'): abuiltin(builtin_while),
    symbol2id('match'): abuiltin(builtin_match),
    # ---
    symbol2id('display'): abuiltin(builtin_display),
    symbol2id('newline'): abuiltin(builtin_newline),
    symbol2id('read'): abuiltin(builtin_read),
    # ---
    symbol2id('env-lexical'): abuiltin(builtin_env_lexical),
    symbol2id('env-dynamic'): abuiltin(builtin_env_dynamic),
    symbol2id('env-root'): abuiltin(builtin_env_root),
    symbol2id('env-parent'): abuiltin(builtin_env_parent),
    symbol2id('env-keys'): abuiltin(builtin_env_keys),
    symbol2id('env-find'): abuiltin(builtin_env_find),
    symbol2id('env-get'): abuiltin(builtin_env_get),
    symbol2id('env-set'): abuiltin(builtin_env_set),
    symbol2id('env-del'): abuiltin(builtin_env_del),
    symbol2id('env-new'): abuiltin(builtin_env_new),
    # ---
    symbol2id('load'): abuiltin(builtin_load),
    # ---
    symbol2id('eq?'): abuiltin(builtin_eq),
    symbol2id('equal?'): abuiltin(builtin_equal),
    # ---
    symbol2id('quit'): abuiltin(builtin_quit)
    # ---
    })


execute_many('''
    (define env env-lexical)
    (define x 10)
    (define y 20)
    (define z 30)

''')




