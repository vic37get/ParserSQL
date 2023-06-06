def nextToken(palavra):
    token = palavra[0]
    palavra.pop(0)
    return palavra, token

def words(fileobj):
    for line in fileobj:
        for word in line.split():
            yield word


def main():
    with open("teste.txt") as wordfile:
        palavra = wordfile.next()
        print(palavra)

main()
    
