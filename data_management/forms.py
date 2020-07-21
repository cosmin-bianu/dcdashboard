from django import forms

class LoginForm(forms.Form):
    username=forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'input is-rounded is-primary is-medium', 'placeholder':'Nume de utilizator'}))
    password=forms.CharField(max_length=60, widget=forms.PasswordInput(attrs={'class': 'input is-rounded is-primary is-medium', 'placeholder':'Parolă'}))