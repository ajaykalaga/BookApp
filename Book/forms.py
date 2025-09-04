# Book/forms.py
from django import forms
from .models import Book
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "gener", "rating", "notes"]
        labels = {
            "title": "Title",
            "author": "Author",
            "gener": "Gener",
            "rating": "Rating",
            "notes": "Notes",
        }
        widgets = {
            "title":  forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter book title"}),
            "author": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter author name"}),
            "gener":  forms.Select(attrs={"class": "form-select"}),
            "rating": forms.NumberInput(attrs={"class": "form-control", "min": 0, "max": 10, "step": 1}),
            "notes":  forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Key takeaways, quotes, edition info…"}),
        }

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class":"form-control"}))
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class":"form-control"})
        self.fields["email"].widget.attrs.update({"class":"form-control"})
        self.fields["password1"].widget.attrs.update({"class":"form-control"})
        self.fields["password2"].widget.attrs.update({"class":"form-control"})

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields["username"].widget.attrs.update({"class":"form-control"})
        self.fields["password"].widget.attrs.update({"class":"form-control"})

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["display_name", "location", "bio"]
        widgets = {
            "display_name": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }