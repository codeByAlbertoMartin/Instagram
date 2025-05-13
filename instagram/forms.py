from django import forms
from  django.contrib.auth.models import User
from profiles.models import UserProfile


class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields = [
            'first_name',
            'username',
            'email',
            'password',
        ]
    def save(self):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data['password'])
        UserProfile.objects.get_or_create(user=user)
        user.save()    

        return user
    
class LoginForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario",max_length=100)
    password = forms.CharField(label="Password",widget=forms.PasswordInput)

class ProfileFollow(forms.Form):
    profile_pk = forms.IntegerField(widget=forms.HiddenInput())