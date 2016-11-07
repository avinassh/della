from django.conf.urls import url

from .views import (MessageCreateView, ThreadDetailView, ThreadListView,
                    SantaThreadDetailView, SanteeThreadDetailView)

urlpatterns = [
    url(r'^@(?P<recipient>[a-zA-Z0-9_]+)/$', ThreadDetailView.as_view(),
        name='thread-detail'),
    url(r'^(?P<pk>\d+)/new/$', MessageCreateView.as_view(),
        name='new-message'),
    url(r'^santa/', SantaThreadDetailView.as_view(), name='santa-detail'),
    url(r'^santee/', SanteeThreadDetailView.as_view(), name='santee-detail'),
    url(r'^$', ThreadListView.as_view(), name='threads')
]
