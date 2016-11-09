from django.views.generic.base import TemplateView

from della.user_manager.forms import SignupForm


class HomePageView(TemplateView):

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SignupForm()
        return context
