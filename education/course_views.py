from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.decorators import allowed_users
from accounts.models import Teacher
from education.forms import CourseForm
from education.models import Course, Group


def course_detail(request, pk):
    course = Course.objects.get(pk=pk)
    groups = Group.objects.filter(course=course)
    topics = course.syllabus.split(', ')
    languages = course.languages.split(',')
    return render(request, 'education/course/course.html',
                  {'course': course, 'topics': topics, 'groups': groups, 'languages': languages})


@allowed_users(allowed_roles=['teacher'])
@login_required(login_url='login')
def create_course_page(request):
    form = CourseForm()
    teacher_id = Teacher.objects.get(user=request.user).pk
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    context = {"form": form, 'teacher_id': teacher_id}
    return render(request, "education/course/create_course.html", context)


@allowed_users(allowed_roles=['teacher'])
@login_required(login_url='login')
def update_course_page(request, pk):
    course = Course.objects.get(pk=pk)
    if Teacher.objects.get(user=request.user) != course.teacher:
        return redirect('home')
    form = CourseForm(instance=course)
    teacher_id = course.teacher.pk
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('profile')
    start_date = str(course.start_date).split()[0]
    end_date = str(course.end_date).split()[0]
    context = {'form': form, 'start_date': start_date, 'end_date': end_date, 'teacher_id': teacher_id, 'course': course}
    return render(request, "education/course/update_course.html", context)


@allowed_users(allowed_roles=['teacher'])
@login_required(login_url='login')
def delete_course_page(request, pk):
    course = Course.objects.get(pk=pk)
    if Teacher.objects.get(user=request.user) != course.teacher:
        return redirect('home')
    if request.method == "POST":
        course.delete()
        return redirect('home')
    context = {'item': course}
    return render(request, "education/course/delete_course.html", context)