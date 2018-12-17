from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django import forms
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Buzz, Hashtag, Message, Chat, Follow, Notification
from .forms import PostForm, ProfileForm, Profile2Form, PMessageForm
from itertools import chain
from django.contrib.auth import login, authenticate, logout
import re

# Create your views here.
def index(request):
    if (request.user.is_authenticated):
        form = PostForm()
        return profile(request, request.user.username)        
    else:
        return render(request, "login.html")

def signupView(request):
    missatges = []
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
            missatges.append('El usuario ya existe')
            args = {'missatges': missatges}
            return render(request, "signup.html", args)

        else:
            user = User.objects.create_user(username=username, password=password)
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
                    return HttpResponseRedirect(reverse("profile", kwargs={'user': user}))
            # mensage de error
            missatges.append('No se ha podido agregar el usuario')
            return render(request, "signup.html")

    else:
        missatges.append('no es metode post')
        return render(request, "signup.html")


def loginView(request):
    missatges=[]
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:  # Active user are not banned users
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect(reverse("profile", kwargs={'user': user}))

        else:  # User is banned
            raise forms.ValidationError(_("This account is banned."), code='inactive', )
    else:
        # Show an error page
        args={}
        if request.method == 'POST':
            missatges.append('user no existe')
            args = {'missatges': missatges}
        return render(request, 'login.html', args)


@login_required
def logoutView(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect(reverse("index"))


def userSearch(request, search_text):
    usernameSearch = Profile.objects.filter(user__username__contains=search_text)
    profileSearch = Profile.objects.filter(screen_name__contains=search_text)
    fullSearch = usernameSearch | profileSearch
    response = [s for s in fullSearch]
    return response


def buzzSearch(request, search_text):
    search = Buzz.objects.filter(text__contains=search_text)
    response = [s for s in search]
    return response

def buzzSearchH(request, search_tag):
    posts = Buzz.objects.filter(published_date__lte=timezone.now()).order_by('published_date').filter(user__username=user)
    post_list = []
    for post in posts:
        for palabra in post.text.split():
            if (palabra == search_tag):  # El post tiene el tag
                post_list.append(post)
                break
    response = post_list
    return response

@login_required
def searchView(request, search_hastag=""):
    missatges = []
    if search_hastag:
        search_text = search_hastag
    else:
        search_text = request.POST.get('search_text')

    if search_text:
        search_hash = search_text.split(" ")

        if search_hash[0][0] == "#":
            buzzs = []
            for hashtag in search_hash:
                buzzs += buzzSearch(request, hashtag)

            args = {'buzzs': buzzs, 'search_text': search_text, 'hashtag': True, 'mencio': False, 'missatges': missatges}
            return render(request, 'search.html', args);
        elif search_hash[0][0] == "@":
            users = []
            for search_text in search_hash:
                users += userSearch(request, search_text[1:])
            args = {'users': users, 'search_text': search_text, 'hashtag': False, 'mencio': True,
                    'missatges': missatges}
            return render(request, 'search.html', args);
        elif request.method == "POST":
            users = userSearch(request, search_text)
            buzzs = buzzSearch(request, search_text)
            args = {'users': users, 'buzzs': buzzs, 'search_text': search_text, 'hashtag':False , 'mencio':False, 'missatges': missatges }
            return render(request, 'search.html', args)
        else:
            missatges.append('no se reconoce el texto')
            args = {'missatges': missatges}
            return render(request, 'search.html', args)
    return render(request, 'search.html')

@login_required
def actualizarProfile(request, user=""):
    form2 = Profile2Form(request.POST)
    if form2.is_valid():
        first_name = form2.cleaned_data['first_name']
        last_name = form2.cleaned_data['last_name']
        email = form2.cleaned_data['email']
        location = form2.cleaned_data['location']
        screen_name = form2.cleaned_data['screen_name']
        url = form2.cleaned_data['url']
        bio = form2.cleaned_data['bio']
        birthday = form2.cleaned_data['birthday']
        usuario = User.objects.filter(username=request.user).first()
        profile = usuario.profile

        if first_name:
            usuario.first_name = first_name
        if last_name:
            usuario.last_name = last_name
        if email:
            usuario.email = email
        if screen_name:
            profile.screen_name = screen_name
        if location:
            profile.location = location
        if url:
            profile.url = url
        if bio:
            profile.bio = bio
        if birthday:
            profile.birthday = birthday

        profile.save()
        usuario.save()

    return HttpResponseRedirect(reverse("profile", kwargs={'user': user}))

@login_required
def profile(request, user=""):
    # If the username is blank, redirect to login
    if User.objects.filter(username=user).exists():
        return getProfile(request, user)
    else:
        messages.error(request, "El usuario " + user + " no existe")
        return HttpResponseRedirect(reverse("index"))


def getProfile(request, user=""):
    if request.method == "GET":
        profile = User.objects.filter(username=user)
        posts = Buzz.objects.filter(published_date__lte=timezone.now()).order_by('published_date').filter(user__username=user)
        form = PostForm()
        form2 = Profile2Form()
        isFollowed = is_follow(request.user, user)
        args = {'posts': posts, 'form': form, 'form2': form2, 'profile': profile.first(), 'isFollowed': isFollowed}
        return render(request, 'profile.html', args)

    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published_date = timezone.now()
            post.save()
            # find hashtags and set buzzs in its hashtag
            hashtags_possible = re.findall(r'(##+)|#(\w+#)|#(\w+)',post.text)
            list_of_hashtags = []
            for pair in hashtags_possible:
                for i in range(3):
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

            return HttpResponseRedirect(reverse("profile", kwargs={'user': user}))


@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published_date = timezone.now()

            # If there is a file attached we save the file and file type in the database
            file = request.FILES.get('file', None)
            if file:
                post.file = file
                # Getting file type from MIME
                post.file_type = file.content_type.split('/')[0]

            if isMultimedia(post.file_type):
                post.save()
            else:
                messages.error(request, "El archivo introducido no es un archivo multimedia")
            users = re.findall(r'@(\w+)',post.text)
            for username in users:
                user = get_object_or_404(User,username=username)
                if user:
                    print(user.username)
                    create_notification('MENCION','El usuario ' + post.user.username + ' te ha mencionado', user, 2,
                                        None, post, None)


        return HttpResponseRedirect(reverse("profile", kwargs={'user': request.user.username}))

    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})


