from django import forms
from models import Client
from audtech_analytics.models import EndClient,Engagement
from customers.models import Mapping
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


#add login required to required views

class TenantForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = '__all__'
        exclude=['user']

    def __init__(self, *args, **kwargs):
        super(TenantForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["username"]=forms.CharField(required=True)
        self.fields["password"]=forms.CharField(widget=forms.PasswordInput,required=True)
        self.fields["name"]=forms.CharField(required=True)
        self.helper.add_input(Submit('submit', 'Create Tenant', css_class='btn-primary'))
        self.helper.form_method = 'POST'
class ERPform(forms.ModelForm):
    class Meta:
        model = Mapping
        exclude = ('final_field',)

    def __init__(self, *args, **kwargs):
        super(ERPform, self).__init__(*args, **kwargs)
        uq=Mapping.objects.values_list('final_field',flat=True).distinct()
        last=[]
        for i in uq:
            last.append((i,i))
        self.fields['final_field']=forms.ChoiceField( choices=last,label="Audtech Field")
        self.helper = FormHelper()
        # self.helper.form_class = 'blueForms'
        self.helper.add_input(Submit('submit', 'Save', css_class='btn-primary'))
        self.helper.form_method = 'POST'

class GetFile(forms.Form):
    inputfile = forms.FileField()
    
    def __init__(self, *args, **kwargs):
        super(GetFile, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        uq=Mapping.objects.values_list('erp',flat=True).distinct()
        last=[]
        for i in uq:
            last.append((i,i))
        self.fields['erp']= forms.ChoiceField(choices=last,label="Financial System")
        self.helper.add_input(Submit('submit', 'Process', css_class='btn-primary'))
        self.helper.form_method = 'POST'

class ClientForm(forms.ModelForm):
    
    class Meta:
        model = EndClient
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Create Client', css_class='btn-primary'))
        self.helper.form_method = 'POST'

class EngagementForm(forms.ModelForm):

    class Meta:
        model = Engagement
        fields= '__all__'   
    def __init__(self, *args, **kwargs):
        super(EngagementForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Create Enagagements', css_class='btn-primary'))
        self.helper.form_method = 'POST'