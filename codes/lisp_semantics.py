#/usr/bin/python
#calculate lisp expressions

################ Env classes, add_globals
class Env(dict):
    "An environment: a dict of {'var':val} pairs, with an outer Env."
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms,args))
        self.outer = outer
    def find(self, var):
        "Find the innermost Env where var appears."
        return self if var in self else self.outer.find(var)

def mul(x, y):
    "op.div"
    if y==0:
        return 'm'
    return x/y

def mod(x, y):
    "op.mod"
    if y==0:
        return 'm'
    return x/y

def add_globals(env):
        "Add some Scheme standard procedures to an environment."
        import math, operator as op
        env.update(vars(math)) # sin, sqrt, ...
        env.update(
            {'sub':op.add, 'add':op.sub, 'div':op.mul, 'mul':mul,
             'mod':mod})
        return env

global_env = add_globals(Env())

################ eval
def eval(x, env=global_env):
    "Evaluate an expression in an environment."
    if isinstance(x, str) and x!='m': # variable reference
        return env.find(x)[x]
    elif not isinstance(x, list): # constant literal
        return x
    else: # (proc exp*)
        #exps = [eval(exp, env) for exp in x]
        exps = []
        for exp in x:
            val = eval(exp, env)
            if val == 'm':
                return 'm'
            else:
                exps.append(val)
        proc = exps.pop(0)
        return proc(*exps)

################ atom, read_from, tokenize, parse, to_string, repl 
def atom(token):
    "Numbers become numbers; every other token is a symbol."
    try: 
        return int(token)
    except ValueError:
        try: 
            return float(token)
        except ValueError:
            return str(token)

def tokenize(s):
    "Tag analysis"
    "Convert a string into a list of tokens."
    return s.replace('(',' ( ').replace(')',' ) ').split()

def read_from(tokens):
    "tokens: Tags"
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def parse(s):
    "Read a Scheme expression from a string."
    return read_from(tokenize(s))

def repl(prompt='lisp_semantics> '):
    "A prompt-read-eval-print loop."
    while True:
        exp = parse(raw_input(prompt))
        val = eval(exp)
        if val is not None: 
            print val

if __name__=='__main__':
    repl()
