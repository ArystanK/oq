from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    student_id = models.AutoField(primary_key=True, unique=True)
    profile_picture = models.ImageField(default="profile_pic.jpeg")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Teacher(models.Model):
    profile_picture = models.ImageField(default="profile_pic.jpeg")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about_me = models.TextField()

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
