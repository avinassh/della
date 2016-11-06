from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import (SignupView, UserProfileUpdateView, DrawNamesView,
                    UserProfileDetailView)

urlpatterns = [
    url(r'^login/$', auth_views.login, name='login',
        kwargs={'template_name': 'user_manager/login.html'}),
    url(r'^logout/$', auth_views.logout, name='logout',
        kwargs={'next_page': '/'}),
    url(r'^create/$', SignupView.as_view()),
    url(r'^update/$', UserProfileUpdateView.as_view(), name='update'),
    url(r'^draw-names/$', DrawNamesView.as_view()),
    url(r'^@(?P<username>[a-zA-Z0-9_]+)/$', UserProfileDetailView.as_view(),
        name='user-detail'),
]
