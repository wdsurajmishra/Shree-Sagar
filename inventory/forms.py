from import_export.forms import ExportForm
from django import forms
from .resources import ProductVariantResource



class ProductExportForm(ExportForm):
    resource = ProductVariantResource()
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))


