from customers.models import Client
from django.conf import settings
from django.db import utils
from django.views.generic import TemplateView
from django.shortcuts import render,redirect
from tenant_schemas.utils import remove_www
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from tenant_schemas.utils import schema_context
from django.http import HttpResponse
def LoginView(request):
    context={}
    if request.method=='GET':
        return render(request,'login.html',context)
    elif request.method=='POST':
        result=authenticate(username=request.POST.get("login"),password=request.POST.get("password"))
        if result:
            login(request,result)
            print(result)
            client=Client.objects.get(user_id=request.user.id)
            request.session['username']=request.POST.get("login")
            request.session['schema_name']=client.schema_name
            print("schema is " + str(client.schema_name))
            return redirect('/ClientTable')
        else:
            with schema_context(request.POST.get('company')):
                U=authenticate(username=request.POST.get("login"),password=request.POST.get("password"))
                print(U)
                if U:
                    login(request,U)
                    # CL=User.objects.get(user)    
                    request.session['username']=request.POST.get("login")
                    request.session['schema_name']=request.POST.get('company')
                    print("schema is " + str(client.schema_name))
                    return redirect('/ClientTable')
                else:
                    context['error']="Login Failed"
                return render(request,'login.html',context)


def LogoutView(request):
    uname=request.user.username
    logout(request)
    return redirect('/login')
    
class HomeView(TemplateView):
    template_name = "index_public.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        hostname_without_port = remove_www(self.request.get_host().split(':')[0])

        try:
            Client.objects.get(schema_name='public')
        except utils.DatabaseError:
            context['need_sync'] = True
            context['shared_apps'] = settings.SHARED_APPS
            context['tenants_list'] = []
            return context
        except Client.DoesNotExist:
            context['no_public_tenant'] = True
            context['hostname'] = hostname_without_port

        if Client.objects.count() == 1:
            context['only_public_tenant'] = True

        context['tenants_list'] = Client.objects.all()
        return context
