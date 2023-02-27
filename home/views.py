from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings 
import geoip2.database
import geoip2
from ipware import ip

# Create your views here.


from django.shortcuts import render, HttpResponse

# Create your views here.

   




def home_view(request,*args,**kwargs):
	
	context = {		}
	return render(request , 'index.html',context)
	