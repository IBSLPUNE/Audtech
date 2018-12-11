from django.shortcuts import render,redirect
from customers.models import FinalTable,Mapping
from django.http import HttpResponse
from django.views.generic.edit import FormView
from customers.forms import ClientForm,EngagementForm,ERPform
from audtech_analytics.models import EndClient,Engagement
import pandas as pd
from tenant_schemas.utils import schema_context
# Create your views here.
def DisplayData(request):
    context={}
    if request.method=="GET":
        context['objects']=FinalTable.objects.all()
        return render(request,'showdata.html',context)
"""
class ClientRegister(FormView):
    with schema_context('testtest'):
        form_class=ClientForm
        template_name="NewClient.html"
        success_url="/ERPMap"
"""
def ClientRegister(request):
    context={}
    if request.method == 'GET':
      with schema_context('testtest'):
        form = ClientForm()
        context['form']=form
        return render(request,'NewClient.html',context)
    elif request.method == 'POST':
      with schema_context('testtest'):
        request.session['clientname']=request.POST.get("name")
        form = ClientForm(request.POST,request.FILES)
        print(form)
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
    if request.method == 'GET':
        form = ERPform()
        context['form']=form
        data=Mapping.objects.filter(erp=request.POST.get('erp'))
        context['data']=data
            
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

from tenant_schemas.utils import schema_context

def EngagementDATA(request,):
    # EC=EndClient.objects.filter(pk=pk)
    context={}
    context['clientname']=request.session.get("clientname")
    if request.method == 'GET':
        with schema_context('testtest'):
            form = EngagementForm()
            context['form']=form
            return render(request,'NewClient.html',context)
    elif request.method =='POST':
        with schema_context('testtest'):
            form = EngagementForm(request.POST,request.FILES)
            print(form)
            if form.is_valid():
                obj=form.save(commit=False)
                # Engagement.objects.create(endclient=EC)
                obj.save()
                return redirect('/processfile')
            else:
                context['form']=form
                return render(request,'NewClient.html',context)

def ClientTable(request):
    data = EndClient.objects.all()
    Context = { 'data':data }
    return render(request,'ClientTable.html',Context)
def AnalyticsBoard(request):
    return render(request,'analytics.htmlchartjs cdn')