from django import forms
from models import Client
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class TenantForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TenantForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Create Tenant', css_class='btn-primary'))
        self.helper.form_method = 'POST'


class GetFile(forms.Form):
    inputfile = forms.FileField()
    
    def __init__(self, *args, **kwargs):
        super(GetFile, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Process', css_class='btn-primary'))
        self.helper.form_method = 'POST'
