from django.conf.urls import include, url
from . import views
from django.views.generic import RedirectView

urlpatterns = [
	url(r'^thot/', views.new_thought, name='new_thought'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^mythots/', views.my_thoughts, name='thots'),
    url(r'^tech/', views.tech, name='tech'),
    url(r'^users/$', 'thoughts.views.users', name='users'),
    url(r'^users/(?P<username>\w{0,30})/$', 'thoughts.views.users', name='found'),
    url(r'^follow/', 'thoughts.views.follow', name='follow'),
    url(r'^unfollow/', 'thoughts.views.unfollow', name='unfollow'),
    url(r'^User-autocomplete/$', views.UserAutocomplete.as_view(), name='User-autocomplete'),
    url(r'^search/', views.UpdateView.as_view(), name="tosearch"),
    url(r'^searched/', views.search, name='search'),
    url(r'^$', RedirectView.as_view(permanent=True, url='inbox/'), name='messages_redirect'),
    url(r'front', views.Update2View.as_view(), name='frontbaby'),
    url(r'^like/$', 'thoughts.views.like', name='like'),
    url(r'^pls/$', 'thoughts.views.pls', name='pls'),
    url(r'^fs/$', 'thoughts.views.FollowerFollowing', name='fs'),

]