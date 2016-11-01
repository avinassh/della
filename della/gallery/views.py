from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Image


@method_decorator(login_required, name='dispatch')
class ImageUploadView(CreateView):
    model = Image
    success_url = '/'
    fields = ['file', 'title', 'description']

    def form_valid(self, form):
        image = form.save(commit=False)
        image.added_by = self.request.user
        return super(ImageUploadView, self).form_valid(form)


class ImageDetailView(DetailView):
    model = Image
