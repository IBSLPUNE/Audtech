from forms import TenantForm,GetFile
from django.shortcuts import render
from django.http import HttpResponse
from models import Client
import pandas as pd
from django.conf import settings
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
            
from customers.models import FinalTable,Mapping
from django.core.files.storage import FileSystemStorage
import os
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
            fs = FileSystemStorage(location=settings.BASE_DIR+'/filesfolder') #defaults to   MEDIA_ROOT 
            savedfile=fs.save(myfile.name,myfile) 
            df=pd.read_csv(settings.BASE_DIR+'/filesfolder/'+savedfile)
            lscols=df.columns.tolist()
            lscols.pop()
            columnnames=[i for i in lscols]
            pairs=[]
            print(request.POST.get("erp"))
            for i in columnnames:
                try:
                    f=Mapping.objects.get(source_filed__iexact=i,erp=request.POST.get("erp"))
                    pairs.append((i,f.final_field.lower()))
               
                except Mapping.DoesNotExist:
                    os.remove(settings.BASE_DIR+'/filesfolder/'+savedfile)
                    return HttpResponse(i + ' column in file has error give right column name according to mapping.' )
            for idx in range(0,len(df)):
                obj=FinalTable()
                for x in pairs: 
                    exec("obj.%s = '%s'" %(x[1],df[x[0]][idx]))
                obj.save()
            os.remove(settings.BASE_DIR+'/filesfolder/'+savedfile)
            return HttpResponse(df.to_string())




        
