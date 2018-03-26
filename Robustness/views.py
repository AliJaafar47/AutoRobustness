from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
# Create your views here.

@login_required(login_url='/accounts/login/')
def login_success(request):
    return render(request,'index.html',context={})