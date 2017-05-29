from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.db.models import Count
from models import *

def index(request):
    if 'user_id' in request.session:
        return redirect('/secrets')
    return render(request, 'dojo_secrets/index.html')

def register(request):
    if request.method == 'POST':
        checker = User.objects.isValid(request.POST)
        if checker['pass'] == True:
            user = User.objects.createUser(request.POST)
            context={'name': user.first_name}
            request.session['user_id']=user.id
            # print request.session['user_id']
            return redirect('/secrets')
        for error in checker['errors']:
            messages.error(request, error)
    return redirect('/')

def login(request):
    if request.method=='POST':
        logger=User.objects.logging_in(request.POST)
        if logger['pass']==True:
            user=logger['user'].first_name
            context={'name': user}
            request.session['user_id']=logger['user'].id
            # print request.session['user_id']
            # return render(request, 'dojo_secrets/secrets.html', context)
            return redirect('/secrets')
        else:
            for error in logger['errors']:
                messages.error(request, error)
    return redirect('/')

def secrets(request):
    if 'user_id' in request.session:
        user=User.objects.findUser(request.session)
        all_secrets=Secret.objects.all().order_by('-created_at')[:10]
        # all_content=[]
        # for secret in all_secrets:
        #      all_content.append(secret)
        context={'all_secrets':all_secrets, 'user': user}
        return render(request, 'dojo_secrets/secrets.html', context)
    return redirect('/')

def popular(request):
    if 'user_id' in request.session:
        user=User.objects.findUser(request.session)
        most_popular=Secret.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:5]
        context={'most_popular': most_popular, 'user': user}
        return render(request, 'dojo_secrets/popular.html', context)

def like(request, find):
    user=User.objects.findUser(request.session)
    print 'user', user
    secret=Secret.objects.filter(id=find).first()
    print secret
    secret.likes.add(user)

    return redirect('/secrets')

    # like = Post.objects.create(liked_posts__user)


def unlike(request, find):
    user=User.objects.findUser(request.session)
    secret=Secret.objects.filter(id=find).first()
    secret.likes.remove(user)
    return redirect('/secrets')



def submit_secret(request):
    if request.method == 'POST':
        user=User.objects.findUser(request.session)
        new=Secret.objects.create(content=request.POST['content'], user=user)
    return redirect('/secrets')

def delete(request, find):
    Secret.objects.filter(id=find).delete()
    return redirect('/secrets')

def logout(request):
    request.session.clear()
    return redirect('/')
