from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from temp1 import models
from django.shortcuts import HttpResponse
import os


# Create your views here.


def index(request):
    return render(request, 'temp1/original.html')


def db_handle(request):
    # models.UserInfo.objects.create(username='andy',password='123456',age=33)  # Add data to a table
    # return HttpResponse('OK')
    target_name = ""
    res = models.nw.objects.filter(name=target_name)
    return render(request, 'temp1/original.html', {'li': res})

error_msg = ''


@csrf_exempt
def search(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name == "":
            error_msg = '不能为空，请重新输入！'
            return render(request, 'temp1/original.html', {'error_msg': error_msg})
        elif name == "----":
            return render(request, 'temp1/db_ans.html')
        elif name == "game":
            return render(request, 'temp1/game.html')
        elif 97 <= ord(name[0]) <= 122:
            res = models.words.objects.filter(word=name)
            return render(request, 'temp1/original.html', {'li': res})
        else:
            res = models.nw.objects.filter(name=name)
            return render(request, 'temp1/original.html', {'li': res})
    elif request.method == 'GET':
        return render(request, 'temp1/original.html', {'error_msg': ''})
