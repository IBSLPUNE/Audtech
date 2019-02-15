from django.db import models
from tenant_schemas.models import TenantMixin
from django.contrib.auth.models import User
from audtech_project import settings
from django.contrib.auth.models import AbstractUser



class Client(TenantMixin):
   user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
  
class Mapping(models.Model):
    eng=models.CharField(max_length=50, blank=True, null=True)
    erp=models.CharField(max_length=200, blank=True, null=True,verbose_name='Financial System')
    transaction_type=models.CharField(max_length=200, blank=True, null=True)
    final_field=models.CharField(max_length=200, blank=True, null=True,verbose_name='Audtech Field')
    source_filed=models.CharField(max_length=200, blank=True, null=True,verbose_name='System Field')
    column_no=models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        default_permissions = ()
        managed = True


class Mapping2(models.Model):
    eng=models.CharField(max_length=50, blank=True, null=True)
    user_id=models.CharField(max_length=50, blank=True, null=True)
    Audtech_field=models.CharField(max_length=50, blank=True, null=True)
    Input_field=models.CharField(max_length=50, blank=True, null=True)
    column_no=models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        default_permissions = ()
        managed = True


"""
class FinalTable(models.Model):
    client=models.CharField(max_length=200, blank=True, null=True)
    engangement=models.CharField(max_length=200, blank=True, null=True)
    user_id=models.CharField(max_length=200, blank=True, null=True)
    upload_date=models.DateField(blank=True,null=True)
    status_op_posted_unposted=models.CharField(max_length=200, blank=True, null=True)
    type_regular=models.CharField(max_length=200, blank=True, null=True)
    div_code=models.CharField(max_length=200, blank=True, null=True)
    doc_date=models.CharField(max_length=200,blank=True,null=True)
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
"""