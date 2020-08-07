from django import forms

from .models import EventItem, Vendor 

class EventItemForm(forms.Form):
    title = forms.CharField()
    slug = forms.SlugField()
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 25}))
    vendor = forms.CharField()

class EventItemModelForm(forms.ModelForm):
    class Meta:
        model = EventItem
        fields = ['title', 'date', 'description', 'vendor']

    def clean_title(self, *args, **kwargs):
        instance = self.instance
        title = self.cleaned_data.get('title')
        qs = EventItem.objects.filter(title__iexact=title)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError('This Event is already exist. Please, choose another event title')
        return title