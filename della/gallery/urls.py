from django.conf.urls import url

from .views import ImageUploadView, ImageDetailView, ImageListView

urlpatterns = [
    url(r'^upload/$', ImageUploadView.as_view(), name='upload'),
    url(r'^(?P<pk>\d+)/$', ImageDetailView.as_view(), name='image-detail'),
    url(r'^$', ImageListView.as_view(), name='image-list')
]
