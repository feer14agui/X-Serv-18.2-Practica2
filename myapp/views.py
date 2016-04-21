from django.shortcuts import render
from models import URLS
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt

def Form(request):

    form = '<form action="" method="POST">' #indico que el formulario mandara un POST
    form += 'Acortar url: <input type="text" name="valor">'
    form += '<input type="submit" value="Enviar">'
    form += '<br>'
    lista = URLS.objects.all()

    if request.method == 'POST':
        if request.POST['valor'].find('http') == -1:
            url = 'http://' + request.POST['valor']
        else:
            url = request.POST['valor']
        for fila in lista:
            if fila.url == url:
                return HttpResponse('La url ' + url + ' ya esta acortada con ID ' + str(fila.id))

        db = URLS(url=url)
        db.save()
    lista = URLS.objects.all()
    salida = 'Hay estas urls acortadas:' + '<br>'
    for fila in lista:
        salida += '<li>' + fila.url + ', ID = ' + str(fila.id)
    return HttpResponse(form + '<br>' + salida)

def Buscar(request, recurso):
    try:
        db = URLS.objects.get(id=recurso)
        return HttpResponseRedirect(db.url)
    except URLS.DoesNotExist:
        return HttpResponse('Recurso /' + recurso + ' no se encuentra en la base de datos')
