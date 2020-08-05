from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField()
    contnent = forms.CharField(widget=Textarea)
    
