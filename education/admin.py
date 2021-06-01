from django.contrib import admin

from .models import Course, Assignment, Group, Lesson

admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(Group)
admin.site.register(Lesson)
