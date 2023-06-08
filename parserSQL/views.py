from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import subprocess

# Create your views here.
def index(request):
    dados = ''
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        dados = uploaded_file.read().decode('utf-8')
    try:
        saida = subprocess.run(["python3", "main.py", 'input.txt'], capture_output=True, text=True)
        if saida.returncode != 0:
            dados = saida.stderr.split('TypeError:')[1]
        else:
            dados = 'Exit sucess 0'
    except subprocess.CalledProcessError as e:
        ...
    context = {
        'saidaLog': dados
    }
    template = loader.get_template('parserSQL/index.html')
    return HttpResponse(template.render(context, request))