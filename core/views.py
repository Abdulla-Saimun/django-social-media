from turtle import pos
from urllib.parse import uses_relative
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Profile, Post, LikePost
from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.


@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    post = Post.objects.all().order_by('created_at').reverse()
    context = {'user_profile': user_profile, 'posts': post}
    return render(request, 'index.html', context)


@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signup')
def like_post(request):
    pass

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            print('hello')
            image = user_profile.profileimg
            # image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            print(image)
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile})


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['password2']
        print(username, email, pass1, pass2)
        if pass1 == pass2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'this email taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'this username taken')
                return redirect('signup')
            else:
                user = User.objects.create(username=username, email=email, password=pass1)
                user.save()

                user_login = auth.authenticate(username=username, password=pass1)
                auth.login(request, user_login)

                # create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'password not matches')
            return redirect('signup')

    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user_login = auth.authenticate(username=username, password=password)
        if user_login:
            auth.login(request, user_login)
            print('success')
            return redirect('/')
        else:
            print('fail')
            messages.info(request, 'Please enter the right credentials')
            return redirect('signin')


    else:
        return render(request, 'signin.html')


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')
