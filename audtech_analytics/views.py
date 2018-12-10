from django.shortcuts import render
from customers.models import FinalTable

# Create your views here.
def DisplayData(request):
    context={}
    if request.method=="GET":
        context['objects']=FinalTable.objects.all()
        return render(request,'showdata.html',context)