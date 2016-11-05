from django.contrib.auth.models import User
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render

from .models import UserProfile
from .forms import SignupForm, UserProfileForm
from . import user_service
from . import draw_service


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


@method_decorator(staff_member_required, name='dispatch')
class DrawNamesView(View):

    template_draw_names = 'user_manager/draw_names.html'
    template_draw_names_done = 'user_manager/draw_names_done.html'

    def get(self, request):
        draw_status = draw_service.get_draw_status()
        users = User.objects.filter(userprofile__is_enabled_exchange=True)
        context = {}
        context['draw_status'] = draw_status
        context['user_list'] = users
        template = self.template_draw_names_done if (
            draw_status) else self.template_draw_names
        return render(
            request=request, template_name=template, context=context)

    def post(self, request):
        if not draw_service.get_draw_status():
            draw_service.draw_names()
        users = User.objects.filter(userprofile__is_enabled_exchange=True)
        context = {}
        context['user_list'] = users
        return render(
            request=request, template_name=self.template_draw_names_done,
            context=context)
