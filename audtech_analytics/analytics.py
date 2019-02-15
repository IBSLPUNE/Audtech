from django.shortcuts import render,redirect
from audtech_analytics.models import FinalTable
from customers.forms import FinalTableFilter
from django.http import HttpResponse
from audtech_analytics.models import Engagement
import pandas as pd
import numpy as np
from django.contrib.auth.decorators import login_required
from django_pandas.io import read_frame
from django.contrib.auth.decorators import permission_required
from django.db.models.functions import Cast
from django.db.models import Count,Case, CharField, Value, When,Max,Q,F,Sum,FloatField
from tenant_schemas.utils import schema_context
from audtech_analytics.functions import missing_values
from django.contrib import messages
from django.db.models.functions import Length
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
from django.db.models.functions import Extract,TruncMonth,ExtractMonth
from django.core.paginator import Paginator

# @permission_required('audtech_analytics.is_analytics',login_url='/PermissionDenied')
def AnalyticsBoard(request):
    filename =request.session.get('saved_file')
    clientname =request.session.get('clientname')
    engangement =request.session.get('engangement')
    context={}
    context['filename']=filename
    context['clientname']=clientname
    context['username']=request.session.get('username')
    context['customer']=request.session.get('schema_name')
    context['engangement']=engangement
    with schema_context(request.session.get('schema_name')):
            # ===========================================================================
                                    # charts
            context['dataset']=FinalTable.objects\
             .filter(client=clientname,engangement=engangement)\
            .values('AccountCategory')\
            .annotate(survived_count=Count('StatusPostedUnposted'),not_survived_count=Count('JournalType'))
            # ====================================================================
                                 #''' Missing Values '''
            obj=FinalTable.objects.filter(client=clientname,engangement=engangement).order_by('SrNo')
            context['transaction']=obj.count()
            # print('========'+str(engangement))
            qs=read_frame(obj)
            df=pd.DataFrame(qs).drop(['client','engangement','user_id','Upload_Date','id'], axis=1)
            # ========================================================================================
            # =============================================================================
            df['SrNo']=df['SrNo'].astype(float)
            dcf=pd.DataFrame(missing_values(df['SrNo']))
            dcf=dcf.count()
            context['missing']=dcf.to_csv(index=False)
            # ==============================================================================
                     # ''' Top users number of entries / value '''
            JE=FinalTable.objects\
                .filter(client=clientname,engangement=engangement)\
                .values('CreatedBy')\
                .annotate(JE=Count('CreatedBy'))\
                .annotate(Credit=Cast('CreditAmount', FloatField()),Debit=Cast('DebitAmount', FloatField()))\
                .annotate(Credit=Sum('Credit'),Debit=Sum('Debit'))
            context['JEuser']=JE
            # ==================================================================================
             # ''' Posted / Un posted - Authorised / Un Authorised JE '''
            posted_unposted=FinalTable.objects\
             .filter(client=clientname,engangement=engangement)\
            .values('StatusPostedUnposted')\
            .annotate(Credit=Cast('CreditAmount', FloatField()),Debit=Cast('DebitAmount', FloatField()))\
            .annotate(posted_unposted=Count('StatusPostedUnposted'),Credit=Sum('Credit'),Debit=Sum('Debit'))
            context['pos_unpos']=posted_unposted
            # =======================================================================================
            # '''Manual JE / System generated JE in terms of number and value  '''
            Je_auto_manual=FinalTable.objects\
             .filter(client=clientname,engangement=engangement)\
            .values('TransactionType')\
            .annotate(Generated=Count('TransactionType'))
            context['TransactionType']=Je_auto_manual
            # ==========================================================================
                    #'''created and authorized by same user'''
            data1=FinalTable.objects\
            .filter(client=clientname,engangement=engangement)\
            .filter(AuthorisedBy__iregex=F('CreatedBy'))
            context['cre_equ_auth']=data1.count()
# =================================================================================
                    # JV passby Month
            Jv_month=FinalTable.objects\
            .values('JournalDate')\
            .filter(client=clientname,engangement=engangement)\
            .annotate(Credit=Cast('CreditAmount', FloatField()),Debit=Cast('DebitAmount', FloatField()))\
            .annotate(c=Count('CreatedBy'),Credit=Sum('Credit'),Debit=Sum('Debit'))
            context['Jvmonth']=Jv_month
            # =================================================
                 #JV's with related parties
        #     JvParties=FinalTable.objects\
        #     .values('MainAccountName')\
        #     .annotate(c=Count('MainAccountName'))\
        #     .filter(client=clientname,engangement=engangement)
        #     context['JvP']=JvParties
    # =======================================================================================
           #JV's On Weekend
            Jvholidays=FinalTable.objects\
            .values('JournalDate')\
            .annotate(c=Count('CreatedBy'))\
            .filter(client=clientname,engangement=engangement)\
            .filter(JournalDate__week_day__in=[1,6,7])
            context['JVweekend']=Jvholidays
