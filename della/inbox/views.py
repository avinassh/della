from django.views.generic.edit import CreateView
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import reverse, get_object_or_404
from django.db.models import Q, Max
from django.http import Http404, JsonResponse
from django.contrib.auth.models import User

from .forms import MessageCreateForm
from .models import Message, Thread
from . import inbox_service


@method_decorator(login_required, name='dispatch')
class MessageCreateView(CreateView):
    model = Message
    form_class = MessageCreateForm

    def post(self, request, pk, *args, **kwargs):
        if not request.is_ajax():
            raise Http404('Haxxeru?')
        self.thread = self._validate_and_get_thread(thread_id=pk)
        if not self.thread:
            raise Http404('Haxxeru?')
        return super().post(request, pk, *args, **kwargs)

    def form_valid(self, form):
        message = form.save(commit=False)
        message.sent_by = self.request.user
        message.thread = self.thread
        super().form_valid(form)
        response = {'status': True, 'pk': self.object.pk}
        return JsonResponse(response)

    def get_success_url(self):
        sender = self.request.user
        recipient = inbox_service.get_recipient(
            thread=self.thread, sender=sender)
        return reverse('inbox:thread-detail', args=(recipient.username,))

    def _validate_and_get_thread(self, thread_id):
        user = self.request.user
        return Thread.objects.filter(
            Q(pk=thread_id) & Q(
                Q(participant_1=user) | Q(participant_2=user))).first()


@method_decorator(login_required, name='dispatch')
class ThreadListView(ListView):
    model = Thread

    def get_queryset(self):
        user = self.request.user
        return Thread.objects.filter(Q(participant_1=user) | Q(
            participant_2=user)).annotate(
            last_message_time=Max('messages__created_on')).order_by(
                '-last_message_time')

    def get_context_data(self, **kwargs):
        sender = self.request.user
        context = super().get_context_data(**kwargs)
        object_list = []
        sneaky_list = []
        for obj in context['object_list']:
            if obj.is_sneaky:
                sneaky_list.append(self._get_sneaky_context(thread=obj))
            else:
                obj.recipient = inbox_service.get_recipient(
                    thread=obj, sender=sender)
                object_list.append(obj)
        context['object_list'] = object_list
        context['sneaky_list'] = sneaky_list
        return context

    def _get_sneaky_context(self, thread):
        sender = self.request.user
        if thread.santa == self.request.user:
            recipient = inbox_service.get_recipient(
                thread=thread, sender=sender)
            thread.title = 'Santee Messages - {}'.format(
                recipient.username)
            thread.url = reverse('inbox:santee-detail')
        else:
            thread.title = 'Santa Messages'
            thread.url = reverse('inbox:santa-detail')
        return thread


@method_decorator(login_required, name='dispatch')
class BaseThreadDetailView(DetailView):
    model = Thread
    form_class = MessageCreateForm

    def get_context_data(self, **kwargs):
        context = {}
        context['form'] = self.form_class()
        return super().get_context_data(**context)

    def _get_thread(self, participant_1, participant_2, santa=None):
        thread, _ = Thread.objects.get_or_create(
            participant_1=participant_1, participant_2=participant_2,
            is_sneaky=bool(santa), santa=santa)
        return thread


class ThreadDetailView(BaseThreadDetailView):
    """
    To render (non-sneaky) message thread between two users
    """

    def get_object(self):
        user = self.request.user
        recipient_name = self.kwargs.get('recipient')
        recipient = get_object_or_404(User, username=recipient_name)
        participant_1, participant_2 = inbox_service.get_participants(
            user_1=user, user_2=recipient)
        return self._get_thread(
            participant_1=participant_1, participant_2=participant_2)


class SantaThreadDetailView(BaseThreadDetailView):
    """
    To render message thread between logged in user and his santa
    """

    def get_object(self):
        user = self.request.user
        try:
            # user.santa is a UserProfile
            santa = user.santa.user
        except user.userprofile.DoesNotExist:
            raise Http404("You don't have a Santa. Yet ;)")
        participant_1, participant_2 = inbox_service.get_participants(
            user_1=user, user_2=santa)
        return self._get_thread(
            participant_1=participant_1, participant_2=participant_2,
            santa=santa)


class SanteeThreadDetailView(BaseThreadDetailView):
    """
    To render message thread between logged in user (santa) and his santee
    """

    def get_object(self):
        user = self.request.user
        santee = user.userprofile.santee
        if not santee:
            raise Http404("You don't have a Santee. Yet ;)")
        participant_1, participant_2 = inbox_service.get_participants(
            user_1=user, user_2=santee)
        return self._get_thread(
            participant_1=participant_1, participant_2=participant_2,
            santa=user)
