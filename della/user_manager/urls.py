from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from .views import (SignupView, UserProfileUpdateView, DrawNamesView,
                    UserProfileDetailView, ActivateView,
                    RequestActivationEmailView, MassEmailView)

app_name = 'user_manager'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="user_manager/login.html"), name='login',
        ),
    path('logout/', auth_views.LogoutView, name='logout',
        kwargs={'next_page': '/'}),
    path('signup/', SignupView.as_view(), name='signup'),
    path('account/', UserProfileUpdateView.as_view(), name='account'),
    re_path(r'^activate/(?P<username>[0-9A-Za-z_]+)-(?P<code>[0-9A-Za-z_:-]+)/$',
        ActivateView.as_view(), name='activate-user'),
    path('activate/request/', RequestActivationEmailView.as_view(),
        name='activate-request'),
    path('draw-names/', DrawNamesView.as_view(), name='draw-names'),
    path('mass-email/', MassEmailView.as_view(), name='mass-email'),
    re_path(r'^@(?P<username>[a-zA-Z0-9_]+)/$', UserProfileDetailView.as_view(),
        name='user-detail'),
]
