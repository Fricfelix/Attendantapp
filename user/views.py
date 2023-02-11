from django.shortcuts import render

# Create your views here.

def user_view(request,*args,**kwargs):
	return render(request , 'user.html',{})
