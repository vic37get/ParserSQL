import re

linhas = 1


def getAllTokens():
    with open("input.txt", "r") as f:
        tokens = (
            f.read()
            .replace(";", " ; ")
            .replace("(", " ( ")
            .replace(")", " ) ")
            .replace("\n", " \n ")
            .replace(">,", "> ,")
            .replace(",<", ", <")
        ).lower()
        tokens = tokens + " $"
        tokens = re.sub(re.compile(f","), " , ", tokens)
    return re.findall(r"\S+", tokens)


def messageError(incoming, expected):
    if incoming == "$":
        raise TypeError(
        f'Error: Erro de token, esperado "{expected}" no comando:{linhas}')
    else:    
        raise TypeError(
            f'Error: Token "{incoming}" não reconhecido, esperado "{expected}" no comando:{linhas}')


tokens = getAllTokens()


def _nextToken():
    for i in tokens:
        yield i


gerador = _nextToken()


def nextToken():
    t = next(gerador)
    return t


token = nextToken()


def equality(expected):
    global token
    if token != expected:
        messageError(token, expected)
    token = nextToken()


def S():
    global token, linhas
    if token == "create":
        token = nextToken()
        if token == "table":
            token = nextToken()
            ID()
            equality("(")
            ID()
            TIPO()
            PT()
            equality(")")

        elif token == "database":
            token = nextToken()
            ID()
        else:
            messageError(token, "TABLE ou DATABASE")
    elif token == "insert":
        token = nextToken()
        INSERT()
    elif token == "select":
        token = nextToken()
        SELECT()
        WHERE()
        ORDER()
    elif token == "update":
        token = nextToken()
        ID()
        equality("set")
        ID()
        equality("=")
        VALOR()
        WHERE()
    elif token == "delete":
        token = nextToken()
        FROM()
        WHERE()
    elif token == "truncate":
        token = nextToken()
        equality("table")
        ID()
    elif token == "use":
        token = nextToken()
        ID()
    else:
        messageError(
            token, 'CREATE, USE, INSERT, SELECT, UPDATE, DELETE ou TRUNCATE')
    equality(";")
    linhas += 1


def TIPO():
    ID()


def INSERT():
    equality("into")
    ID()
    equality("(")
    ID()
    P()
    equality(")")
    equality("values")
    equality("(")
    VALOR()
    VALOR_VARIOS()
    equality(")")


def SELECT():
    global token
    if token == "*":
        token = nextToken()
    else:
        ID()
        P()
    FROM()


def WHERE():
    global token
    if token == "where":
        token = nextToken()
        ID()
        equality("=")
        VALOR()


def ORDER():
    global token
    if token == "order":
        token = nextToken()
        equality("by")
        ID()


def FROM():
    global token
    if token == "from":
        token = nextToken()
        ID()
    else:
        messageError(token, "from")


def ID():
    global token
    if not re.match(re.compile(f"^[a-z]([a-z0-9])*$", flags=re.IGNORECASE), token):
        messageError(token, "ID válido")
    token = nextToken()


def VALOR():
    global token
    if not re.match(
        re.compile(f"^([a-z]([a-z0-9])*|[0-9]*)$", flags=re.IGNORECASE), token
    ):
        messageError(token, "Valor válido")
    token = nextToken()


def VALOR_VARIOS():
    global token
    if token == ",":
        token = nextToken()
        VALOR()
        VALOR_VARIOS()


def PT():
    global token
    if token == ",":
        token = nextToken()
        ID()
        TIPO()
        PT()


def P():
    global token
    if token == ",":
        token = nextToken()
        ID()
        P()


def main():
    while token != "$":
        S()


main()