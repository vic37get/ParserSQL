from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import subprocess
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def index(request):
    dados = ''
    try:
        saida = subprocess.run(["python3", "main.py"], capture_output=True, text=True)
        if saida.returncode != 0:
            dados = saida.stderr.split('TypeError:')[1]
        else:
            dados = 'Exit success 0'
    except subprocess.CalledProcessError as e:
        pass

    context = {
        'saidaLog': dados
    }
    print(dados)
    template = loader.get_template('parserSQL/index.html')
    return HttpResponse(template.render(context, request))

@csrf_exempt
def save_text_file(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        with open('input.txt', 'w') as f:
            f.write(content)
        # Lógica para salvar o conteúdo em um arquivo ou banco de dados
        # ...
        return HttpResponse('Arquivo salvo com sucesso!')
    return HttpResponse('Erro: método não permitido.')
