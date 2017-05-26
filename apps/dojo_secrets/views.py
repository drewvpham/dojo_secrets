from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from models import *
# Create your views here.

def index(request):
    return render(request, 'dojo_secrets/index.html')

def register(request):
    if request.method == 'POST':
        checker = User.objects.isValid(request.POST)
        print checker
        if checker['pass'] == True:
            user = User.objects.createUser(request.POST)
            print user
            context={'name': user.first_name}
            request.session['user_id']=user.id
            return render(request, 'dojo_secrets/secrets.html', context)
        else:
            for error in checker['errors']:
                messages.error(request, error)
            return redirect('/')


def login(request):
    if request.method=='POST':
        logger=User.objects.logging_in(request.POST)
        if logger['pass']==True:
            user=logger['user'].first_name
            context={'name': user}
            return render(request, 'dojo_secrets/secrets.html', context)
        else:
            for error in logger['errors']:
                messages.error(request, error)
            return redirect('/')

def secrets(request):
    return render(request, 'dojo_secrets/secrets.html')

#
# def logout(request):
#     if request.method=='POST':
#         request.session.clear()
#         return redirect('/')
