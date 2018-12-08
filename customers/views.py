from forms import TenantForm,GetFile
from django.shortcuts import render
from django.http import HttpResponse
from models import Client
import pandas as pd
def CreateTenant(request):
    context={}
    if request.method=="GET":
        form=TenantForm()
        context['form']=form
        return render(request,'createtenant.html',context)
    elif request.method=="POST":
        form=TenantForm(request.POST)
        if form.is_valid():
            obj=Client(domain_url=request.POST.get("domain_url"),schema_name=request.POST.get("schema_name"),
            name=request.POST.get("name"),description=request.POST.get("description"))
            obj.save()
            return HttpResponse("Tenant " + request.POST.get("name") + " is created")
            

def ProcessFile(request):
    context={}
    if request.method=="GET":
        form=GetFile()
        context['form']=form
        return render(request,'createtenant.html',context)

    elif request.method=="POST":
        form=GetFile(request.POST,request.FILES)
        if form.is_valid():
            myfile=request.FILES['inputfile']
            df=pd.read_csv(myfile)
            lscols=df.columns.tolist()
            lscols.pop()
            return HttpResponse(df.to_string())

            

        
