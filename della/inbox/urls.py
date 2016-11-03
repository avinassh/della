from django.conf.urls import url

from .views import MessageCreateView

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', MessageCreateView.as_view())
]
