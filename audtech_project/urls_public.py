from django.conf.urls import url
from audtech_analytics.views import DisplayData
from customers.views import CreateTenant,ProcessFile
urlpatterns = [
    url(r'^createtenant$', CreateTenant),
    url(r'^processfile$', ProcessFile),
    url(r'^display$', DisplayData),

]
