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

def add_globals(env):
        "Add some Scheme standard procedures to an environment."
        import math, operator as op
        env.update(vars(math)) # sin, sqrt, ...
        env.update(
            {'add':op.add, 'sub':op.sub, 'gt':op.gt, 'lt':op.lt, 'equ':op.eq, \
             'not':op.not_, 'and':op.and_, 'or':op.or_})
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
        exps = []
        for exp in x:
            val = eval(exp, env)
            ###type detection
            if (type(val) == bool) and exps[0].__name__ not in ['not_', \
                                                                  'and_', \
                                                                  'or_']:
                raise SyntaxError('type detection error')
            if (type(val) == int) and (exps[0].__name__ not in ['add', \
                                                                  'sub', \
                                                                  'gt', \
                                                                  'lt', \
                                                                  'eq']):
                raise SyntaxError('type detection error')
            exps.append(val)
        proc = exps.pop(0)
        return proc(*exps)

################ atom, read_from, tokenize, parse, to_string, repl 
def atom(token):
    "Numbers become numbers; every other token is a symbol."
    try: 
        return int(token)
    except ValueError:
        if token == 'T':
            return True
        if token == 'F':
            return False
        #if token in ['True', 'False']
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

def repl(prompt='lisp_type_detection> '):
    "A prompt-read-eval-print loop."
    while True:
        exp = parse(raw_input(prompt))
        print exp
        val = eval(exp)
        if val is not None: 
            print val

if __name__=='__main__':
    repl()
