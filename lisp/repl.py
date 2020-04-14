
try:
    import readline
except:
    pass    
import traceback


from .common import *
from .parser import *
from .environment import *
from .eval_apply import *





# Load and execute file
def load(fname,env):
    o = open(fname)
    s = "("+o.read()+")"
    o.close()
    code = parser(tokenizer(s))
    r = Cons()
    while not isnil(code):
        x,code = match_car(code)
        r = eval(x,env)
    return r


# ---------------- REPL -------------------------

"""
repl_loop = True

# read with evaluation
def sexpr_read():
    s = ""
    l = []
    while True:
        r = input()
        if len(r)==0:
            break
        if r=='#quit' or r=='#q':
            global repl_loop
            repl_loop = False
            break
        if r=='#symtable':
            print("Symbol Table:")
            print(symbol_table.id2symbol_dict)
            break
        if r=='#genv':
            print("Global Environment:")
            for symbol_id in genv.values:
                print('[%d] %s = [%s] %s'%(symbol_id, id2symbol(symbol_id), gettype(genv.values[symbol_id]), unparser(genv.values[symbol_id])))
            break    
        if r=='#loop':
            print("Endless loop")
            i = 1
            while True: 
                print(i)
                i+=1
        s += " %s\n"%r
        l = tokenizer(s)        
        if bracket_count(l)==0 and len(l)>0:
            break
    return l

# Read-eval-parse-loop function
def repl(prompt = 'Ok', result='->'):
    global repl_loop
    repl_loop = True
    while repl_loop:
        try:
            print(prompt)
            l = sexpr_read()
            if len(l)>0:
                c = parser(l)
                r = eval(c) 
                s = unparser(r)
                print(result,s)
        except:
            traceback.print_exc()
"""

# -------------------------------------------



# Load and execute file
def load(fname,env=genv,env2=genv):
    o = open(fname)
    s = "("+o.read()+")"
    o.close()
    code = parser(tokenizer(s))
    return evmany(code,env,env2)


def execute_many(source,env=genv,env2=genv):
    s = "("+source+")"
    code = parser(tokenizer(s))
    r = evmany(code,env,env2)
    return r


def execute_request(source,env=genv,env2=genv):
    try:
        code = parser(tokenizer(source))
        r = eval(code,env,env2)
        result = unparser(r)
        return result,False
    except:
        return traceback.format_exc(), True


class Repl:
    def __init__(self, prompt="Ok", result="->"):
        self.prompt = prompt
        self.result = result
        self.loop = True
    # read with evaluation
    def sexpr_read(self):
        s = ""
        l = []
        while True:
            r = input()
            if len(r)==0:
                break
            if r=='#quit' or r=='#q':
                self.loop = False
                break
            if r=='#symtable':
                print("Symbol Table:")
                print(symbol_table.id2symbol_dict)
                break
            if r=='#genv':
                print("Global Environment:")
                for symbol_id in genv.values:
                    print('[%d] %s = [%s] %s'%(symbol_id, \
                        id2symbol(symbol_id), gettype(genv.values[symbol_id]), \
                        unparser(genv.values[symbol_id])))
                break    
            if r=='#loop':
                print("Endless loop")
                i = 1
                while True: 
                    print(i)
                    i+=1
            s += " %s\n"%r
            l = tokenizer(s)        
            if bracket_count(l)==0 and len(l)>0:
                break
        return l
    # Read-eval-parse-loop function
    def run(self):
        self.loop = True
        while self.loop:
            try:
                print(self.prompt)
                l = self.sexpr_read()
                if len(l)>0:
                    c = parser(l)
                    r = eval(c,genv,genv) 
                    s = unparser(r)
                    print(self.result,s)
            except:
                traceback.print_exc()


repl = Repl()















