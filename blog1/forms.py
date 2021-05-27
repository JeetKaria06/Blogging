from django import forms
from django.forms import fields, models, widgets
from .models import Article, Author
from ckeditor.fields import RichTextField

class AuthorForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=500)
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = Author
        fields = ('username', 'password')

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get("password")
        username = cleaned_data.get("username")

        if not Author.objects.filter(username=username, password=password).exists():
            raise forms.ValidationError(
                "username and password don't match!"
            )

class AuthorRegiterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Author
        fields = ('username', 'password', 'confirm_password')

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        username = cleaned_data.get("username")

        if Author.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Username already exists."
            )

        if password != confirm_password:
            raise forms.ValidationError(
                "Password and confirm_password does not match"
            )

class ArticleForm(forms.ModelForm):
    title = forms.CharField(max_length=200, label='Title')
    content = RichTextField()

    class Meta:
        model = Article
        fields = ('title', 'content')
    
    def clean(self):
        cleaned_data = self.cleaned_data