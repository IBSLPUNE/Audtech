from __future__ import unicode_literals

from django.db import models
from audtech_analytics import  constants
# Create your models here.

    
class EndClient(models.Model):
     name=models.CharField(max_length=60,null=True,blank=True)
     email=models.EmailField(blank=True, max_length=60, unique=True,null=True)
     company_ode=models.CharField(max_length=60,null=True,blank=True,verbose_name="Company Code")
     description=models.TextField(max_length=200, null=True,blank=True)
     company_type= models.CharField(max_length=60,null=True,blank=True)
     registration_no=models.CharField(max_length=60,null=True,blank=True)
     address=models.CharField(default='', max_length=300,null=True,blank=True)
     country=models.CharField(max_length=80,null=True,blank=True)
     document=models.FileField(upload_to='',null=True,blank=True),
     state=models.CharField(max_length=90,null=True,blank=True)
     contact_no=models.CharField(max_length=90,null=True,blank=True)
     starting_date=models.DateField(null=True,blank=True)
     created_date=models.DateField(null=True,blank=True,auto_now_add=True)
     def __str__(self):
         return self.name

class Engagement(models.Model):
    endclient=models.ForeignKey(EndClient,on_delete=models.PROTECT)
    engagement_name=models.CharField(max_length=90,null=True,blank=True)
    peroid_frequency=models.CharField(max_length=90,choices=constants.PEROID_FREQUENCY,null=True,blank=True)
    financial_management_system=models.CharField(max_length=90,null=True,blank=True)
    fiscal_start_month=models.DateField(blank=True,null=True)
    additional_info=models.TextField(blank=True,null=True)
    created_date=models.DateField(null=True,blank=True,auto_now_add=True)

class FinalTable(models.Model):
    client=models.CharField(max_length=200, blank=True, null=True)
    engangement=models.CharField(max_length=200, blank=True, null=True)
    user_id=models.CharField(max_length=200, blank=True, null=True)
    upload_date=models.DateField(blank=True,null=True)
    status_op_posted_unposted=models.CharField(max_length=200, blank=True, null=True)
    type_regular=models.CharField(max_length=200, blank=True, null=True)
    div_code=models.CharField(max_length=200, blank=True, null=True)
    doc_date=models.DateField(blank=True,null=True)
    sr_no=models.CharField(blank=True,null=True,max_length=100)
    tr_code=models.CharField(max_length=200, blank=True, null=True)
    doc_no=models.CharField(max_length=200, blank=True, null=True)
    acct_category=models.CharField(max_length=200, blank=True, null=True)
    main_acct_code=models.CharField(max_length=200, blank=True, null=True)
    main_acct_name=models.CharField(max_length=200, blank=True, null=True)
    sub_acct_code=models.CharField(max_length=200, blank=True, null=True)
    sub_acct_name=models.CharField(max_length=200, blank=True, null=True)
    dr_gl_curr_code=models.CharField(max_length=200, blank=True, null=True)
    cr_gl_curr_code=models.CharField(max_length=200, blank=True, null=True)
    tr_curr_code=models.CharField(max_length=200, blank=True, null=True)
    dr_in_fc=models.CharField(max_length=200, blank=True, null=True)
    cr_in_fc=models.CharField(max_length=200, blank=True, null=True)
    created_by=models.CharField(max_length=200, blank=True, null=True)
    authorised_by=models.CharField(max_length=200, blank=True, null=True)
    auto_manual=models.CharField(max_length=200, blank=True, null=True)
    created_date=models.DateField(null=True,blank=True,auto_now_add=True)




class OriginalData(models.Model):
    client=models.CharField(max_length=200, blank=True, null=True)
    engangement=models.CharField(max_length=200, blank=True, null=True)
    user_id=models.CharField(max_length=200, blank=True, null=True)
    upload_date=models.DateField(blank=True,null=True)
    c1 = models.CharField(max_length=200, blank=True, null=True)
    c2 = models.CharField(max_length=200, blank=True, null=True)
    c3 = models.CharField(max_length=200, blank=True, null=True)
    c4 = models.CharField(max_length=200, blank=True, null=True)
    c5 = models.CharField(max_length=200, blank=True, null=True)
    c6 = models.CharField(max_length=200, blank=True, null=True)
    c7 = models.CharField(max_length=200, blank=True, null=True)
    c8 = models.CharField(max_length=200, blank=True, null=True)
    c9 = models.CharField(max_length=200, blank=True, null=True)
    c10 = models.CharField(max_length=200, blank=True, null=True)
    c11 = models.CharField(max_length=200, blank=True, null=True)
    c12 = models.CharField(max_length=200, blank=True, null=True)
    c13 = models.CharField(max_length=200, blank=True, null=True)
    c14 = models.CharField(max_length=200, blank=True, null=True)
    c15 = models.CharField(max_length=200, blank=True, null=True)
    c16 = models.CharField(max_length=200, blank=True, null=True)
    c17 = models.CharField(max_length=200, blank=True, null=True)
    c18 = models.CharField(max_length=200, blank=True, null=True)
    c19 = models.CharField(max_length=200, blank=True, null=True)
    c20 = models.CharField(max_length=200, blank=True, null=True)
    c21 = models.CharField(max_length=200, blank=True, null=True)
    created_date=models.DateField(null=True,blank=True,auto_now_add=True)

