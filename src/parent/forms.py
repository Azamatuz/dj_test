from django import forms

from .models import Kid 


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

COUNTRY_CHOICES = (
    ('CA', 'Canada'),
    #('US', 'United States')
)

PROVINCE_CHOICES = (
    ('AB', 'Alberta'), 
    ('BC', 'British Columbia'), 
    ('MB', 'Manitoba'), 
    ('NB', 'New Brunswick'), 
    ('NL', 'Newfoundland and Labrador'), 
    ('NT', 'Northwest Territories'), 
    ('NS', 'Nova Scotia'), 
    ('NU', 'Nunavut'), 
    ('ON', 'Ontario'), 
    ('PE', 'Prince Edward Island'), 
    ('QC', 'Quebec'), 
    ('SK', 'Saskatchewan'), 
    ('YT', 'Yukon')
    )
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


class CheckoutForm(forms.Form):
    shipping_street = forms.CharField(required=False)
    shipping_city = forms.CharField(required=False)
    shipping_country = forms.ChoiceField(
        required=False, 
        choices=COUNTRY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'custom-select d-block w-100'
        })
        )
    shipping_province = forms.ChoiceField(
        required=False,
        choices=PROVINCE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'custom-select d-block w-100'
        })
        )
    shipping_zip = forms.CharField(required=False)

    billing_street = forms.CharField(required=False)
    billing_city = forms.CharField(required=False)
    billing_country = forms.ChoiceField(
        required=False, 
        choices=COUNTRY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'custom-select d-block w-100'
        })
        )
    billing_province = forms.ChoiceField(
        required=False,
        choices=PROVINCE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'custom-select d-block w-100'
        })
        )
    billing_zip = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, 
        choices=PAYMENT_CHOICES)