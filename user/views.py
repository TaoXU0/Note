from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

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

        # 2. If the username valid
        old_users = User.objects.filter(username=username)
        if old_users:
            return HttpResponse('Username is registered.')
        # 3. Store data
        User.objects.create(username=username, password=password_1)
        return HttpResponse('Successfully register')

