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
        raise TypeError('ID inválido!')
    token = nextToken()

    
def S():
    global token
    if token.upper() == 'create'.upper():
        token = nextToken()
        create()
    elif token.upper() == 'use'.upper():
        token = nextToken()
        ID()
        if token != ';':
            messageError(token, ';')
    elif token.upper() == 'insert'.upper():
        token = nextToken()
        if token.upper() != 'into'.upper():
            messageError(token,'into')
        token = nextToken()
        ID()
        idParenthesesNoType()
        if token.upper() != 'values'.upper():
            messageError(token,'values')
        token = nextToken()
        valueParentheses()
    elif token.upper() == 'select'.upper():
        token = nextToken()
        if token == '*':
            token = nextToken()
            fromID()
        else:
            ID()
            idNoParentheses()
            fromID()
        where()
        orderBy()
        if token != ';':
            messageError(token, ';')
    elif token.upper() == 'truncate'.upper():
        token = nextToken()
        create()

def where():
    global token

    if token.upper() == 'WHERE':
        token = nextToken()
        ID()
        
        if token != "=":
            messageError(token, "=")
        token = nextToken()
        value()

def value():
    global token
    if re.search(r"^((\"[^\"]*\")|(\'[^']*\')|([0-9]+))$", token):
        token = nextToken()
    else:
        messageError(token, 'valor')


def orderBy():
    global token
    if token.upper() == 'ORDER':
        token = nextToken()
        if token.upper() != 'BY':
            messageError(token, "BY")
        else:
            token = nextToken()
            ID()
            idNoParentheses()
            if token.upper() in ['DESC', 'ASC']:
                token = nextToken()

def fromID():
    global token
    if token.upper() != "FROM":
        messageError(token, 'FROM')
    else:
        token = nextToken()
        ID()

def create():
    global token
    if token.upper() == 'database'.upper():
        token = nextToken()
        ID()
        if token != ';':
            messageError(token,';')
    elif token.upper() == 'table'.upper():
        token = nextToken()
        ID()
        idParenthesesWithType()
        if token != ';':
            messageError(token,';')
    else:
        messageError(token,'DATABASE ou TABLE')

def idParenthesesWithType():
    global token
    if token == '(':
        token = nextToken()
        ID()
        ID()
        idParenthesesWithType()
        if token != ')':
            messageError(token,')')
        else:
            token = nextToken()
    if token.upper() == ',':
        token = nextToken()
        ID()
        ID()
        idParenthesesWithType()

def idParenthesesNoType():
    global token
    if token == '(':
        token = nextToken()
        ID()
        idParenthesesNoType()
        if token != ')':
            messageError(token,')')
        else:
            token = nextToken()
    if token == ',':
        token = nextToken()
        ID()
        idParenthesesNoType()

def idNoParentheses():
    global token
    if token.upper() == ',':
        token = nextToken()
        ID()
        idNoParentheses()
    

def valueParentheses():
    global token
    if token.upper() == '(':
        token = nextToken()
        value()
        valueParentheses()
        if token.upper() != ')':
            messageError(token,')')
        else:
            token = nextToken()
    if token.upper() == ',':
        token = nextToken()
        value()
        valueParentheses()

if __name__ == "__main__":
    S()