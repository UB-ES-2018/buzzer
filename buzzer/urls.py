from django.conf.urls import url
from . import views

urlpatterns = [
    # Index
    url(r'^$', views.index, name='index'),

    # Authentication
    url(r'^signup/$', views.signupView, name='signup'),
    url(r'^login/$', views.loginView, name='login'),
    url(r'^logout/$', views.logoutView, name='logout'),

    # Search
    url(r'^search/(?P<search_hastag>.*)/$', views.searchView, name='search'),
    url(r'^search/$', views.searchView, name='search'),

    # Create a new post
    url(r'^new_post/$', views.new_post, name='new_post'),

    # Profile
    url(r'^profile/(?P<user>.*)/$', views.profile, name='profile'),
    url(r'^actualizarProfile/(?P<user>.*)/$', views.actualizarProfile, name='actualizarProfile'),

    # Private messages
    url(r'^messages/$', views.private_messages, name='messages'),
    url(r'^message/$', views.conversation, name="chat"),
    url(r'^message/(?P<user>.*)/$', views.conversation, name="chat"),
    url(r'^followCreate/(?P<follower>.*)/(?P<followed>.*)/$', views.followCreate, name='followCreate'),
    url(r'^followSearch/(?P<follower>.*)/$', views.followSearch, name='followSearch'),
    
    # Ajax
    url(r'^ajax/follow_toggle/$', views.follow_toggle, name='follow_toggle'),

    # Browser DBs
    url(r'^users/$', views.users, name='users'),
    url(r'^users/(?P<user>.*)/$', views.users, name='users'),
    url(r'^profiles/$', views.profiles, name='profiles'),
    url(r'^profiles/(?P<user>.*)/$', views.profiles, name='profiles'),
    url(r'^buzzs/$', views.buzzs, name='buzzs'),
    url(r'^buzzs/(?P<user>.*)/$', views.buzzs, name='buzzs'),
    url(r'^upload/$', views.load_image, name='load_image'),

    url(r'^notify/$', views.message_notify, name='message_notify'),
    url(r'^notify/(?P<user>.*)/$', views.message_notify, name='message_notify'),

]
