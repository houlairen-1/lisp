#/usr/bin/python
#convert lisp to c in format

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

def lisp2c(l):
    "format: lisp to c"
    print '{0}('.format(l[0]),
    if isinstance(l[1], list):
        lisp2c(l[1])
    else:
        print '{0}'.format(l[1]),
    print ',',
    if isinstance(l[2], list):
        lisp2c(l[2])
    else:
        print '{0}'.format(l[2]),
    print ')',
    

def repl(prompt='lisp_grammar> '):
    "A prompt-read-eval-print loop."
    while True:
        exp = parse(raw_input(prompt))
        #        print 'c format = ',
        lisp2c(exp)
        print ''

if __name__=='__main__':
    repl()
