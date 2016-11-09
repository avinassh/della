from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Reset, Layout, Fieldset

from .models import Image


class ImageUploadForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # make description optional field
        self.fields['description'].required = False

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Upload Image',
                'title',
                'file',
                'description'
            )
        )
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = 'gallery:upload'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'
        self.helper.add_input(Reset('reset', 'Cancel'))
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Image
        fields = ['title', 'file', 'description']
