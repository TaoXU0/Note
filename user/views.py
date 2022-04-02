from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import hashlib
# Create your views here.
from .models import *


def reg_view(request):
    # Register
    if request.method == 'GET':
        # GET return page
        return render(request, 'user/register.html')

    elif request.method == 'POST':
        # process posted data
        username = request.POST.get('username')
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        # 1. Two passwords needs to be same
        if password_1 != password_2:
            return HttpResponse('Two password is different.')
        # hash table
        m = hashlib.md5()
        m.update(password_1.encode())  # change string to bytes
        password_m = m.hexdigest()
        # 2. If the username valid
        old_users = User.objects.filter(username=username)
        if old_users:
            return HttpResponse('Username has been registered.')
        # 3. Store data
        try:
            user = User.objects.create(username=username, password=password_m)
        except Exception as e:
            print('--create user is error %s' % e)
            return HttpResponse('Username has been registered.')
        # Create session
        request.session['username'] = username
        request.session['uid'] = user.id

        return HttpResponseRedirect('/index')


def login_view(request):
    # login
    # GET return page
    if request.method == 'GET':
        # check login state
        if request.session.get('username') and request.session.get('uid'):
            return HttpResponseRedirect('/index')
        c_username = request.COOKIES.get('username')
        c_uid = request.COOKIES.get('uid')
        if c_username and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return HttpResponseRedirect('/index')
        return render(request, 'user/login.html')
    # POST process data
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except Exception as e:
            print('login user error is %s' % e)
            return HttpResponse('User name or password is wrong')

        # Compare the password
        m = hashlib.md5()
        m.update(password.encode())

        if m.hexdigest() != user.password:
            return HttpResponse('User name or password is wrong')

        # create session
        request.session['username'] = username
        request.session['uid'] = user.id

        resp = HttpResponseRedirect('/index')
        # if user click remember username then add cookies
        if 'remember' in request.POST:
            resp.set_cookie(key='username', value=username, max_age=3*3600*24)
            resp.set_cookie(key='uid', value=user.id, max_age=3*3600*24)

        return resp
