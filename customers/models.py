from django.db import models
from tenant_schemas.models import TenantMixin


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    created_on = models.DateField(auto_now_add=True)

class Mapping(models.Model):
    erp=models.CharField(max_length=200, blank=True, null=True)
    transaction_type=models.CharField(max_length=200, blank=True, null=True)
    final_field=models.CharField(max_length=200, blank=True, null=True)
    source_filed=models.CharField(max_length=200, blank=True, null=True)