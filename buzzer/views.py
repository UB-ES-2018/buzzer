from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from .models import Buzz
from django.contrib.auth import login, authenticate, logout
from itertools import chain
from .forms import PostForm
from .models import Buzz
from .models import Hashtag
import re

# Create your views here.
def index(request):
    if(request.user.is_authenticated):
        form = PostForm()
        return render(request, 'testLogin.html', {'form': form})
    else :
        return render(request, "signup.html")

# List All Users or List one (username)
def users(request, user=""):
    response = "You aren't admin"
    if request.user.is_superuser:
        if user:
            response = "You're looking for user from %s <BR>" % user
            list_of_users = User.objects.filter(username=user)
            response = response + '<BR> <li>' + '<BR> <li>'.join([str(user.id) + " - " + str(user) for user in list_of_users])
        else:
            response = "You're looking all Users"
            list_of_users = User.objects.filter()
            response = response + '<BR> <li>' + '<BR> <li>'.join([str(user.id) + " - " + str(user) for user in list_of_users])

    return HttpResponse(response)

# List All Users+Profile or List one (username)
def profiles(request, user=""):
    response = "You aren't admin"
    if request.user.is_superuser:
        if user:
            response = "You're looking for user from %s <BR>" % user
            list_of_users = User.objects.filter(username=user)
            response = response + '<BR> <li>' + '<BR> <li>'.join([Profile.all_fields(user.profile) for user in list_of_users])
        else:
            response = "You're looking all Users"
            list_of_users = User.objects.filter()
            response = response + '<BR> <li>' + '<BR> <li>'.join([Profile.all_fields(user.profile) for user in list_of_users])

    return HttpResponse(response)

# List All Buzzs or List of one username
def buzzs(request, user=""):
    response = "You aren't admin"
    if request.user.is_superuser:
        if user:
            response = "You're looking for buzz of user from %s <BR>" % user
            list_of_users = User.objects.filter(username=user)
            for userlist in list_of_users:
                list_of_buzzs = Buzz.objects.filter(user_id=userlist.id)
                response = response + '<BR> <li>' + '<BR> <li>'.join([Buzz.all_fields(buzz) for buzz in list_of_buzzs])
        else:
            response = "You're looking all Users"
            list_of_buzzs = Buzz.objects.filter()
            response = response + '<BR> <li>' + '<BR> <li>'.join([Buzz.all_fields(buzz) for buzz in list_of_buzzs])

    return HttpResponse(response)


def signupView(request):

    if request.method == 'POST':

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        first_name = request.POST.get('name', '')
        last_name = request.POST.get('surname', '')
        email = request.POST.get('email', '')
        screen_name = request.POST.get('usertag', '')

        user = authenticate(username=username, password=password)

        if user is not None:
            # mensage de error ja existeix
            return render(request, "signup.html")

        else:
            user = User.objects.create_user(username=username,password=password)
            if user is not None:
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()
                profile = Profile.objects.create(user=user)
                profile.screen_name = screen_name
                profile.save()
                if user.is_active:  # Active user are not banned users
                    login(request, user)
                    # Redirect to a success page.
                    return HttpResponseRedirect(reverse('index'))
            #mensage de error
            return render(request, "signup.html")

    else:
        return render(request, "signup.html")

def loginView(request):
    username = request.POST.get('username', '')    
    password = request.POST.get('password', '')    
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:  # Active user are not banned users
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect(reverse('index'))

        else:   # User is banned
            raise forms.ValidationError(_("This account is banned."), code='inactive',)
    else:
        # Show an error page
        return render(request, 'login.html')


@login_required
def logoutView(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect(reverse("index"))


def userSearch(request, search_text):
    usernameSearch = Profile.objects.filter(user__username__contains=search_text)
    profileSearch= Profile.objects.filter(screen_name__contains=search_text)
    fullSearch = usernameSearch | profileSearch

    response = [s for s in fullSearch]
    return response


def buzzSearch(request, search_text):
    search = Buzz.objects.filter(text__contains=search_text)

    response = [s for s in search]
    return response


def searchView(request):
    search_text = request.POST.get('search_text')

    if request.method == "POST":
        users = userSearch(request, search_text)
        buzzs = buzzSearch(request, search_text)
        args = {'users': users, 'buzzs': buzzs, 'search_text': search_text}
        return render(request, 'search.html', args)
    return render(request,'search.html')


def profile(request, user=""):  # TEMPORAL
    if request.method == "GET":
        profile = User.objects.filter(username=user)
        posts = Buzz.objects.filter(published_date__lte=timezone.now()).order_by('published_date').filter(user__username=user)
        form = PostForm()

        args = {'posts': posts, 'form': form, 'profile': profile.first(),}
        
        return render(request, 'profile.html', args)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published_date = timezone.now()
            post.save()        

            # find hashtags and set buzzs in its hashtag
            hashtags_possible = re.findall(r'#(\w+#)|#(\w+)',post.text)
            list_of_hashtags = []
            for pair in hashtags_possible:
                for i in range(2):	
                    if pair[i] != '' and pair[i].find('#')==-1:
                        if pair[i] not in list_of_hashtags:
                            list_of_hashtags.append(pair[i])        
            for tag in list_of_hashtags:
                if Hashtag.objects.filter(text = tag).exists():
                    hashtag = Hashtag.objects.filter(text = tag)[0]
                else: 
                    hashtag = Hashtag.objects.create(text = tag)
                hashtag.buzzs.add(post)
                hashtag.save()

                

            return HttpResponseRedirect(reverse("profile", kwargs={'user': user }))

"""
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published_date = timezone.now()
            post.save()
            return render(request,'testLogin.html')
    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})
"""

# List All Buzzs or List of one hashtag
def hashtags(request, text_hashtag=""):
    response = "You aren't admin"
    p = posts_hashtags(text_hashtag)
    if request.user.is_superuser:
        if text_hashtag:
            response = "You're looking for buzz of hashtag from %s <BR>" % text_hashtag
            list_of_hashtags = Hashtag.objects.filter(text=text_hashtag)

            for hashtaglist in list_of_hashtags:
                list_of_buzzs = hashtaglist.buzzs.all()
                response = response + '<BR> <li>' + '<BR> <li>'.join([Buzz.all_fields(buzz) for buzz in list_of_buzzs])
        else:
            response = "You're looking all hashtags"
            list_of_hashtags = Hashtag.objects.filter()
            response = response + '<BR> <li>' + '<BR> <li>'.join([str(hashtag) for hashtag in list_of_hashtags])

    return render(request,'find_tags.html',{'response':response,'list_post':p,'tag':text_hashtag})

def posts_hashtags(tag):
    #posts =Buzz.objects.filter(published_date__lte=timezone.now()).order_by('published_date').filter(user__username=user)
    posts = Buzz.objects.all()
    post_list = []
    for post in posts:
        for palabra in post.text.split():
            if(palabra==tag): # El post tiene el tag
                post_list.append(post)
                break
    return post_list