from django.http import HttpResponseRedirect, Http404
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
        elif name == "letter":
            return HttpResponseRedirect('/letter_game')
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


def letter_game(request):
    return render(request, 'temp1/letter_game.html')


def letter_game_register(request):
    return render(request, 'temp1/letter_game_register.html')


@csrf_exempt
def letter_game_login(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        try:
            res = models.letter_user.objects.filter(username=name)[0]   # 返回的res对象是记录集合，而不是单个个体，但是记录不支持负索引
        except IndexError:
            raise Http404('找不到对应用户!')
        if res.password == password:
            return HttpResponseRedirect('/letter_game/play')
        else:
            raise Http404('用户名或密码错误!')
    elif request.method == 'GET':
        return render(request, 'temp1/letter_game_login.html', {'error_msg': ''})   # 默认get方法时返回的页面

# HttpResponseRedirect 页面跳转 render 页面渲染
# Http404 配合raise使用来实现404报错


def letter_game_play(request):
    return render(request, 'temp1/letter_game_play.html')

