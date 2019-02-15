from forms import TenantForm,GetFile,match
from django.shortcuts import redirect,render
from django.http import HttpResponse,Http404,JsonResponse
from models import Client
import pandas as pd
import numpy as np
from django.db.models import F
import string
from django.conf import settings
from audtech_analytics.models import Engagement,FinalTable, Mapping
from audtech_analytics.functions import removePunct
from django.core.files.storage import FileSystemStorage
from tenant_schemas.utils import  schema_context
from django_pandas.io import read_frame
import os
from django.db.models import Sum,Count
import json
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages 

def CreateTenant(request):
    context={}
    if request.method=="GET":
        form=TenantForm()
        context['form']=form
        return render(request,'createtenant.html',context)
    elif request.method=="POST":
        form=TenantForm(request.POST)
        context['form']=form
        if form.is_valid():
            obj=Client(domain_url=(request.POST.get("domain_url")+'.audtech.com'),schema_name=request.POST.get("schema_name"))
            print(obj)
            user=User.objects.create_user(username=request.POST.get("username"),password=request.POST.get("password"))
            obj.user=user
            obj.user_id=user.id
            obj.save()
            messages.success(request,str(request.POST.get("domain_url"))+' Created Successfully ')
        else:
            messages.error(request,str(form.errors.as_text())) 
    return render(request,'createtenant.html',context)
import datetime
import dateparser
import re
def ProcessFile(request):
    with schema_context(request.session.get('schema_name')):
        context={}
        context['client']=Engagement.objects.filter(user_id=request.session.get('username'))
        context['engagment']=Engagement.objects.filter(user_id=request.session.get('username'))
        context['username']=request.session.get('username')
        context['clientname']=request.session.get('clientname')
        context['engangement']=request.session.get("engangement")
        if request.method=="GET":
            form1=GetFile(request.GET)
            context['form']=form1
            return render(request,'uploaddata.html',context)
        elif request.method=="POST":
            with schema_context(request.session.get('schema_name')):
                form=GetFile(request.POST,request.FILES)
                if form.is_valid():
                    if request.POST.get('client') != "":
                        request.session["clientname"]=request.POST.get('client')
                        request.session['engangement']=request.POST.get('engagement')
                        myfile=request.FILES['inputfile']
                        fs = FileSystemStorage(location=settings.BASE_DIR+'/filesfolder') #defaults to   MEDIA_ROOT 
                        savedfile=fs.save(myfile.name,myfile)
                        request.session['saved_file']=savedfile
                        df=pd.read_csv(settings.BASE_DIR+'/filesfolder/'+str(request.session['saved_file']))
                        df=df.rename(columns=lambda x: x.strip())
                        lscols=df.columns.tolist()          
                        time=Engagement.objects.get(engagement_name=request.POST.get('engagement'),name=request.POST.get('client'))
                        request.session['erp']=time.financial_management_system
                        df=df.fillna('0')
                        for i in lscols:
                            # if re.findall(r'(\d{1,4})[/.-](\d{1,2})[/.-](\d{1,4})|(\d{1,2})[/.-](\d{1,2})$',arg2):
                            i=i.strip()
                            try:
                                Mapping.objects.get(source_filed__iexact=i,eng=request.session.get("engangement"))
                            except Mapping.DoesNotExist:
                                return redirect('/AfterProcess')
                        mask = df.astype(str).apply(lambda x : x.str.match(r'[0-9]{2}[-|\/]{1}[0-9]{2}[-|\/]{1}[0-9]{4}').all())
                        df.loc[:,mask] = df.loc[:,mask].apply(pd.to_datetime)
                        Fo=Mapping.objects.filter(eng=request.session.get("engangement"))
                        context['Fo']=Fo
                        lscols=df.columns.tolist()
                        dicto={}
                        for idx in range(len(df.index)):
                            for i in lscols:
                                i=i.strip()
                                f=Mapping.objects.get(source_filed__iexact=i,eng=request.session.get('engangement'))
                                arg2=df[i][idx]
                                arg2=removePunct(arg2)
                                dicto[f.final_field]=arg2
                                dicto['client']=request.POST.get('client')
                                dicto['engangement']=request.POST.get('engagement')
                            FinalTable.objects.bulk_create([FinalTable(**dicto)])
                        return render(request,'process.html')
                    else:
                        myfile=request.FILES['inputfile']
                        fs = FileSystemStorage(location=settings.BASE_DIR+'/filesfolder') #defaults to   MEDIA_ROOT 
                        savedfile=fs.save(myfile.name,myfile)
                        request.session['saved_file']=savedfile
                        df=pd.read_csv(settings.BASE_DIR+'/filesfolder/'+str(request.session['saved_file']))
                        df=df.rename(columns=lambda x: x.strip())
                        df=df.round()
                        mask = df.astype(str).apply(lambda x : x.str.match(r'[0-9]{2}[-|\/]{1}[0-9]{2}[-|\/]{1}[0-9]{4}').all())
                        df.loc[:,mask] = df.loc[:,mask].apply(pd.to_datetime)
                        print(str(df.loc[:,mask])+"=====================")
                        lscols=df.columns.tolist()
                        df=df.fillna('0')
                        for i in lscols:
                            i=i.strip()
                            try:
                                Mapping.objects.get(source_filed__iexact=i,eng=request.session.get('engangement'))
                            except Mapping.DoesNotExist:
                                return redirect('/AfterProcess')
                        Fo=Mapping.objects.filter(eng=request.session.get("engangement"))
                        context['Fo']=Fo
                        dicto={}
                        for idx in range(len(df.index)):
                            for i in lscols:
                                i=i.strip()
                                f=Mapping.objects.get(source_filed__iexact=i,eng=request.session.get('engangement'))
                                arg2=df[i][idx]
                                arg2=removePunct(arg2)
                                dicto[f.final_field]=arg2
                                dicto['client']=request.session.get('clientname')
                                dicto['engangement']=request.session.get('engangement')
                            FinalTable.objects.bulk_create([FinalTable(**dicto)])
                        df=df.head(50)
                        context['frame']=df.to_html(index=False)
                        return render(request,'process.html',context)
                else:
                    context['form']=form
            return render(request,'process.html',context)

