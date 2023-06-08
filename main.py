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
    raise TypeError(f'Error: Token "{incoming}" não reconhecido, esperado "{expected}"')

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
        raise TypeError('Error: ";" esperado.')
token = nextToken()

def ID():
    global token
    if not re.match(re.compile(f'[a-z]([a-z0-9])*',flags=re.IGNORECASE),token):
        messageError(token, 'ID válido')
    token = nextToken()

    
def S():
    global token
    if token.upper() == 'CREATE':
        token = nextToken()
        create()
    elif token.upper() == 'USE':
        token = nextToken()
        ID()
        if token != ';':
            messageError(token, ';')
    elif token.upper() == 'INSERT':
        token = nextToken()
        if token.upper() != 'INTO':
            messageError(token,'INTO')
        token = nextToken()
        ID()
        idParenthesesNoType()
        if token.upper() != 'VALUES':
            messageError(token,'VALUES')
        token = nextToken()
        valueParentheses()
    elif token.upper() == 'SELECT':
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
    elif token.upper() == 'UPDATE':
        token = nextToken()
        ID()
        Set()
    elif token.upper() == 'DELETE':
        token = nextToken()
        fromID()
        where()
    elif token.upper() == 'TRUNCATE':
        token = nextToken()
        table()
    else:
        messageError(token, "CREATE, USE, INSERT, SELECT, UPDATE, DELETE, TRUNCATE")


def Set():
    global token

    if token.upper() != 'SET':
        messageError(token, 'SET')
    token = nextToken()
    compare()
    where()

def compare():
    global token

    ID()
    if token != "=":
        messageError(token, "=")
    token = nextToken()
    value()


def where():
    global token

    if token.upper() == 'WHERE':
        token = nextToken()
        compare()
    else:
        messageError(token, 'WHERE')

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
    if token.upper() == 'DATABASE':
        token = nextToken()
        ID()
        if token != ';':
            messageError(token,';')
    elif token.upper() == 'TABLE':
        table()
    else:
        messageError(token,'DATABASE ou TABLE')

def table():
    global token

    token = nextToken()
    ID()
    idParenthesesWithType()
    if token != ';':
        messageError(token,';')

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
    if token == ',':
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
    if token == ',':
        token = nextToken()
        ID()
        idNoParentheses()
    

def valueParentheses():
    global token
    if token == '(':
        token = nextToken()
        value()
        valueParentheses()
        if token != ')':
            messageError(token,')')
        else:
            token = nextToken()
    if token == ',':
        token = nextToken()
        value()
        valueParentheses()

S()