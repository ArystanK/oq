from django.db import models
from accounts.models import Teacher, Student


class Course(models.Model):
    course_name = models.CharField(max_length=50)
    about_course = models.CharField(max_length=255)
    price = models.FloatField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_students = models.IntegerField()
    languages = models.CharField(max_length=255)
    syllabus = models.TextField()

    def __str__(self):
        return self.course_name


class Group(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    students = models.ManyToManyField(Student)
    number_of_students = models.IntegerField(default=1)

    def __str__(self):
        return self.course.course_name + " by " + str(self.course.teacher) + " on " + self.language


class Assignment(models.Model):
    title = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    task = models.FileField(null=True, blank=True)
    submission = models.FileField(null=True, blank=True)
    grade = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title + " for " + str(self.student)


class Lesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    description = models.TextField()
    recording_link = models.TextField(null=True, blank=True)
    time = models.DateTimeField()

    def __str__(self):
        return str(self.group) + " at " + str(self.time.date()) + " " + str(self.time.time())
