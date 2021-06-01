from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import django.contrib.auth.models

import education.models
from .models import Student, Teacher
from .forms import CreateUserForm, UpdateTeacherForm, UpdateStudentForm
from .decorators import unauthenticated_user, allowed_users


@allowed_users(allowed_roles=['teacher'])
@login_required(login_url='login')
def profile_page(request):
    teacher = Teacher.objects.get(user=request.user)
    courses = education.models.Course.objects.filter(teacher=teacher)
    last_lesson = education.models.Lesson.objects.last()
    return render(request, 'accounts/profile.html',
                  context={'teacher': teacher, 'courses': courses, 'lesson': last_lesson})


@allowed_users(allowed_roles=['teacher'])
@login_required(login_url='login')
def update_profile_teacher(request):
    teacher = Teacher.objects.get(user=request.user)
    form = UpdateTeacherForm(instance=teacher)
    if request.method == 'POST':
        form = UpdateTeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request, 'accounts/edit_profile_page.html', {'form': form})


@unauthenticated_user
def register_page(request, is_student):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=request.POST.get('username'))
            if is_student == 1:
                group_name = 'student'
                student = Student(user=user)
                student.save()
            else:
                group_name = 'teacher'
                teacher = Teacher(user=user)
                teacher.save()
            group = django.contrib.auth.models.Group.objects.get(name=group_name)
            user.groups.add(group)
            messages.success(request, "Account was created for " + str(user))
            return redirect('login')
    return render(request, 'accounts/application.html', {"is_student": is_student, "form": form})


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        messages.info(request, "Username OR password is incorrect")
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout_page(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def student_page(request):
    student = Student.objects.get(user=request.user)
    groups = education.models.Group.objects.filter(students__student_id=student.student_id)
    return render(request, 'accounts/student.html', {'student': student, 'groups': groups})


@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def edit_student_page(request):
    student = Student.objects.get(user=request.user)
    form = UpdateStudentForm(instance=student)
    if request.method == 'POST':
        form = UpdateStudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student')
    return render(request, 'accounts/edit_student.html', {'form': form})
