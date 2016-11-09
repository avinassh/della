from django.contrib.auth.models import User
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import UserProfile
from .forms import (SignupForm, UserProfileForm, RequestActivationCodeForm,
                    MassEmailForm)
from . import user_service
from . import draw_service
from . import activation_service
from . import email_service


class SignupView(CreateView):
    model = User
    form_class = SignupForm
    success_url = '/'
    template_name = 'generic_crispy_form_template.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        user_service.create_user_profile(user=user)
        user_service.send_activation_email(request=self.request, user=user)
        m = ('Hey {}! Your account has been created. Please check your '
             'email for account activation link.').format(user.username)
        messages.add_message(self.request, messages.SUCCESS, m)
        return redirect('/')


class ActivateView(View):

    def get(self, request, username, code):
        user = get_object_or_404(User, username=username)
        if not activation_service.validate_key(key=code, user=user):
            m = 'Activation key expired, request a new one.'
            messages.add_message(self.request, messages.ERROR, m)
            return redirect(reverse('user_manager:activate-request'))
        user_service.activate_user(user=user)
        user_service.enable_for_exchange(user=user)
        messages.add_message(self.request, messages.SUCCESS,
                             'Your email is confirmed. Please login.')
        return redirect(reverse('user_manager:login'))


class RequestActivationEmailView(FormView):
    form_class = RequestActivationCodeForm
    template_name = 'generic_crispy_form_template.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = get_object_or_404(User, email=email)
        if user.is_active:
            messages.add_message(
                self.request, messages.WARNING,
                'Account already active. Please login')
            return redirect(reverse('user_manager:login'))
        user_service.send_activation_email(request=self.request, user=user)
        messages.add_message(self.request, messages.INFO,
                             'Activation email has been sent.')
        return redirect('/')


@method_decorator(login_required, name='dispatch')
class UserProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    success_url = reverse_lazy('user_manager:account')

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


class UserProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'user_manager/userprofile_detail.html'
    template_name_santa = 'user_manager/userprofile_detail_santa.html'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(UserProfile, user__username=username)

    def render_to_response(self, context, **response_kwargs):
        if self.request.user.is_authenticated():
            # check if the logged in user has a santee
            santee = self.request.user.userprofile.santee
            if santee:
                if santee.id == self.object.user.id:
                    self.template_name = self.template_name_santa
        return super().render_to_response(context, **response_kwargs)


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
        eligible_users = User.objects.filter(
            userprofile__is_enabled_exchange=True).count()
        if eligible_users < 3:
            m = ('The number of eligible users for exchange is less')
            messages.add_message(self.request, messages.ERROR, m)
            return redirect(reverse('user_manager:draw-names'))
        if not draw_service.get_draw_status():
            draw_service.draw_names()
        users = User.objects.filter(userprofile__is_enabled_exchange=True)
        context = {}
        context['user_list'] = users
        return render(
            request=request, template_name=self.template_draw_names_done,
            context=context)


@method_decorator(staff_member_required, name='dispatch')
class MassEmailView(FormView):
    form_class = MassEmailForm
    template_name = 'user_manager/mass_email.html'

    def form_valid(self, form):
        message = form.cleaned_data['message']
        subject = form.cleaned_data['subject']
        recipients = form.cleaned_data['recipients']
        email_service.send_email(
            subject=subject, message=message, recipient_list=recipients)
        messages.add_message(self.request, messages.SUCCESS,
                             'Emails have been sent!')
        return redirect(reverse('user_manager:mass-email'))
