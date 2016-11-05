from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy

from .models import UserProfile
from .forms import SignupForm, UserProfileForm
from . import user_service


class SignupView(CreateView):
    model = User
    form_class = SignupForm
    success_url = '/'
    template_name = 'user_manager/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        user_service.send_activation_email(user=form.cleaned_data['email'])
        return response


@method_decorator(login_required, name='dispatch')
class UserProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    success_url = reverse_lazy('user_manager:update')

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def get_initial(self):
        form_data = super().get_initial()
        form_data['first_name'] = self.object.user.first_name
        form_data['last_name'] = self.object.user.last_name
        return form_data

    def form_valid(self, form):
        if 'last_name' in form.changed_data or (
                'first_name' in form.changed_data):
            self.object.user.first_name = form.cleaned_data['first_name']
            self.object.user.last_name = form.cleaned_data['last_name']
            self.object.user.save()
        response = super().form_valid(form)
        return response
