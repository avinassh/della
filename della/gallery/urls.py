from django.conf.urls import url

from .views import ImageUploadView, ImageDetailView

urlpatterns = [
    url(r'^upload/$', ImageUploadView.as_view()),
    url(r'^images/(?P<pk>\d+)/$', ImageDetailView.as_view())
]
