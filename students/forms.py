from django import forms 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from students.models import Profile

class RegisterForm(UserCreationForm):
    STUDENT = 'student'
    TEACHER = 'teacher'

    STATUS_CHOICES = [
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
    ]
    
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter your name',
                                                                                              'class': 'box'
                                                                                              }))
    
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                                                              'class': 'box'
                                                                                              }))
    
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                                                              'class': 'box'
                                                                                              }))
    
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                                          'class': 'box'
                                                                          }))
    
    password1 = forms.CharField(max_length=50,required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                                              'class': 'box',
                                                                                              'data-toggle': 'password',
                                                                                              'id': 'password'
                                                                                              }))
    
    password2 = forms.CharField(max_length=50,required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                                              'class': 'box',
                                                                                              'data-toggle': 'password',
                                                                                              'id': 'password'
                                                                                              }))
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'box'
        })
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'status']
        
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
            # Check if the profile already exists
            profile, created = Profile.objects.get_or_create(user=user)
            profile.status = self.cleaned_data['status']
            profile.save()
        return user
    
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'box'}))
    
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'box',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']
        
        
class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'box'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'box'}))
    
    first_name = forms.CharField(required=True,
                             widget=forms.TextInput(attrs={'class': 'box'}))
    
    last_name = forms.CharField(required=True,
                             widget=forms.TextInput(attrs={'class': 'box'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UpdateProfileForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'box'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'box', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['image', 'bio']