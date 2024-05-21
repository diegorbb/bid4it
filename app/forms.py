from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2']


class ListProduct(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ['seller']


class ArchiveListingForm(forms.Form):
    confirm = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']


class ListingForm(ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'starting_price', 'archived', 'image']