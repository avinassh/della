from django.contrib.auth.models import User
from django.views.generic.edit import CreateView

from .forms import SignupForm
from . import user_service


class SignupView(CreateView):
    model = User
    form_class = SignupForm
    success_url = '/'
    template_name = 'user_manager/signup.html'

    def form_valid(self, form):
        response = super(SignupView, self).form_valid(form)
        user_service.send_activation_email(user=form.cleaned_data['email'])
        return response
