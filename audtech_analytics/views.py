from django.shortcuts import render,redirect
from customers.models import Mapping
from audtech_analytics.models import FinalTable
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from customers.forms import ClientForm,EngagementForm,ERPform,CreateUserForm
from audtech_analytics.models import EndClient,Engagement
import pandas as pd
from django.db.models import Count
from tenant_schemas.utils import schema_context
# Create your views here.
# def form(request):
#     return render(request,'form.html')
def navbar(request):
    context={}
    context['username']=request.session.get('username')
    context['customer']=request.session.get('schema_name')
    return render(request,'nav.html',context)
def handler404(request):
    return render(request, '404.html', status=404)

def DisplayData(request):
    context={}
    if request.method=="GET":      
      with schema_context(request.session.get('schema_name')):  
        context['objects']=FinalTable.objects.all()
        return render(request,'showdata.html',context)

"""CreateUserForm
class ClieCreateUserFormntRegister(FormView):
    with sCreateUserFormchema_context('testtest'):
        foCreateUserFormrm_class=ClientForm
        teCreateUserFormmplate_name="NewClient.html"
        suCreateUserFormccess_url="/ERPMap"
"""
def ClientRegister(request):
    context={}
    context['username']=request.session.get('username')
    context['customer']=request.session.get('schema_name')
    if request.method == 'GET':
      with schema_context(request.session.get('schema_name')):
        form = ClientForm()
        context['form']=form
        return render(request,'NewClient.html',context)
    elif request.method == 'POST':
      with schema_context(request.session.get('schema_name')):
        request.session['clientname']=request.POST.get("name")
        form = ClientForm(request.POST,request.FILES)
        print(form)
        if EndClient.object.get(name=request.POST.get("name").exist()):
            return HttpResponse("Dusra Namm Ki comapny do bhiya")
        if form.is_valid():
            form.save()
            return redirect("/Engagement")
        else:
            context['form']=form 
            return render(request,'NewClient.html',context)         
    else:
        form=ClientForm()
    return render(request,'NewClient.html')
def ERPMap (request):
    context={}
    context['username']=request.session.get('username')
    context['customer']=request.session.get('schema_name')
    if request.method == 'GET':
        form = ERPform()
        context['form']=form
        data=Mapping.objects.filter(erp=request.POST.get('erp'))
        context['data']=data
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
        else:
            context['form']=form
    return render(request,'ERPForm.html',context)

from tenant_schemas.utils import schema_context

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
            form = CreateUserForm(request.POST,request.FILES)
            print(form)
            if form.is_valid():
                obj=form.save(commit=False)
                # Engagement.objects.create(endclient=EC)
                obj.save()
                return HttpResponse("hogya BHai")
            else:
                context['form']=form
                return render(request,'createuser.html',context)
def EngagementDATA(request,):
    # EC=EndClient.objects.filter(pk=pk)
    context={}
    context['username']=request.session.get('username')
    context['customer']=request.session.get('schema_name')
    context['clientname']=request.session.get("clientname")
    if request.method == 'GET':
        with schema_context(request.session.get('schema_name')):
            form = EngagementForm()
            context['form']=form
            return render(request,'NewClient.html',context)
    elif request.method =='POST':
        with schema_context(request.session.get('schema_name')):
            form = EngagementForm(request.POST,request.FILES)
            print(form)
            if form.is_valid():
                obj=form.save(commit=False)
                request.session["engangement"]=request.POST.get("engagement_name")
                # Engagement.objects.create(endclient=EC)
                obj.save()
                return redirect('/processfile')
            else:
                context['form']=form
                return render(request,'NewClient.html',context)

def ClientTable(request):
    context={}
    context['username']=request.session.get('username')
    context['customer']=request.session.get('schema_name')
    with schema_context(request.session.get('schema_name')):
        data = EndClient.objects.all()
        context['data'] =data
        return render(request,'ClientTable.html',context)

@login_required
def AnalyticsBoard(request):
    context={}
    context['filename']=request.session.get('filename')
    context['username']=request.session.get('username')
    context['customer']=request.session.get('schema_name')
    context['engangement']=request.session.get("engangement")
    # context['transaction']=request.session.get("transaction")
    if request.method=="GET":      
      with schema_context(request.session.get('schema_name')):  
        context['dataset']=FinalTable.objects\
        .values('acct_category')\
        .annotate(survived_count=Count('status_op_posted_unposted'),not_survived_count=Count('type_regular'))
        return render(request,'analytics.html',context)
    # context['debit']=request.session.get("debit")

                       
        # context['credit']=request.session.get("credit"]  