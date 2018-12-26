from forms import TenantForm,GetFile
from django.shortcuts import redirect,render
from django.http import HttpResponse,Http404,JsonResponse
from models import Client
import pandas as pd
from django.conf import settings
from customers.models import Mapping
from audtech_analytics.models import FinalTable
from django.core.files.storage import FileSystemStorage
from tenant_schemas.utils import  schema_context
import os
from django.db.models import Sum,Count
import json
from django.contrib.auth.models import User

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
            obj=Client(domain_url=(request.POST.get("domain_url")+'.audtech.com'),schema_name=request.POST.get("domain_url"))
            print(obj)
            user=User.objects.create_user(username=request.POST.get("username"),password=request.POST.get("password"))
            obj.user=user
            obj.user_id=user.id
            obj.save()
            return HttpResponse("Tenant " + request.POST.get("name") + " is created")
        else:
            return render(request,'createtenant.html',context)
  
def ProcessFile(request):
    context={}
    schema_context(request.session.get('schema_name'))
    context['clientname']=request.session.get('clientname')
    if request.method=="GET":
        form=GetFile()
        context['form']=form
        return render(request,'uploaddata.html',context)

    elif request.method=="POST":
       with schema_context(request.session.get('schema_name')):
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
                print(i)
                try:
                    f=Mapping.objects.get(source_filed__iexact=i,erp=request.POST.get("erp"))
                    pairs.append((i,f.final_field.lower()))
                except Mapping.DoesNotExist:
                    os.remove(settings.BASE_DIR+'/filesfolder/'+savedfile)
                    return HttpResponse(str(i) + 'is not in Audtech System.' )
            for idx in range(0,len(df)):
                obj=FinalTable()
                for x in pairs: 
                    arg2=df[x[0]][idx]
                    try:
                        arg2.replace("'","")
                    except:
                        pass
                    if x[1]=="engangement":
                        obj.engangement=request.session.get("engagement_name")
                        continue
                    exec("obj.%s = '%s'" %(x[1],arg2))
                obj.save()
                # data = {'is_valid': True}
                # dump = json.dumps(data)
            os.remove(settings.BASE_DIR+'/filesfolder/'+savedfile)
            request.session['filename']=savedfile
            # request.session['dataset']=data1
            request.session['transaction']=df.shape[0]
            engs=FinalTable.objects.values_list('engangement',flat = True).distinct()
            FinalTable.objects.create(client=request.session.get('clientname'),
            engangement=request.session.get("engagement_name"),user_id=request.session.get('username'))
            # dataset=FinalTable.objects \
            #            .values('acct_category')\
            #            .annotate(survivd_count=Count('status_op_posted_unposted'),not_survived_count=Count('type_regular'))
            # request.session['dataset']=dataset
            #request.session['engagement']=list(engs.pop())
            # df column name sum function ---- request.session['debit']= FinalTable.objects.aggregate(Sum('dr_gl_curr_code')).values()[0]
            #df column name sum function ---- request.session['debit']= FinalTable.objects.aggregate(Sum('dr_gl_curr_code')).values()[0]
            #df column name sum function ---- request.sesson['credit']= FinalTable.objects.aggregate(Sum('cr_gl_curr_code')).values()[0]
            # return JsonResponse(data)
            return render(request,'buttons.html',{'frame':df.to_html()})