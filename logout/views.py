from django.shortcuts import render

# Create your views here.

def logout_view(request,*args,**kwargs):
	return render(request , 'logout.html',{})