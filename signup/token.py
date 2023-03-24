
# # def send_confirmation_email(user,request):
# #   current_site = get_current_site(request)
# #   uid = urlsafe_base64_encode(force_bytes(user.pk))
# #   token = user.email_confirmation_token
# #   confirmation_url = request.build_absolute_uri(reverse('confirm_email',kwargs={'uidb64':uid,'token':token}))
# #   subject = "Please confirm email to activate your account"
# #   message = render_to_string('comfirm-email.html',{'user':user,'domain':current_site.domain,'confirmation_url':confirmation_url})
    
# #   email_from = settings.EMAIL_HOST_USER
# #   recipient_list = [user.email]
# #   send_mail = EmailMessage(subject,message,email_from,recipient_list)
# #   send_mail.content_type = 'html'
# #   send_mail.send()


# from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.tokens import default_token_generator
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode
# from django.utils.translation import ugettext_lazy as _
# from .forms import CustomUserCreationForm

# def signup(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             subject = _('Activate Your Account')
#             message = render_to_string('signup_activation_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': default_token_generator.make_token(user),
#             })
#             to_email = form.cleaned_data.get('email')
#             send_mail(subject, message, 'noreply@example.com', [to_email], fail_silently=False)
#             return render(request, 'signup_activation_sent.html', {'email': to_email})
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'signup.html', {'form': form})

    

# def activate(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = CustomUser.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
#         user = None

#     if user and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         return redirect('home')

#     return render(request, 'signup_activation_invalid.html')



# # def send_confirmation_email(user,request):
# # subject = _('Activate Your Account')
# #             message = render_to_string('signup_activation_email.html', {
# #                 'user': user,
# #                 'domain': current_site.domain,
# #                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
# #                 'token': default_token_generator.make_token(user),
# #             })
# #             to_email = form.cleaned_data.get('email')
# #             send_mail(subject, message, 'noreply@example.com', [to_email], fail_silently=False)
# #             return render(request, 'signup_activation_sent.html', {'email': to_email})