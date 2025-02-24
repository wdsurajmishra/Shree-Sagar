from django import forms
from tinymce.widgets import TinyMCE

class RichTextField(forms.CharField):
    widget = TinyMCE()