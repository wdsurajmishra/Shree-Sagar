from django import forms
from accounts.models import Customer
from orders.models import ShippingAddress

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone','profile_picture']

class ShippingAddressForm(forms.ModelForm):
    state = forms.CharField(widget=forms.Select(attrs={'id': 'state', 'class': 'form-select', 'onchange': 'populateDistricts()'}), required=True)
    city = forms.CharField(widget=forms.Select(attrs={'id': 'city', 'class': 'form-select', }), required=True)

    class Meta:
        model = ShippingAddress
        fields = ['phone_number', 'full_name', 'address_line_1', 'address_line_2', 'state',  'city', 'country', 'postal_code']


from django.contrib.flatpages.models import FlatPage
from .fields import RichTextField  # Import your custom field

class FlatPageForm(forms.ModelForm):
    content = RichTextField() # Use your RichTextField here.

    class Meta:
        model = FlatPage
        fields = ('url', 'title', 'content', 'template_name', 'registration_required', 'sites')

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