#=================================================================================================
        #JV's with Little Description
            JvLittleDesc=FinalTable.objects\
            .values('ShortText','CreatedBy')\
            .filter(client=clientname,engangement=engangement)\
            .annotate(len=Length('ShortText'))\
            .filter(len__lte=25)
            context['JvLittleDesc']=JvLittleDesc
#========================================================================================\
            # Debit-Credit Amount
            JVCreDebAmount=FinalTable.objects\
             .filter(client=clientname,engangement=engangement)\
            .values('CreditAmount','DebitAmount','CurrencyCode' )\
            .annotate(Credit=Cast('CreditAmount', FloatField()),Debit=Cast('DebitAmount', FloatField()))\
            .aggregate(Sum('Credit'),Sum('Debit'))
            context['DebCre']=JVCreDebAmount
            JVCurrency=FinalTable.objects.values("CurrencyCode").distinct().filter(client=clientname,engangement=engangement)
            context['JVCurrency']=JVCurrency
#++++++++=================================================================================
            return render(request,'analytics.html',context)
# @permission_required('audtech_analytics.is_report',login_url='/PermissionDenied')
def JVSummary(request):
        filename =request.session.get('saved_file')
        clientname =request.session.get('clientname')
        engangement =request.session.get('engangement')
        context={}
        context['clientname']=clientname
        context['username']=request.session.get('username')
        context['customer']=request.session.get('schema_name')
        context['engangement']=engangement
        with schema_context(request.session.get('schema_name')):
                if request.method == "GET":
                        form = FinalTableFilter(request)
                        context['form']=form
                        return render(request,'Analytics/JVSummary.html',context)
                if request.method =="POST":
                        form = FinalTableFilter(request,request.POST)
                        print(str(request.POST.get("JournalDate"))+"============")
                        JE=FinalTable.objects\
                        .filter(Q(client=clientname,engangement=engangement) & Q(JournalDate__contains=request.POST.get('JournalDate'))
                        & Q(MainAccountCode__contains=request.POST.get('MainAccountCode')) & Q(AccountCategory__contains=request.POST.get('AccountCategory')))\
                        .values('MainAccountCode','MainAccountName','JournalDate','SubAccountCode','SubAccountName','AccountCategory','DebitAmount','CreditAmount')
                        context['JEuser']=JE
                        context['form']=form
                return render(request,'Analytics/JVSummary.html',context)
        return render(request,'Analytics/JVSummary.html',context)
# @permission_required('audtech_analytics.is_report',login_url='/PermissionDenied')
def ManualJE(request,value):
        clientname =request.session.get('clientname')
        engangement =request.session.get('engangement')
        context={}
        context['clientname']=clientname
        context['username']=request.session.get('username')
        context['customer']=request.session.get('schema_name')
        context['engangement']=engangement
        Je_auto_manual=FinalTable.objects\
        .filter(client=clientname,engangement=engangement,TransactionType=value)
        context['JournalType']=Je_auto_manual
        for I in Je_auto_manual:
                context['I']=I
                return render(request,'Analytics/ManualJE.html',context)

# @permission_required('audtech_analytics.is_report',login_url='/PermissionDenied')
def total_Tranasacion_according_to_users(request,value):
        clientname =request.session.get('clientname')
        engangement =request.session.get('engangement')
        context={}
        context['clientname']=clientname
        context['username']=request.session.get('username')
        context['customer']=request.session.get('schema_name')
        context['engangement']=engangement
        with schema_context(request.session.get('schema_name')):
                JE=FinalTable.objects\
                .filter(client=clientname,CreatedBy=value,engangement=engangement)
                context['JEuser']=JE
                for I in JE:
                        context['I']=I
                return render(request,'Analytics/total_Tranasacion_according_to_users.html',context)

# @permission_required('audtech_analytics.is_report',login_url='/PermissionDenied')
def SameAuthandCreate(request):
        clientname =request.session.get('clientname')
        engangement =request.session.get('engangement')
        context={}
        context['clientname']=clientname
        context['username']=request.session.get('username')
        context['customer']=request.session.get('schema_name')
        context['engangement']=engangement
        with schema_context(request.session.get('schema_name')):
            data1=FinalTable.objects\
            .filter(client=clientname,engangement=engangement)\
            .filter(AuthorisedBy__iregex=F('CreatedBy'))
            context['cre_equ_auth']=data1
            return render(request,'Analytics/SameAuthandCreate.html',context)

