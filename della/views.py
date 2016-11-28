from django.views.generic.base import TemplateView

from della.user_manager.forms import SignupForm


class HomePageView(TemplateView):

    template_name = 'home.html'
    template_name_authenticated = 'home_authenticated.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            self.template_name = self.template_name_authenticated
            return context
        context['form'] = SignupForm()
        return context
