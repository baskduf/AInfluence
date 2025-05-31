from django import forms

class SignupForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(), required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)
    email = forms.EmailField(widget=forms.TextInput())