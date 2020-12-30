from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
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


@csrf_exempt
def letter_game_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        qq = request.POST.get('QQ')
        if username and password and phone and qq:
            if models.letter_user.objects.filter(username=username):
                messages.info(request, '用户已注册请勿重复注册!')
                return render(request, 'temp1/letter_game_register.html')
            elif not phone.isdigit() or not qq.isdigit():
                messages.info(request, '请检查联系方式或QQ格式!')
                return render(request, 'temp1/letter_game_register.html')
            else:
                letter_user = models.letter_user(username=username, password=password, phone=phone, QQ=qq)
                letter_user.save()      # 保存、写入数据库
                messages.info(request, '注册成功！')
                return render(request, 'temp1/letter_game_register.html')
        else:
            messages.success(request, '请输入完整信息')
            return render(request, 'temp1/letter_game_register.html')
    elif request.method == 'GET':
        return render(request, 'temp1/letter_game_register.html')
# message 后面如果是render,则未跳转界面，可以看见提示，
# message 后面如果是httpresponse,则跳转界面，看不见提示。


@csrf_exempt
def letter_game_login(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        try:
            res = models.letter_user.objects.filter(username=name)[0]   # 返回的res对象是记录集合，而不是单个个体，但是记录不支持负索引
        except IndexError:
            messages.info(request, '找不到对应用户!')
            return render(request, 'temp1/letter_game_login.html')
        if res.password == password:
            return HttpResponseRedirect('/letter_game/play')
        else:
            messages.info(request, '用户名或密码错误!')
            return render(request, 'temp1/letter_game_login.html')
    elif request.method == 'GET':
        return render(request, 'temp1/letter_game_login.html', {'error_msg': ''})   # 默认get方法时返回的页面

# HttpResponseRedirect 页面跳转 render 页面渲染
# Http404 配合raise使用来实现404报错


def letter_game_play(request):
    if request.method == 'POST':
        hard = request.POST.get('hardlevel')
        return render(request, 'temp1/letter_game_play.html')
    elif request.method == 'GET':
        return render(request, 'temp1/letter_game_play.html')

