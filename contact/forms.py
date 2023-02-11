from django import forms

class ContactForm(forms.Form):
	name = forms.CharField(required=False,max_length=100)
	email = forms.EmailField(required=True)
	comments = forms.CharField(required=True, widget =forms.Textarea)


