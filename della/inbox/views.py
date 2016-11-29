from django.views.generic.edit import CreateView
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import reverse, get_object_or_404
from django.db.models import Q, Max
from django.http import Http404, JsonResponse
from django.contrib.auth.models import User
from django.utils.formats import date_format

from .forms import MessageCreateForm
from .models import Message, Thread
from . import inbox_service
from . import tasks


@method_decorator(login_required, name='dispatch')
class MessageCreateView(CreateView):
    model = Message
    form_class = MessageCreateForm
    success_url = '/'

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
        response = self._get_response()
        base_site_url = self.request.build_absolute_uri('/')
        tasks.send_email_notification(
            message_id=self.object.id, base_site_url=base_site_url)
        return JsonResponse(response)

    def _validate_and_get_thread(self, thread_id):
        user = self.request.user
        return Thread.objects.filter(
            Q(pk=thread_id) & Q(
                Q(participant_1=user) | Q(participant_2=user))).first()

    def _get_response(self):
        timestamp = date_format(self.object.created_on, 'DATETIME_FORMAT')
        data = {
            'text': self.object.text,
            'signature': "{} | {}".format(self.object.sent_by.username,
                                          timestamp),
        }
        return {'status': True, 'data': data}


@method_decorator(login_required, name='dispatch')
class ThreadListView(ListView):
    model = Thread

    def get_queryset(self):
        user = self.request.user
        return Thread.objects.prefetch_related('messages').filter(
            Q(participant_1=user) | Q(participant_2=user)).annotate(
            last_message_time=Max('messages__created_on')).order_by(
                '-last_message_time')

    def get_context_data(self, **kwargs):
        sender = self.request.user
        context = super().get_context_data(**kwargs)
        object_list = []
        sneaky_list = []
        for obj in context['object_list']:
            try:
                obj.latest_message = obj.messages.latest('created_on')
            except Message.DoesNotExist:
                continue
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
        if thread.santa == self.request.user:
            thread.title = 'Santee Messages'
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
        context['thread_messages'] = self.object.messages.all()
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
        thread = self._get_thread(
            participant_1=participant_1, participant_2=participant_2)
        thread.recipient = recipient_name
        return thread


class SantaThreadDetailView(BaseThreadDetailView):
    """
    To render message thread between logged in user and his santa
    """

    template_name = 'inbox/thread_detail_sneaky.html'

    def get_object(self):
        user = self.request.user
        try:
            # user.santa is a UserProfile
            self.santa = user.santa.user
        except user.userprofile.DoesNotExist:
            raise Http404("You don't have a Santa. Yet ;)")
        participant_1, participant_2 = inbox_service.get_participants(
            user_1=user, user_2=self.santa)
        thread = self._get_thread(
            participant_1=participant_1, participant_2=participant_2,
            santa=self.santa)
        thread.recipient = 'Santa'
        return thread

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for message in context['thread_messages']:
            if message.sent_by == self.santa:
                message.sent_by.username = 'Santa'
        return context


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
        thread = self._get_thread(
            participant_1=participant_1, participant_2=participant_2,
            santa=user)
        thread.recipient = "{} (Santee)".format(santee.username)
        return thread
