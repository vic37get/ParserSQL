import re
def getAllTokens():
    with open('input.txt','r') as f:
        tokens = f.read()\
            .replace(';',' ; ')\
            .replace('(',' ( ')\
            .replace(')',' ) ')\
            .replace('\n',' \n ')\
            .replace('>,','> ,')\
            .replace(',<',', <')
        tokens = re.sub(re.compile(f','),' , ',tokens)
    return re.findall(r'\S+', tokens)

def messageError(incoming,expected):
    raise TypeError(f'Token "{incoming}" não reconhecido, esperado "{expected}"')

tokens = getAllTokens()
def _nextToken():
    for i in tokens:
        yield i
gerador = _nextToken()
def nextToken():
    try:
        t = next(gerador)
        return t
    except StopIteration:
        raise TypeError('Erro: ";" esperado.')
token = nextToken()

def ID():
    global token
    if not re.match(re.compile(f'[a-z]([a-z0-9])*',flags=re.IGNORECASE),token):
        raise TypeError('Token não reconhecido')
    token = nextToken()

    
def S():
    global token
    if token.upper() == 'create'.upper():
        token = nextToken()
        I()
    elif token.upper() == 'truncate'.upper():
        token = nextToken()
        I()
    elif token.upper() == 'insert'.upper():
        token = nextToken()
        if token.upper() != 'into'.upper():
            messageError(token,'into')
        token = nextToken()
        ID()
        F_()
        if token.upper() != 'values'.upper():
            messageError(token,'values')
        token = nextToken()
        V()
    else:
        messageError(token,'create')

def I():
    global token
    if token.upper() == 'database'.upper():
        token = nextToken()
        ID()
        if token != ';':
            messageError(token,';')
    elif token.upper() == 'table'.upper():
        token = nextToken()
        ID()
        F()
        if token != ';':
            messageError(token,';')
    else:
        messageError(token,'database')

def F():
    global token
    if token.upper() == '(':
        token = nextToken()
        ID()
        ID()
        F()
        if token.upper() != ')':
            messageError(token,')')
        else:
            token = nextToken()
    if token.upper() == ',':
        token = nextToken()
        ID()
        ID()
        F()

def F_():
    global token
    if token.upper() == '(':
        token = nextToken()
        ID()
        F_()
        if token.upper() != ')':
            messageError(token,')')
        else:
            token = nextToken()
    if token.upper() == ',':
        token = nextToken()
        ID()
        F_()

def V():
    global token
    if token.upper() == '(':
        token = nextToken()
        token = nextToken()
        V()
        if token.upper() != ')':
            messageError(token,')')
        else:
            token = nextToken()
    if token.upper() == ',':
        token = nextToken()
        token = nextToken()
        V()


S()