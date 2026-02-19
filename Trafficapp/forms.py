# from django import forms
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User
# from .models import Profile, QuizTest, QuizQuestion,TrafficRule,Tutorial




# # Signup Form
# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

#     class Meta:
#         model = User
#         fields = ["username", "email", "password1", "password2"]


# # Login Form
# class CustomAuthenticationForm(AuthenticationForm):
#     username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

# class UserUpdateForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email']

# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['phone', 'city', 'profile_picture']
        
        

# # forms.py
# class QuizQuestionForm(forms.ModelForm):
#     class Meta:
#         model = QuizQuestion
#         fields = ["question", "option_a", "option_b", "option_c", "option_d", "correct_answer", "image"]  # ✅ added image
#         widgets = {
#             "question": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
#             "option_a": forms.TextInput(attrs={"class": "form-control"}),
#             "option_b": forms.TextInput(attrs={"class": "form-control"}),
#             "option_c": forms.TextInput(attrs={"class": "form-control"}),
#             "option_d": forms.TextInput(attrs={"class": "form-control"}),
#             "correct_answer": forms.Select(attrs={"class": "form-select"}),
#         }
   

# class QuizTestForm(forms.ModelForm):
#     class Meta:
#         model = QuizTest
#         fields = ["title"]   # only title for now


# class AdminCreationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ["username", "email", "password"]

# class UserCreationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ["username", "email", "password"]

# class CustomUserCreationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ["username", "email", "password"]
        
# class TrafficRuleForm(forms.ModelForm):
#     class Meta:
#         model = TrafficRule
#         fields = ["title", "file"]
        
#         from .models import Tutorial

# class TutorialForm(forms.ModelForm):
#     class Meta:
#         model = Tutorial
#         fields = ["title", "file"]   # matches your model fields
#         widgets = {
#             "title": forms.TextInput(attrs={"class": "form-control"}),
#             "file": forms.ClearableFileInput(attrs={"class": "form-control"}),
#         }

# class TutorialForm(forms.ModelForm):
#     class Meta:
#         model = Tutorial
#         fields = ["title", "file"]
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, QuizTest, QuizQuestion, TrafficRule, Tutorial


# -------------------------------
# 🔐 AUTHENTICATION FORMS
# -------------------------------

# ✅ Signup Form (uses Django’s built-in password hashing)
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


# ✅ Login Form
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))


# -------------------------------
# 👤 PROFILE FORMS
# -------------------------------

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'city', 'profile_picture']


# -------------------------------
# 🧠 QUIZ FORMS
# -------------------------------

class QuizQuestionForm(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = ["question", "option_a", "option_b", "option_c", "option_d", "correct_answer", "image"]
        widgets = {
            "question": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "option_a": forms.TextInput(attrs={"class": "form-control"}),
            "option_b": forms.TextInput(attrs={"class": "form-control"}),
            "option_c": forms.TextInput(attrs={"class": "form-control"}),
            "option_d": forms.TextInput(attrs={"class": "form-control"}),
            "correct_answer": forms.Select(attrs={"class": "form-select"}),
        }


class QuizTestForm(forms.ModelForm):
    class Meta:
        model = QuizTest
        fields = ["title"]


# -------------------------------
# 🚦 TRAFFIC RULES FORM
# -------------------------------

class TrafficRuleForm(forms.ModelForm):
    class Meta:
        model = TrafficRule
        fields = ["title_en", "title_ur", "file"]
        widgets = {
            "title_en": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter English title"}),
            "title_ur": forms.TextInput(attrs={"class": "form-control", "placeholder": "اردو عنوان درج کریں"}),
            "file": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


# -------------------------------
# 🎓 TUTORIAL FORM
# -------------------------------

class TutorialForm(forms.ModelForm):
    class Meta:
        model = Tutorial
        fields = ["title_en", "title_ur", "file"]
        widgets = {
            "title_en": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter English title"}),
            "title_ur": forms.TextInput(attrs={"class": "form-control", "placeholder": "اردو عنوان درج کریں"}),
            "file": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

#Forget Password

from django import forms

class ForgetPasswordForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    
    
#Reset Password Form
class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput,
        label="New Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password"
    )
