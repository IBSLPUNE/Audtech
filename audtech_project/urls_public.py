from django.conf.urls import url
# from audtech_analytics.views import DisplayData
from customers.views import CreateTenant,ProcessFile
# from django.contrib import admin
from django.conf.urls import url, include
from audtech_analytics import views 
from audtech_project import views as Anmol
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static


handler404 = views.handler404
urlpatterns = [
    url(r'HomeView/?$',Anmol.HomeView.as_view()),
    url(r'createtenant/?$', CreateTenant),
    url(r'processfile/?$', ProcessFile),
    url(r'display/$', views.DisplayData),
    url(r'analytics/$', views.AnalyticsBoard),
    url(r'login/?$', Anmol.LoginView),

    url(r'logout/$', Anmol.LogoutView),

    # url('admin/', admin.site.urls),
    #  url(r'signup/$', views.signup, name='signup'),
    #  url(r'login/', views.login, name='login'),
     url(r'ClientRegister/$', views.ClientRegister, name='ClientRegister'),
     url(r'navbar/$', views.navbar, name='navbar'),
    #   url(r'form/$', views.form, name='form'),
     url(r'CreateUser/$', views.CreateUser, name='CreateUser'),
     url(r'ClientTable/$',views.ClientTable,name='ClientTable'),
     url(r'Engagement/$',views.EngagementDATA,name='Engagement'),
     url(r'ERPMap/$',views.ERPMap,name='ERPMap'),
 
    #  url(r'ImportFile/$',views.ImportFile,name='ImportFile'),
    # url('ImportMainFile/<int:pk>',views.ImportMainFile,name='ImportMainFile'),
     #url(r'simple_upload/$',views.simple_upload,name='simple_upload'),
    #  url(r'Table/$',views.Table,name='Table'),
    #  url(r'MissingValues/$',views.MissingValues,name='MissingValues'),
    #  url(r'highcharts/$',views.highcharts,name='highcharts')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
