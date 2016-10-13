# encoding: utf-8
__author__ = 'Nazmi ZORLU'
__email__ = "nazmizorlu@gmail.com"


from django.utils.translation import ugettext_lazy as _
from django import forms


class SearchForm(forms.Form):
    phrase = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": _("I'm looking for...")}))
    location = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": _("Location")}))

