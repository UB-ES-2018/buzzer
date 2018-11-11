from django.conf.urls import url
from . import views

urlpatterns = [
    
    url(r'^$', views.index, name='index'),
    # Authentication
    url(r'^signup/$', views.signupView, name='signup'),
    url(r'^login/$', views.loginView, name='login'),    
    url(r'^logout/$', views.logoutView, name='logout'),
    
    # Search
    url(r'^search/$', views.searchView, name='search'),
    
    # Extras
    #url(r'^new_post/$', views.post_new, name='post_new'),
    url(r'^profile/(?P<user>.*)/$', views.profile, name='profile'),

    # Browser DBs
    url(r'^users/$', views.users, name='users'),
    url(r'^users/(?P<user>.*)/$', views.users, name='users'),  
    url(r'^profiles/$', views.profiles, name='profiles'),
    url(r'^profiles/(?P<user>.*)/$', views.profiles, name='profiles'),    
    url(r'^buzzs/$', views.buzzs, name='buzzs'),
    url(r'^buzzs/(?P<user>.*)/$', views.buzzs, name='buzzs'),
    url(r'^hashtags/$', views.hashtags, name='hashtags'),
    url(r'^hashtags/(?P<text_hashtag>.*)/$', views.hashtags, name='hashtags')
]

