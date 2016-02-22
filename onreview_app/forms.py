from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password', widget=forms.PasswordInput())

class CommentForm(forms.Form):
    code = forms.CharField(label='Code',widget=forms.Textarea())
    description = forms.CharField(label='Description',widget=forms.Textarea())
    post_id = forms.CharField(label='post_id', widget=forms.HiddenInput())
