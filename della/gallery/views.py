from django.views.generic.edit import CreateView
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import reverse

from .models import Image
from .forms import ImageUploadForm


@method_decorator(login_required, name='dispatch')
class ImageUploadView(CreateView):
    model = Image
    form_class = ImageUploadForm
    template_name = 'generic_crispy_form_template.html'

    def form_valid(self, form):
        image = form.save(commit=False)
        image.added_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('gallery:image-detail', args=(self.object.id,))


class ImageDetailView(DetailView):
    model = Image


class ImageListView(ListView):
    model = Image

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-created_on')
