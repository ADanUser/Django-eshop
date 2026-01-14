from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "input"})
            field.help_text = None


# class UserAuthForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput, label='Пароль', strip=False)

#     class Meta:
#         model = User
#         fields = ['username', 'password']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs.update({"placeholder": " ", "class": "input"})
#             field.help_text = None

    
class UserAuthForm(forms.Form):
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={"class": "input"}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "input"}), strip=False)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not (username.isascii() and username.isalpha()):
            raise forms.ValidationError("Имя пользователя должно содержать только латинские буквы.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise forms.ValidationError("Пароль должен содержать не менее 8 символов.")
        return password