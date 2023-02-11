from django.shortcuts import render, redirect
from django.core.mail import send_mail,BadHeaderError
from django.conf import settings
from .forms import ContactForm
from django.contrib import messages
# Create your views here.


def contact_view(request,*args,**kwargs):
    form = ContactForm(request.POST or None)
    if form.is_valid():

    	body = {
    	'name': form.cleaned_data['name'],
    	'email': form.cleaned_data['email'],
    	'comments':form.cleaned_data['comments'],
    	}
    	subject = "Website Inquiry from {}".format(body['name'])

    	# message = "\n".join(body.values())
    	message = body['comments']

    	try:
    		send_mail(subject, message,body['email'],[settings.EMAIL_HOST_USER])
    		messages.success(request, "Message sent." )

    	except BadHeaderError:
    		messages.error(request, "Error. Message not sent.")

    	return redirect ("/contact")
    form = ContactForm()
    return render(request, "contact.html", {'form':form})


# def contact_view(request,*args,**kwargs):
# 	form = ContactForm(request.POST or None)
# 	confirm_msg = None
# 	if form.is_valid():
# 		name = form.cleaned_data['name']
# 		comments = form.cleaned_data['comments']

# 		subject = 'message from my django app'
# 		message = '%s %s' %(comments,name)
# 		emailFrom = settings.EMAIL_HOST_USER 
# 		emailTo =form.cleaned_data['email']

# 		# CHANGE THE fail_silently to true when debugging

# 		send_mail(subject,message,emailFrom,[emailTo],fail_silently=True,)
		
		
# 		confirm_msg = messages.add_message(request,messages.SUCCESS,
# 			'Thanks for your message',fail_silently=True)
# 		form = ContactForm()
# 	context = {'confirm_msg':confirm_msg,'form':form}
# 	return render(request , 'contact.html',context)
# 	