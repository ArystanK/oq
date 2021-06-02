from django import forms

from .models import Course, Lesson, Assignment


class CreateAssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['group', 'title', 'description', 'task', 'student']


class UpdateAssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['group', 'title', 'description', 'task', 'student', 'grade']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = "__all__"