def isMultimedia(type): # Returns true if the file is multimedia, or if there's no file
    return type == 'image' or type == 'video' or type == 'audio' or type == ''


@login_required
def load_image(request):
    instance = get_object_or_404(Profile, user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.image = request.FILES['image']
            instance.save()

            return HttpResponseRedirect(reverse("profile", kwargs={'user': request.user.username}))

    else:
        form = ProfileForm()

    return render(request, 'edit.html', {'form': form})

def posts_hashtags(user,tag):
    posts = Buzz.objects.filter(published_date__lte=timezone.now()).order_by('published_date').filter(user__username=user)
    post_list = []
    for post in posts:
        for palabra in post.text.split():
            if(palabra==tag): # El post tiene el tag
                post_list.append(post)
                break
    return post_list


@login_required
def private_messages(request):
    if request.method == "GET":
        user = request.user
        chat_list = search_chats(user.username)
        args = {'chats': chat_list}
        return render(request, "messages.html", args)


@login_required
def conversation(request, user):

    try:
        username = User.objects.get(username=user).username
    except User.DoesNotExist:
        username = None

    if username is None:
        messages.error(request, "ERROR: El usuario " + user + " no existe")
        return HttpResponseRedirect(reverse("messages"))

    if request.method == "GET":
        people = [request.user.username, user]
        chat = search_chat(people)
        pmessages = messages_chat(chat.id_chat)

        profile = User.objects.filter(username=user)

        form = PMessageForm(auto_id=False)

        args = { "pmessages": pmessages, "profile": profile.first(), "pform": form }

        return render(request, "chat.html", args)

    if request.method == "POST":
        form = PMessageForm(request.POST)

        if form.is_valid():
            msg = form.save(commit=False)
            msg.user = request.user
            msg.date = timezone.now()

            people = [request.user.username, user]
            chat = search_chat(people)

            msg.chat = chat

            msg.save()

        return HttpResponseRedirect(reverse("chat", kwargs={'user': user}))


def follow_toggle(request):
    user = request.GET.get('user', None)
    profile = request.GET.get('profile', None)

    if not user or not profile:
        messages.error(request, "Acceso denegado")
        return HttpResponseRedirect(reverse("profile", kwargs={'user': request.user.username}))

    if is_follow(user, profile):
        unfollow(user, profile)
    else:
        new_follow_usernames(user, profile)

    profile_user = User.objects.get(username=profile)

    data = {
        'followers': profile_user.profile.count_follower
    }

    return JsonResponse(data)


# search list of chats of one user
def search_chats(user_name):
    userchat = User.objects.get(username=user_name)
    return userchat.chat_set.all()


# create a chat and return
def create_chat(users_list,chat_name=""):
    if chat_name:
        chat = Chat.objects.create(name=chat_name)
    else:
        for user in users_list:
            chat_name += str(user.username)
        chat = Chat.objects.create(name=chat_name)
    chat.members.set(users_list)

    chat.save()

    return chat


# Search a chat of a list of users, creates the chat if it doesn't exist
# Receives a list with the name of every user, sender being the first one
def search_chat(username_list):
    chat_list = search_chats(username_list[0])
    member_list = []

    # Search the chat
    for chat in chat_list:
        member_list = []
        for member in  chat.members.all():
            member_list.append(member.username)

        # If the two lists are equal we found the chat
        if sorted(member_list) == sorted(username_list):
            return chat

    # If the chat is not found we create it
    list_of_users = []
    for user_name in username_list:
        user = User.objects.get(username=user_name)
        list_of_users.append(user)
    return create_chat(list_of_users)


# create message
def create_message(chat_id,user_name,text_message):
    chat = Chat.objects.get(id_chat=chat_id)
    user = User.objects.get(username = user_name)
    message = Message.objects.create(chat=chat,user=user)
    message.date = timezone.now()
    message.content = text_message
    message.save()
    return message

# return all messages of a chat ordered by date
def messages_chat(chat_id):
    chat = Chat.objects.get(id_chat=chat_id)
    #list_of_messages = sorted(chat.messages.all , key = lambda x: x.object.time)
    list_of_messages = chat.message_set.all()

    return list_of_messages

# send a message directly from sender to receiver
#   chek if chat between them exists and create if it does not exist
def send_message(sender_name,receiver_name,text_message,notified):
    list_of_user_names = [sender_name,receiver_name]
    chat = search_chat(list_of_user_names)
    user = User.objects.get(username = sender_name)
    user_reciver = User.objects.get(username=receiver_name)
    message = Message.objects.create(chat=chat,user=user)
    message.date = timezone.now()
    message.content = text_message
    message.notified = notified
    message.save()
    create_notification('Tienes un nuevo mensaje', 'El usuario' + sender_name + 'te ha mandado un mensaje nuevo', user_reciver, 1, message, None, None)
    return message 

# check follow relationship exists
def is_follow(follower_name,followed_name):
    follower = User.objects.get(username=follower_name)
    followed = User.objects.get(username=followed_name)
    list_of_follows = Follow.objects.filter(follower=follower,followed=followed)
    return(list_of_follows.count() != 0)

# create a new follow
def new_follow(follower,followed):
    follows = Follow.objects.filter(follower=follower,followed=followed)
    if not(follows): 
        follow = Follow.objects.create(follower=follower,followed=followed)
        follow.save()
        follower.profile.count_followed += 1
        follower.profile.save()  
        followed.profile.count_follower += 1
        followed.profile.save()
    else:
        follow = follows[0]        
    return(follow)

# create a new follow (usernames)
def new_follow_usernames(follower_name,followed_name):
    follower = User.objects.get(username=follower_name)
    followed = User.objects.get(username=followed_name)   
    follow = new_follow(follower,followed)    
    return(follow)

def unfollow(follower_name, followed_name):
    follower = User.objects.get(username=follower_name)
    followed = User.objects.get(username=followed_name)
    list_of_follows = Follow.objects.filter(follower=follower,followed=followed)
    
    for follow in list_of_follows:
        follow.delete()        
        
        follower.profile.count_followed -= 1
        follower.profile.save()

        followed.profile.count_follower -= 1
        followed.profile.save()

# search follows of an user (username)
def search_follows(follower_name):
     follower = User.objects.get(username=follower_name)              
     return follower.profile.get_follows()

# search followeds of an user (username)
def search_followeds(follower_name):
     follower = User.objects.get(username=follower_name)             
     return follower.profile.get_followeds()

# search followers of an user (username)
def search_followers(followed_name):
     followed = User.objects.get(username=followed_name)              
     return followed.profile.get_followers()

# create a new follow (followed) from a request
def followCreate(request, follower="",followed=""):
    follow = new_follow_usernames(follower,followed)
    response = str(follow)
    return HttpResponse(response)

# search all follows (followeds) from a request
def followSearch(request, follower=""):
    follows = search_follows(follower)
    response = "You're looking all follows relationship as follower:"
    response = response + '<BR> <li>' + '<BR> <li>'.join(
         [str(follow) for follow in follows])

    return HttpResponse(response)

# create new notification
def create_notification(title, description, user_notify, type_notification, message=None, buzz=None, follower=None):
    notification = Notification(title = title ,description = description)
    notification.save()
    notification.user_notify = user_notify
    notification.type_notification = type_notification
    if type_notification==1: # notification of message
        notification.message = message
    else:    	
        if type_notification==2:  # notification of buzz        
            notification.buzz = buzz
        else:  # notification of follower (type_notification==3)  
            notification.buzz = follower
    notification.save()
    user_notify.profile.count_notification += 1
    user_notify.profile.save()   

# search all notification of user
def search_notifications(user):
    notifications = Notification.objects.filter(user_notify = user)
    return notifications

# search all pending notifications of user
def search_notifications_pending(user):
    notifications = Notification.objects.filter(user_notify = user)
    list_of_pending_notifications = []
    for notification in notifications:
        if not(notification.showed):
            list_of_pending_notifications.append(notification)
    return list_of_pending_notifications

# set all pending notifications of user as showed (showed=True)
def set_notifications_showed(user):
    notifications = search_notifications_pending(user)
    count_showed = 0
    for notification in notifications:
        notification.showed = True
        notification.save()
        count_showed += 1
    user.profile.count_notification -= count_showed
    user.profile.save()

def look_for_new_messages(user_name):
    user = User.objects.get(username=user_name) # We get the user
    chats = user.chat_set.all()     # Get all the chats of the user
    notify = {}
    for chat in chats:
        # Get all the messages of the chat
        messages = messages_chat(chat.id_chat)
        for i in range(len(messages)):
            # If the message is not notified
            if messages[i].notified == False:
                # We add it to the notify dictionary
                notify[i] = messages[i]
    # return the dictionary
    return notify

def notified(notified):
    pass

def message_notify(request, user=None):
    user = User.objects.get(username=request.user)  # We get the user
    notify = search_notifications_pending(user)
    set_notifications_showed(user)

    return render(request,'notifications.html',{'notificaciones': notify})

def search_notify(username):
    user = User.objects.get(username=username)
    return user

