from turtle import pos
from urllib.parse import uses_relative
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Profile, Post, LikePost, FollowerCount
from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from itertools import chain


# Create your views here.


@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    #post = Post.objects.all().order_by('created_at').reverse()
    # post = Post.objects.exclude(user=request.user.username).order_by('created_at').reverse()
    user_following_list = list()
    feed = list()
    user_following = FollowerCount.objects.filter(follower = request.user.username)
    for users in user_following:
        user_following_list.append(users.user)
    
    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)
    feed_list = list(chain(*feed))
    context = {'user_profile': user_profile, 'posts': feed_list}
    return render(request, 'index.html', context)

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        xox = list(chain(*username_profile_list))
        
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': xox})

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
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, user_name=username).first()
    print(like_filter)

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, user_name=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def follow(request):
    if request.method == "POST":
        follower = request.POST['followers']
        user = request.POST['user']
        print(follower, user)

        if FollowerCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowerCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowerCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username = pk)
    user_profile = Profile.objects.get(user = user_object)
    post = Post.objects.filter(user=pk)
    post_count = len(post)

    follower = request.user.username
    user = pk 
    check_following = FollowerCount.objects.filter(follower = follower, user=user).first()
    follower_count = FollowerCount.objects.filter(user=pk).count()
    following_count = FollowerCount.objects.filter(follower=pk).count()
    # print(following_count)
    if check_following:
        button_text = "Unfollow"
    else:
        button_text = "Follow"
        #follower_count = FollowerCount.objects.filter(user=pk).count()
        #print(follower_count)

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'post_count': post_count,
        'user_post': post,
        'button_text': button_text,
        'follower_count': follower_count,
        "following_count": following_count,
    }
    return render(request, 'profile.html', context)

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
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password Not Matching')
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
            return HttpResponseRedirect('/')
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
