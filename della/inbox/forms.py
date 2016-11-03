from django.forms import ModelForm

from .models import Message


class MessageCreateForm(ModelForm):

    class Meta:
        model = Message
        fields = ['text']
