from django.conf.urls import url
from audtech_analytics.views import DisplayData
from customers.views import CreateTenant,ProcessFile
# from django.contrib import admin
from django.conf.urls import url, include
from audtech_analytics import views
from django.conf.urls import url, include
from django.conf.urls.static import static
urlpatterns = [
    url(r'^createtenant$', CreateTenant),
    url(r'^processfile$', ProcessFile),
    url(r'^display$', DisplayData),
    url(r'^analytics$', views.AnalyticsBoard),

    # url('admin/', admin.site.urls),
    #  url(r'^signup/$', views.signup, name='signup'),
    #  url(r'login/', views.login, name='login'),
     url(r'^ClientRegister/$', views.ClientRegister, name='ClientRegister'),
     url(r'^ClientTable/$',views.ClientTable,name='ClientTable'),
     url(r'Engagement/$',views.EngagementDATA,name='Engagement'),
     url(r'ERPMap/$',views.ERPMap,name='ERPMap'),
    #  url(r'^ImportFile/$',views.ImportFile,name='ImportFile'),
    # url('ImportMainFile/<int:pk>',views.ImportMainFile,name='ImportMainFile'),
     #url(r'^simple_upload/$',views.simple_upload,name='simple_upload'),
    #  url(r'^Table/$',views.Table,name='Table'),
    #  url(r'^MissingValues/$',views.MissingValues,name='MissingValues'),
    #  url(r'^highcharts/$',views.highcharts,name='highcharts')
]
