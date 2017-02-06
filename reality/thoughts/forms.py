from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.html import strip_tags
from models import bella
from models import UserProfile
from dal import autocomplete
from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .fields import CommaSeparatedUserField
from django.core.files.images import get_image_dimensions
from .models import UserProfile

notification = None



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
    

class SearchForm(forms.ModelForm):
            username = forms.ModelChoiceField(
                queryset=UserProfile.objects.all(),
                widget=autocomplete.ModelSelect2(url='User-autocomplete')
                                           )
            #username3 = models.ManyToManyField('thoughts.thought')
            class Meta:
                model = User
                fields = []
                #widgets = {
                #'user': autocomplete.ModelSelect2Multiple(url='User-autocomplete'),
                #'username3': autocomplete.ModelSelect2Multiple(url='User-autocomplete')


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Last Name'}))
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password Confirmation'}))
    def clean_username(self):
    # Since User.username is unique, this check is redundant,
    # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
            raise forms.ValidationError(
                                self.error_messages['duplicate_username'],
                                code='duplicate_username',
                                )

def clean_password2(self):
    password1 = self.cleaned_data.get("password1")
    password2 = self.cleaned_data.get("password2")
    if password1 and password2 and password1 != password2:
        raise forms.ValidationError(
                                    self.error_messages['password_mismatch'],
                                    code='password_mismatch',
                                    )
    return password2

def save(self, commit=True):
    user = super(UserCreationForm, self).save(commit=False)
    user.set_password(self.cleaned_data["password1"])
    if commit:
        user.save()
        
        userProfile = DoctorSeeker(user=user, name=name, email=email)
        userProfile.save()
    
    return user

    
    def is_valid(self):
        form = super(UserCreateForm, self).is_valid()
        for f, error in self.errors.iteritems():
            if f != '__all_':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form
    
    class Meta:
        fields = ['email', 'username', 'first_name', 'last_name', 'password1',
                  'password2']
        model = User

class AuthenticateForm(AuthenticationForm):
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))
    
    def is_valid(self):
        form = super(AuthenticateForm, self).is_valid()
        for f, error in self.errors.iteritems():
            if f != '__all__':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form

class thoughtform(forms.ModelForm):
    image = forms.ImageField(required=False)
    content = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'special'}))
    
    def is_valid(self):
        form = super(thoughtform, self).is_valid()
        for f in self.errors.iterkeys():
            if f != '__all__':
                self.fields[f].widget.attrs.update({'class': 'error bellaText'})
        return form
    
    class Meta:
        model = bella
        exclude = ('user','likes',)

def clean_username(self):
    # Since User.username is unique, this check is redundant,
    # but it sets a nicer error message than the ORM. See #13147.
    username = self.cleaned_data["username"]
    try:
        User._default_manager.get(username=username)
    except User.DoesNotExist:
        return username
    raise forms.ValidationError(
                                self.error_messages['duplicate_username'],
                                code='duplicate_username',
                                )

def clean_password2(self):
    password1 = self.cleaned_data.get("password1")
    password2 = self.cleaned_data.get("password2")
    if password1 and password2 and password1 != password2:
        raise forms.ValidationError(
                                    self.error_messages['password_mismatch'],
                                    code='password_mismatch',
                                    )
    return password2