from django.db.models import Q
# @permission_required('audtech_analytics.is_report',login_url='/PermissionDenied')
def PostedUnposted(request,value):
        clientname =request.session.get('clientname')
        engangement =request.session.get('engangement')
        context={}
        context['clientname']=clientname
        context['username']=request.session.get('username')
        context['customer']=request.session.get('schema_name')
        context['engangement']=engangement
        with schema_context(request.session.get('schema_name')):
                posted_unposted=FinalTable.objects\
                .filter(Q(client=clientname)&Q(engangement=engangement)).order_by('SrNo')\
                .filter(StatusPostedUnposted=value)
                context['pos_unpos']=posted_unposted
                for I in posted_unposted:
                        context['I']=I
                return render(request,'Analytics/PostedUnposted.html',context)


# @permission_required('audtech_analytics.is_report',login_url='/PermissionDenied')
def Missingvalues(request):
        clientname =request.session.get('clientname')
        engangement =request.session.get('engangement')
        context={}
        context['clientname']=clientname
        context['username']=request.session.get('username')
        context['customer']=request.session.get('schema_name')
        context['engangement']=engangement
        with schema_context(request.session.get('schema_name')):
                obj=FinalTable.objects.filter(client=clientname,engangement=engangement).order_by('SrNo')
                qs=read_frame(obj)
                df=pd.DataFrame(qs).drop(['client','engangement','user_id','Upload_Date','id'], axis=1)
                df['SrNo']=df['SrNo'].astype(float)
                dcf=pd.DataFrame(missing_values(df['SrNo'])).rename(columns={0:'Missing Values'})  
                context['missing']=dcf.to_html()
                return render(request,'Analytics/Missingvalues.html',context)
# @permission_required('audtech_analytics.is_report',login_url='/PermissionDenied')
def JVwithRelatedParties(request,value):
        clientname =request.session.get('clientname')
        engangement =request.session.get('engangement')
        context={}
        context['clientname']=clientname
        context['username']=request.session.get('username')
        context['customer']=request.session.get('schema_name')
        context['engangement']=engangement
        with schema_context(request.session.get('schema_name')):
                JvParties=FinalTable.objects\
                .filter(client=clientname,engangement=engangement,MainAccountName=value)
                context['JvP']=JvParties
                for JE in JvParties:
                        context['JE']=JE
                return render(request,'Analytics/JVwithRelatedParties.html',context)

def Jvmonth(request,value):
        clientname =request.session.get('clientname')
        engangement =request.session.get('engangement')
        context={}
        context['clientname']=clientname
        context['username']=request.session.get('username')
        context['customer']=request.session.get('schema_name')
        context['engangement']=engangement
        with schema_context(request.session.get('schema_name')):
                Jv_month=FinalTable.objects\
                .filter(client=clientname,engangement=engangement,JournalDate=value)\
                .order_by('JournalDate')
                context['Jvmonth']=Jv_month
                for I in Jv_month:
                        context['I']=I
                return render(request,'Analytics/Jv_month.html',context)

from datetime import timedelta
def LastPeriodEneries(request):
        clientname =request.session.get('clientname')
        engangement =request.session.get('engangement')
        context={}
        context['clientname']=clientname
        context['username']=request.session.get('username')
        context['customer']=request.session.get('schema_name')
        context['engangement']=engangement
        with schema_context(request.session.get('schema_name')):
                eng=Engagement.objects.get(name=clientname,engagement_name=engangement)
                lastdate= eng.fiscal_end_month - timedelta(days=5)
                LastPeriodEneries=FinalTable.objects\
                .filter(client=clientname,engangement=engangement,JournalDate__range=(eng.fiscal_end_month,lastdate))
                context['LastPeriodEneries']=LastPeriodEneries
                return render(request,'Analytics/LastPeriodEneries.html',context)
def JVNotBalToZero(request):
        clientname =request.session.get('clientname')
        engangement =request.session.get('engangement')
        context={}
        context['clientname']=clientname
        context['username']=request.session.get('username')
        context['customer']=request.session.get('schema_name')
        context['engangement']=engangement
        with schema_context(request.session.get('schema_name')):
                JVBalZero=FinalTable.objects.filter(client=clientname,engangement=engangement).exclude(DebitAmount=('CreditAmount'))
                context['Jv0']=JVBalZero
                for I in JVBalZero:
                        context['I']=I
                return render(request,'Analytics/JVNotBalToZero.html',context)

