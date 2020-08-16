from django import forms

from .models import MenuItem 

class MenuItemForm(forms.Form):
    title = forms.CharField()
    slug = forms.SlugField()
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 25}))
    price = forms.IntegerField()

class MenuItemModelForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['title', 'price', 'description','category', 'label']

    def clean_title(self, *args, **kwargs):
        instance = self.instance
        title = self.cleaned_data.get('title')
        qs = MenuItem.objects.filter(title__iexact=title)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError('This prodact is already exist. Please, choose another product title')
        return title