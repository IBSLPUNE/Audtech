from django.shortcuts import render,redirect,get_object_or_404,reverse
from customers.models import Mapping
from audtech_analytics.models import Engagement,FinalTable,CompanyInfo
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import permission_required
import pandas as pd
import pdfkit 
from django.conf import settings
from django_pandas.io import read_frame
from django.contrib.auth.models import Permission,Group
from customers.forms import EngagementForm,ERPform,CreateUserForm,companyinfo
from django.db.models.functions import Cast
from tenant_schemas.utils import schema_context
from django.contrib import messages 
# Create your views here.

def main_page(request):
    return render(request,'index2.html')
def PermissionDenied(request):
    return render(request,'PermissionDenied.html')
# def form(request):
#      return render(request,'alertcreated.html')
def CompanyInformation(request):
    context={}
    if request.method == 'GET':
        form = companyinfo()
        context['form']=form
        return render(request,'companyinfo.html',context)
    elif request.method =="POST":
        with schema_context(request.session.get('schema_name')):
            form = companyinfo(request.POST)
            if form.is_valid():
                New=form.save(commit=False)
                New.user_id=request.session.get('username')
                New.save()
                return redirect('/home')
            else:
                messages.error(request,str(form.errors.as_text()))
    return render(request,'companyinfo.html',context)

def navbar(request):
    context={}
    context['username']=request.session.get('username')
    context['customer']=request.session.get('schema_name')
    return render(request,'nav.html',context)
def handler404(request):
    return render(request, '404.html', status=404)
def handler500(request):
    return render(request, '404.html', status=404)
def DisplayData(request):
    context={}
    if request.method=="GET":      
      with schema_context(request.session.get('schema_name')):  
        context['objects']=(pd.DataFrame(read_frame(FinalTable.objects.all()))).to_html()
        return render(request,'showdata.html',context)
def pdfconvertor(request):
    pdfkit.from_url(settings.BASE_DIR+'/templates/'+'analytics.html', 'out.pdf')
    return HttpResponse("'out.pdf'")
def Home(request):
    context={}
    context['clientname']=request.session.get('clientname')
    context['username']=request.session.get('username')
    context['customer']=request.session.get('schema_name')
    context['engangement']=request.session.get('engangement')
    context['username']=request.session.get('username')
    context['customer']=request.session.get('schema_name')
    with schema_context(request.session.get('schema_name')):
        details=Engagement.objects.filter(user_id=request.session.get('username'))
        context['details']=details
        return render(request,'home.html',context)
def Home2(request):
    context={}
    context['clientname']=request.session.get('clientname')
    context['username']=request.session.get('username')
    context['customer']=request.session.get('schema_name')
    context['engangement']=request.session.get('engangement')
    context['username']=request.session.get('username')
    context['customer']=request.session.get('schema_name')
    with schema_context(request.session.get('schema_name')):
        details=User.objects.all()
        context['details']=details
        return render(request,'home2.html',context)
#     return render(request,'NewClient.html',context)
def ERPMap (request):
    context={}
    context['engangement']=request.session.get("engangement")
    context['username']=request.session.get('username')
    context['customer']=request.session.get('schema_name')
    if request.method == 'GET':
        form = ERPform()
        context['form']=form
        return render(request,'ERPForm.html',context)
    elif request.method =='POST':
        form = ERPform(request.POST,request.FILES)
        print(form)
        if form.is_valid():
            #obj=form.save(commit=False)
            form=ERPform()
            context['form']=form
            obj=Mapping.objects.create(source_filed=request.POST.get("source_filed"),final_field=request.POST.get("final_field"),transaction_type=request.POST.get("transaction_type"),erp=request.POST.get("erp"))
            data=Mapping.objects.filter(erp=request.POST.get('erp'))
            context['data']=data
            return render(request,'ERPForm.html',context)
        else:
            context['form']=form
    return render(request,'ERPForm.html',context)

from django.views.generic.edit import UpdateView
def CreateUser (request):
    context={}
    context['username']=request.session.get('username')
    context['customer']=request.session.get('schema_name')
    context['clientname']=request.session.get("clientname")
    if request.method == 'GET':
        with schema_context(request.session.get('schema_name')):
            form = CreateUserForm()
            context['form']=form
            return render(request,'createuser.html',context)
    elif request.method == 'POST':
        with schema_context(request.session.get('schema_name')):
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user=form.save(commit=False)
                # user.refresh_from_db()
                user.save()
                # group=Group.objects.get(id=request.POST.get('groups'))
                print(str(request.POST.getlist('user_permissions')))
                for i in request.POST.getlist('user_permissions'):
                    permission = Permission.objects.get(name =i)
                    # group.permissions.add(permission)
                    user = User.objects.get(username=request.POST.get('username'))
                    user.user_permissions.add(permission)
                    user=user.id
                    # group.user_set.add(user)
                return redirect('/home')
            else:
                messages.error(request,str(form.errors.as_text()))   
    return render(request,'createuser.html',context)
    
# @permission_required("audtech_analytics.add_engagement",login_url='/PermissionDenied')
def EngagementDATA(request):
    context={}
    context['username']=request.session.get('username')
    context['customer']=request.session.get('schema_name')
    if request.method == 'GET':
        with schema_context(request.session.get('schema_name')):
            form = EngagementForm()
            context['form']=form
            return render(request,'NewClient.html',context)
    elif request.method =='POST':
        with schema_context(request.session.get('schema_name')):
            form = EngagementForm(request.POST,request.FILES)
            if form.is_valid():
                obj=form.save(commit=False)
                request.session["engangement"]=request.POST.get("engagement_name")
                request.session["clientname"]=request.POST.get('name')
                request.session["start_month"]=request.POST.get('fiscal_start_month').strip('/')
                request.session["end_month"]=request.POST.get('fiscal_end_month').strip('/')
                request.session["erp"]=request.POST.get("financial_management_system")
                obj.user_id=request.session.get('username')
                obj.save()
                user=User.objects.get(username=request.session['username'])
                if user.has_perm("is_import"):
                    return redirect('/processfile')
                else:
                    return redirect("/home")
            else:
                context['form']=form
    return render(request,'NewClient.html',context)


