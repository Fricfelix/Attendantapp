from django.shortcuts import render
# from app.settings import GEOLOCATION_API

# Create your views here.


from django.shortcuts import render, HttpResponse

# Create your views here.

   




def home_view(request,*args,**kwargs):
	context = {}

	return render(request , 'index.html',context)
	