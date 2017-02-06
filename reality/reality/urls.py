from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from thoughts import views
from django.contrib import admin
from ajax_select import urls as ajax_select_urls


urlpatterns = [
    url(r"^$", views.home, name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r"^thoughts/", include("thoughts.urls")),
    url(r"^account/social/accounts/$", TemplateView.as_view(template_name="account/social.html"), name="account_social_accounts"),
    url(r"^account/social/", include("social.apps.django_app.urls", namespace="social")),
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    url(r'', include('taggit_live.urls')),
    url(r'^messages/', include('postman.urls', namespace='postman', app_name='postman')),
    url(r'^select/', views.UpdateView.as_view(), name='select'),
    url(r'^signup/', views.RegisterView, name='register'),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^friendship/', include('friendship.urls')),
    
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
