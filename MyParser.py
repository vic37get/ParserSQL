import re


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
        )
        tokens = tokens + "$"
        tokens = re.sub(re.compile(f","), " , ", tokens)
    return re.findall(r"\S+", tokens)


def messageError(incoming, expected):
    raise TypeError(f'Error: Token "{incoming}" não reconhecido, esperado "{expected}"')


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
    global token
    token = token.lower()
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
            messageError(token, "(table|database)")
    if token == "insert":
        token = nextToken()
        INSERT()
    if token == "select":
        token = nextToken()
        SELECT()
        WHERE()
        ORDER()
    if token == "update":
        token = nextToken()
        ID()
        equality("set")
        ID()
        equality("=")
        VALOR()
        FROM()
    if token == "delete":
        token = nextToken()
        FROM()
        WHERE()
    if token == "truncate":
        token = nextToken()
        equality("table")
        ID()
    if token == "use":
        ID()
    equality(";")


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
    if not re.match(re.compile(f"[a-z]([a-z0-9])*", flags=re.IGNORECASE), token):
        messageError(token, "ID válido")
    token = nextToken()


def VALOR():
    global token
    if not re.match(
        re.compile(f"([a-z]([a-z0-9])*|[0-9]*)", flags=re.IGNORECASE), token
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
