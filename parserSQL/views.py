from django.http import HttpResponse
from django.template import loader
import subprocess
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    dados = ""
    dados = realizaParser()
    context = {"saidaLog": dados}
    template = loader.get_template("parserSQL/index.html")
    return HttpResponse(template.render(context, request))


@csrf_exempt
def save_text_file(request):
    if request.method == "POST":
        content = request.POST.get("content")
        with open("input.txt", "w") as f:
            f.write(content)
        dados = realizaParser()
        return HttpResponse(dados)
    return HttpResponse("Erro: método não permitido.")


def realizaParser():
    try:
        saida = subprocess.run(
            ["python3", "MyParser.py"], capture_output=True, text=True
        )
        if saida.returncode != 0:
            dados = saida.stderr.split("TypeError:")[1]
        else:
            dados = "Exit success 0"
    except subprocess.CalledProcessError as e:
        pass
    return dados


def splitMantendoSeparador(string, separador):
    string_split = []
    string_aux = ""
    for caractere in string:
        string_aux += caractere
        if caractere == separador:
            string_split.append(string_aux)
            string_aux = ""
    string_split.append(string_aux)
    return string_split
