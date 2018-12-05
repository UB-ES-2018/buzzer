from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Buzz, Hashtag, Message, Chat
from .forms import PostForm, ProfileForm, Profile2Form, PMessageForm
from itertools import chain
from django.contrib.auth import login, authenticate, logout

# Create your views here.
def index(request):
    if (request.user.is_authenticated):
        form = PostForm()
        return render(request, 'profile.html', {'form': form})
    else:
        return render(request, "login.html")


# List All Users or List one (username)
@login_required
def users(request, user=""):
    response = "You aren't admin"
    if request.user.is_superuser:
        if user:
            response = "You're looking for user from %s <BR>" % user
            list_of_users = User.objects.filter(username=user)
            response = response + '<BR> <li>' + '<BR> <li>'.join(
                [str(user.id) + " - " + str(user) for user in list_of_users])
        else:
            response = "You're looking all Users"
            list_of_users = User.objects.filter()
            response = response + '<BR> <li>' + '<BR> <li>'.join(
                [str(user.id) + " - " + str(user) for user in list_of_users])
    return HttpResponse(response)


# List All Users+Profile or List one (username)
@login_required
def profiles(request, user=""):
    response = "You aren't admin"
    if request.user.is_superuser:
        if user:
            response = "You're looking for user from %s <BR>" % user
            list_of_users = User.objects.filter(username=user)
            response = response + '<BR> <li>' + '<BR> <li>'.join(
                [Profile.all_fields(user.profile) for user in list_of_users])
        else:
            response = "You're looking all Users"
            list_of_users = User.objects.filter()
            response = response + '<BR> <li>' + '<BR> <li>'.join(
                [Profile.all_fields(user.profile) for user in list_of_users])
    return HttpResponse(response)


# List All Buzzs or List of one username
@login_required
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
                    return HttpResponseRedirect(reverse('index'))
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
            return HttpResponseRedirect(reverse('index'))

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
    if search_hastag != "":
        search_text = search_hastag
    else:
        search_text = request.POST.get('search_text')

    if search_text is not None and search_text != "":
        search_hash = search_text.split(" ")
        if search_hash[0][0] == "#":
            buzzs = []
            for hashtag in search_hash:
                buzzs += buzzSearch(request, hashtag)
            args = {'buzzs': buzzs, 'search_text': search_text, 'hashtag': True, 'missatges': missatges}
            return render(request, 'search.html', args);
        if request.method == "POST":

            users = userSearch(request, search_text)
            buzzs = buzzSearch(request, search_text)
            args = {'users': users, 'buzzs': buzzs, 'search_text': search_text, 'hashtag':False , 'missatges': missatges }
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

        if first_name != '':
            usuario.first_name = first_name
        if last_name != '':
            usuario.last_name = last_name
        if email != '':
            usuario.email = email
        if screen_name != '':
            profile.screen_name = screen_name
        if location != '':
            profile.location = location
        if url != '':
            profile.url = url
        if bio != '':
            profile.bio = bio
        if birthday != '':
            profile.birthday = birthday

        profile.save()
        usuario.save()

        return HttpResponseRedirect(reverse("profile", kwargs={'user': user}))
    return HttpResponseRedirect(reverse("profile", kwargs={'user': user}))

@login_required
def profile(request, user=""):  # TEMPORAL
    if request.method == "GET":
        profile = User.objects.filter(username=user)
        posts = Buzz.objects.filter(published_date__lte=timezone.now()).order_by('published_date').filter(user__username=user)
        form = PostForm()        
        form2 = Profile2Form()
        args = {'posts': posts, 'form': form, 'form2': form2, 'profile': profile.first()}


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
def post_new(request):
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
    posts =Buzz.objects.filter(published_date__lte=timezone.now()).order_by('published_date').filter(user__username=user)
    post_list = []
    for post in posts:
        for palabra in post.text.split():
            #print(palabra,tag)
            if(palabra==tag): # El post tiene el tag
                post_list.append(post)
                break
    return post_list

# define equal in lists
def equal_list(list1,list2):
    list1.sort()
    list2.sort()
    equals = True
    if len(list1) != len(list2):
        equals = False
    else:
        for i in range(len(list1)):
            if list1[i] != list2[i]:
                equals = False
                break

    return equals


@login_required
def private_messages(request):
    if request.method == "GET":
        user = request.user
        chat_list = search_chats(user.username)
        args = { "chats" : chat_list }
    
        return render(request, "messages.html", args)


@login_required
def conversation(request, user):
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

# search list of chats of one user
def search_chats(user_name):
    userchat = User.objects.get(username=user_name)
    list_of_chats = userchat.chat_set.all()
    return list_of_chats

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

# search chat of a list of users  (if the chat doesnt exist it will be created)
#    enter a list of names of all users (first sender)
#    return chat 
def search_chat(list_of_user_names):
    list_of_chats = search_chats(list_of_user_names[0])
    found = False
    list_of_member_names = []
    
    for chat in list_of_chats:
        list_of_member_names = []
        for member in  chat.members.all():
            list_of_member_names.append(member.username)
        if equal_list(list_of_member_names,list_of_user_names):
            found= True
            chat_return = chat
            break

    if (not found):
       list_of_users = []
       for user_name in list_of_user_names:
           user = User.objects.get(username=user_name)
           list_of_users.append(user)
       chat_return = create_chat(list_of_users)
    
    return chat_return

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
    message = Message.objects.create(chat=chat,user=user)
    message.date = timezone.now()
    message.content = text_message
    message.notified = notified
    message.save()

    return message 
