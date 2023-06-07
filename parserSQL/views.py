from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    context = {
        
    }
    template = loader.get_template('parserSQL/index.html')
    return HttpResponse(template.render(context, request))