def AfterProcess(request):
    context={}
    if request.method == 'GET':
        df=pd.read_csv(settings.BASE_DIR+'/filesfolder/'+str(request.session['saved_file']))
        df=df.head(10)
        context['username']=request.session.get('username')
        context['frame']=df.to_html(index=False,classes='')
        context['eng']=request.session.get("engangement")
        context['clientname']=request.session.get("clientname")
        context['erp']=request.session.get('erp')
        count=pd.DataFrame(df.columns)
        context['count']=count.values.tolist()
        return render(request,'buttons.html',context)
    if request.method=='POST':
        with schema_context(request.session.get('schema_name')):
            if request.POST.get('done'):
                return redirect('/UpdateMappiing')
            else:
                df=pd.read_csv(settings.BASE_DIR+'/filesfolder/'+str(request.session['saved_file']))
                df=df.rename(columns=lambda x: x.strip())
                count=pd.DataFrame(df.columns)
                context['count']=count.values.tolist()
                for i ,j in zip(range(len(df.columns)),range(1,len(df.columns)+1)):
                    Mapping.objects.create(source_filed=df.columns[i],final_field=(request.POST.get('C'+str(j))).replace(' ',''),column_no=df.columns[i],eng=request.session.get('engangement'))
                lscols=df.columns.tolist() 
                for i in lscols:
                    try:
                        Mapping.objects.get(source_filed__iexact=i,eng=request.session.get("engangement"))
                        return redirect('/EndProcess')
                    except Mapping.DoesNotExist:
                        return HttpResponse(str(i))
        return render(request,'buttons.html',context)
def EndProcess(request):
    with schema_context(request.session.get('schema_name')):
        context={}
        Fo=Mapping.objects.filter(eng=request.session.get("engangement"))
        context['Fo']=Fo
        df=pd.read_csv(settings.BASE_DIR+'/filesfolder/'+ str(request.session.get('saved_file')))
        mask = df.astype(str).apply(lambda x : x.str.match(r'[0-9]{2}[-|\/]{1}[0-9]{2}[-|\/]{1}[0-9]{4}').all())
        df=df.fillna('0')
        df=df.head(50)
        df.loc[:,mask] = df.loc[:,mask].apply(pd.to_datetime)
        df=df.rename(columns=lambda x: x.strip())
        lscols=df.columns.tolist()
        dicto={}
        for idx in range(len(df.index)):
            for i in lscols:
                i=i.strip()
                f=Mapping.objects.get(source_filed__iexact=i,eng=request.session.get('engangement'))
                arg2=df[i][idx]
                arg2=removePunct(arg2)
                dicto[f.final_field]=arg2
                dicto['client']=request.session.get('clientname')
                dicto['engangement']=request.session.get('engangement')
            FinalTable.objects.bulk_create([FinalTable(**dicto)])
        df=df.head(50)
        context['frame']=df.to_html(index=False)
        return render(request,'process.html',context)
# def UpdateMapping(request):
#     context={}
#     if request.method == 'GET':
#         form=match()
#         df=pd.read_csv(settings.BASE_DIR+'/filesfolder/'+str(request.session['saved_file']))
#         df=df.head(5)
#         context['username']=request.session.get('username')
#         context['frame']=df.to_html(index=False,classes='')
#         context['eng']=request.session.get("engangement")
#         context['clientname']=request.session.get("clientname")
#         context['erp']=request.session.get('erp')
#         count=pd.DataFrame(df.columns)
#         context['count']=count.values.tolist()
#         context['form']=form
#         return render(request,'UpdateMapping.html',context)
#     if request.method=='POST':
#         with schema_context(request.session.get('schema_name')):    
#             df=pd.read_csv(settings.BASE_DIR+'/filesfolder/'+str(request.session['saved_file']))
#             count=pd.DataFrame(df.columns)
#             context['count']=count.values.tolist()
#             for i ,j in zip(range(len(df.columns)),range(1,len(df.columns)+1)):
#                 Mapping.objects.update(source_filed=df.columns[i],final_field=request.POST.get('C'+str(j)),column_no=df.columns[i]).filter(eng=request.session.get('engangement'))
#             lscols=df.columns.tolist()               
#             columnnames=[i for i in lscols ]
#             for i in columnnames:
#                 try:
#                     Mapping.objects.get(source_filed__iexact=i,eng=request.session.get('engangement'))
#                     return redirect('/EndProcess')
#                 except Mapping.DoesNotExist:
#                     return HttpResponse(str(i))
#     return render(request,'UpdateMapping.html',context)
