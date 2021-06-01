from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.decorators import allowed_users
from .filters import CourseFilter
from .forms import CourseForm
from .models import Course, Student, Teacher, Group


def home_page(request):
    my_filter = CourseFilter()
    courses = Course.objects.all()[0:4]
    return render(request, "education/home.html", {'courses': courses, 'my_filter': my_filter})


def search_page(request):
    courses = Course.objects.all()
    my_filter = CourseFilter(request.GET, queryset=courses)
    courses = my_filter.qs
    return render(request, "education/search.html", {'my_filter': my_filter, 'courses': courses})


def course_detail(request, pk):
    course = Course.objects.get(pk=pk)
    groups = Group.objects.filter(course=course)
    topics = course.syllabus.split(', ')
    languages = course.languages.split(',')
    return render(request, 'education/course.html',
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
    return render(request, "education/create_course.html", context)


@allowed_users(allowed_roles=['teacher'])
@login_required(login_url='login')
def update_course_page(request, pk):
    course = Course.objects.get(pk=pk)
    form = CourseForm(instance=course)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('profile')
    context = {'form': form}
    return render(request, "education/create_course.html", context)


@allowed_users(allowed_roles=['teacher'])
@login_required(login_url='login')
def delete_course_page(request, pk):
    course = Course.objects.get(pk=pk)
    if request.method == "POST":
        course.delete()
        redirect('/')
    context = {'item': course}
    return render(request, "education/delete_course.html", context)


@allowed_users(allowed_roles=['student'])
@login_required(login_url='login')
def apply_for_course(request, course_id):
    student = Student.objects.get(user=request.user)
    course = Course.objects.get(pk=course_id)
    language = request.POST.get('language')
    return redirect('home')
