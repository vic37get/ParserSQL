from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    dados = ''
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        dados = uploaded_file.read().decode('utf-8')
    print(dados)
    context = {
        'codigoSQL': dados
    }
    template = loader.get_template('parserSQL/index.html')
    return HttpResponse(template.render(context, request))
