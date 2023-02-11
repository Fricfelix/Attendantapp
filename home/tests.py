from django.test import TestCase

# Create your tests here.

from django.shortcuts import render
from app.settings import GEOLOCATION_API

# Create your views here.


from django.shortcuts import render, HttpResponse

# Create your views here.

   




def home_view(request,*args,**kwargs):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	response = HttpResponse(f"https://ipgeolocation.abstractapi.com/v1/?api_key={GEOLOCATION_API}")


	api_key = GEOLOCATION_API
	api_url = HttpResponse(f"https://ipgeolocation.abstractapi.com/v1/?api_key={GEOLOCATION_API}")


	# api_url = 'https://ipgeolocation.abstractapi.com/v1/?api_key=' + api_key


	# get_ip_geolocation_data(ip_address):

	context = {}
	if x_forwarded_for:
		res = HttpResponse(api_url + "&ip_address=" + ip_address)

		ip = x_forwarded_for.split(',')[0]
		context = {"ip":ip,
					"location":res
		}
		return render(request , 'index.html',context)

	else:
		ip = request.META.get('REMOTE_ADDR')
		context = {"ip":ip}
		return render(request , 'index.html',context)

	# return HttpResponse("Welcome! You are visiting from: {}".format(ip))


	return render(request , 'index.html',context)
	