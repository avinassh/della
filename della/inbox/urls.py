from django.urls import path, re_path

from .views import (MessageCreateView, ThreadDetailView, ThreadListView,
                    SantaThreadDetailView, SanteeThreadDetailView)

app_name = 'inbox'

urlpatterns = [
    re_path(r'^@(?P<recipient>[a-zA-Z0-9_]+)/$', ThreadDetailView.as_view(),
        name='thread-detail'),
    path('<int:pk>/new/', MessageCreateView.as_view(),
        name='new-message'),
    path('santa/', SantaThreadDetailView.as_view(), name='santa-detail'),
    path('santee/', SanteeThreadDetailView.as_view(), name='santee-detail'),
    path('', ThreadListView.as_view(), name='threads')
]
