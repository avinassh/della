from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import reverse
from django.db.models import Q
from django.http import Http404


from .models import Message, Thread


@method_decorator(login_required, name='dispatch')
class MessageCreateView(CreateView):
    model = Message
    fields = ['text']

    def post(self, request, pk, *args, **kwargs):
        self.thread = self._validate_and_get_thread(thread_id=pk)
        if not self.thread:
            raise Http404('Haxxeru?')
        return super(MessageCreateView, self).post(
            request, pk, *args, **kwargs)

    def form_valid(self, form):
        message = form.save(commit=False)
        message.sent_by = self.request.user
        message.thread = self.thread
        return super(MessageCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('gallery:image-detail', args=(self.object.id,))

    def _validate_and_get_thread(self, thread_id):
        user = self.request.user
        return Thread.objects.filter(
            Q(pk=thread_id) & Q(
                Q(participant_1=user) | Q(participant_2=user))).first()
