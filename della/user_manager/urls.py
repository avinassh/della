from django.conf.urls import url

from .views import SignupView

urlpatterns = [
    url(r'^create/$', SignupView.as_view()),
]
