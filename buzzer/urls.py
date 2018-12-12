from django.conf.urls import url
from . import views

urlpatterns = [
    
    url(r'^$', views.index, name='index'),
    # Authentication
    url(r'^signup/$', views.signupView, name='signup'),
    url(r'^login/$', views.loginView, name='login'),    
    url(r'^logout/$', views.logoutView, name='logout'),
    
    # Search
    url(r'^search/(?P<search_hastag>.*)/$', views.searchView, name='search'),
    url(r'^search/$', views.searchView, name='search'),

    
    # Extras
    url(r'^new_post/$', views.post_new, name='post_new'),
    url(r'^profile/(?P<user>.*)/$', views.profile, name='profile'),
    url(r'^actualizarProfile/(?P<user>.*)/$', views.actualizarProfile, name='actualizarProfile'),
    url(r'^messages/$', views.private_messages, name='messages'),
    url(r'^message/$', views.conversation, name="chat"),
    url(r'^message/(?P<user>.*)/$', views.conversation, name="chat"),
    url(r'^followCreate/(?P<follower>.*)/(?P<followed>.*)/$', views.followCreate, name='followCreate'),
    url(r'^followSearch/(?P<follower>.*)/$', views.followSearch, name='followSearch'),
    
    # Ajax
    url(r'^ajax/follow_toggle/$', views.follow_toggle, name='follow_toggle'),

    # Browser DBs
    url(r'^upload/$', views.load_image, name='load_image'),

    url(r'^notify/$', views.message_notify, name='message_notify'),
    url(r'^notify/(?P<user>.*)/$', views.message_notify, name='message_notify'),


]

