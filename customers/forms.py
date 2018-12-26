from django import forms
from models import Client
from django.contrib.auth.models import User
from audtech_analytics.models import EndClient,Engagement
from customers.models import Mapping
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


#add login required to required views

class TenantForm(forms.ModelForm):
    email=forms.EmailField( required=False,label='Your Email')
    ls=(("Manfacturing","Manfacturing"),
       ("Audit Firm","Audit Firm"))
    Country_list=(('India','India'),('USA','USA'))
    Company_Choice=forms.ChoiceField( choices=ls,required=False,label='What does your organization do? ')
    Country=forms.ChoiceField( choices=Country_list, required=False,label="Choose Country")
    Curr=(('INR','INR'),('USD','USD'))
    currency=forms.ChoiceField(label='Currency', choices=Curr, required=False)
    class Meta:
        model = Client
        fields = '__all__'
        exclude=['user','schema_name']

    def __init__(self, *args, **kwargs):
        super(TenantForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["username"]=forms.CharField(required=True,label='Your Name')
        self.fields["domain_url"]=forms.CharField(label="Your Site Name",required=False)
        self.helper.form_class = 'Shounak'
        self.helper.form_id= 'form_id'
        self.fields["password"]=forms.CharField(widget=forms.PasswordInput,required=True)
        self.fields["name"]=forms.CharField(required=True,label="Company Name")
        self.helper.add_input(Submit('submit', 'Signup', css_class='btn-primary',css_id='submit'))
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
        self.helper.add_input(Submit('submit', 'Process', css_class='btn btn-primary js-upload-photos',css_id='submit_it'))
        self.helper.form_method = 'POST'

class ClientForm(forms.ModelForm):
    
    class Meta:
        model = EndClient
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'Shounak'
        self.helper.add_input(Submit('submit', 'Create Client', css_class='btn-primary'))
        self.helper.form_method = 'POST'
class CreateUserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Create User', css_class='btn-primary'))
        self.helper.form_method = 'POST'

class EngagementForm(forms.ModelForm):

    class Meta:
        model = Engagement
        fields= '__all__'   
    def __init__(self, *args, **kwargs):
        super(EngagementForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'Shounak'
        self.helper.add_input(Submit('submit', 'Create Enagagements', css_class='btn-primary'))
        self.helper.form_method = 'POST'