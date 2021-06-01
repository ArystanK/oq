from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from accounts.models import Teacher, Student


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class UpdateTeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ['about_me', 'language', 'profile_picture']


class UpdateStudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['profile_picture']
