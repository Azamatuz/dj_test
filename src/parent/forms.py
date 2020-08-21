from django import forms

from .models import Kid 

class KidForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    slug = forms.SlugField()
    province = forms.CharField()
    city = forms.CharField()
    school = forms.CharField()
    grade = forms.CharField() 
    teacher = forms.CharField()

class KidModelForm(forms.ModelForm):
    class Meta:
        model = Kid
        fields = ['first_name', 'last_name', 'province','city', 'school', 'grade', 'teacher']

    def clean_first_name(self, *args, **kwargs):
        instance = self.instance
        first_name = self.cleaned_data.get('first_name')
        qs = Kid.objects.filter(first_name__iexact=first_name)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError('This chile is already added.')
        return first_name