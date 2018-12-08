from django.conf.urls import url

from customers.views import CreateTenant,ProcessFile
urlpatterns = [
    url(r'^createtenant$', CreateTenant),
    url(r'^processfile$', ProcessFile),
]
