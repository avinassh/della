from django.urls import path

from .views import ImageUploadView, ImageDetailView, ImageListView

app_name = 'gallery'

urlpatterns = [
    path('upload/', ImageUploadView.as_view(), name='upload'),
    path('<int:pk>/', ImageDetailView.as_view(), name='image-detail'),
    path('', ImageListView.as_view(), name='image-list')
]
