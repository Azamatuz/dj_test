from django import forms

from .models import MenuItem 

class MenuItemForm(forms.Form):
    title = forms.CharField()
    slug = forms.SlugField()
    description = forms.CharField(widget=forms.Textarea)
    price = forms.IntegerField()

class MenuItemModelForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['title', 'description', 'price']

    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get('title')
        qs = MenuItem.objects.filter(title=title)
        if qs.exists():
            raise forms.ValidationError('This prodact is already exist. Please, choose another product title')
        return title