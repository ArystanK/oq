from django.forms import ModelForm
from .models import Course, Group, Assignment, Lesson


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = "__all__"
        # exclude = ('teacher',)


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = "__all__"


class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields = "__all__"


class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = "__all__"
