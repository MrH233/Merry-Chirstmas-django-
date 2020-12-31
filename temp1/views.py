from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from temp1 import models
import time
import random


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
        user = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        qq = request.POST.get('QQ')
        if user and password and phone and qq:
            if models.letter_user.objects.filter(username=user):
                messages.info(request, '用户已注册请勿重复注册!')
                return render(request, 'temp1/letter_game_register.html')
            elif not phone.isdigit() or not qq.isdigit():
                messages.info(request, '请检查联系方式或QQ格式!')
                return render(request, 'temp1/letter_game_register.html')
            else:
                letter_user = models.letter_user(username=user, password=password, phone=phone, QQ=qq)
                letter_user.save()  # 保存、写入数据库
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
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            res = models.letter_user.objects.filter(username=username)[0]  # 返回的res对象是记录集合，而不是单个个体，但是记录不支持负索引
        except IndexError:
            messages.info(request, '找不到对应用户!')
            return render(request, 'temp1/letter_game_login.html')
        if res.password == password:
            messages.success(request, '登录成功!')
            time.sleep(1)
            render(request, 'temp1/letter_game_login.html')
            return HttpResponseRedirect(f'play/{username}')
        else:
            messages.info(request, '用户名或密码错误!')
            return render(request, 'temp1/letter_game_login.html')
    elif request.method == 'GET':
        return render(request, 'temp1/letter_game_login.html', {'error_msg': ''})  # 默认get方法时返回的页面


# HttpResponseRedirect 页面跳转 render 页面渲染
# Http404 配合raise使用来实现404报错


@csrf_exempt
def letter_game_play(request, user):
    user = user.split('/')[-1]
    if request.method == 'POST':
        hard = request.POST.get('hardlevel')
        try:
            if not hard:
                messages.success(request, '请输入难度.(level1~level3)')
                return render(request, 'temp1/letter_game_play.html')
            elif hard[:5] != 'level' or int(hard[5:]) > 3 or int(hard[5:]) < 1:
                messages.success(request, '请输入正确难度.(level1~level3)')
                return render(request, 'temp1/letter_game_play.html')
            else:
                return HttpResponseRedirect(f'/letter_game/show/{user}')
        except ValueError:
            messages.success(request, '请输入正确难度.(level1~level3)')
            return render(request, 'temp1/letter_game_play.html')
    elif request.method == 'GET':
        if not models.letter_user.objects.filter(username=user):
            messages.info(request, '非法进入！')
            return HttpResponseRedirect('/letter_game/login')
        else:
            return render(request, 'temp1/letter_game_play.html')


ran = random.randint(1, 5500)


@csrf_exempt
def letter_game_show(request, user):
    global ran
    user = user.split('/')[-1]
    record = models.words.objects.get(id=ran)
    word = list(record.word)
    for i in random.sample(list(range(0, len(word))), round(0.4 * len(word))):
        word[i] = '_'
    word = ''.join(word)
    tips = record.transition

    if request.method == 'POST':
        ans = request.POST.get('answer')
        if ans == '':
            messages.info(request, '请输入答案!')
            return render(request, 'temp1/letter_game_show.html', {'word': word, 'tips': tips})
        elif ans != record.word:
            messages.info(request, f'猜错了噢，请再试试!')
            return render(request, 'temp1/letter_game_show.html', {'word': word, 'tips': tips})
        elif ans == record.word:
            add_object = models.letter_user.objects.get(username=user)
            add_object.score = add_object.score + 1
            add_object.save()
            messages.info(request, f'回答正确，答案就是{ans}，得一分!')
            ran = random.randint(1, 5500)  # 刷新数据
            return HttpResponseRedirect(f'/letter_game/show/{user}')    # 用HttpResponseRedirect而非render,因为渲染时采用的是先前数据，而直接跳转则不会
    elif request.method == 'GET':
        if not models.letter_user.objects.filter(username=user):
            messages.info(request, '非法进入！')
            return HttpResponseRedirect('/letter_game/login')
        else:
            return render(request, 'temp1/letter_game_show.html', {'word': word, 'tips': tips})


# HttpResponseRedirect 页面跳转 render 页面渲染
# 注意把握HttpResponseRedirect / render / HttpResponse 三者的差异
# 用render时,因为渲染时,如果引用数据,那引用的也是先前数据，而直接跳转(HRR)则不会,它会更新数据
# Http404 配合raise使用来实现404报错
# message 后面如果是render,则未跳转界面，可以看见提示，
# message 后面如果是httpresponse,则跳转界面，看不见提示。
