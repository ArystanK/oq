from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.decorators import allowed_users
from .filters import CourseFilter
from .forms import CourseForm, LessonForm
from .models import Course, Student, Teacher, Group, Lesson, Assignment


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
    start_date = str(course.start_date).split()[0]
    end_date = str(course.end_date).split()[0]
    context = {'form': form, 'start_date': start_date, 'end_date': end_date}
    return render(request, "education/update_course.html", context)


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
    groups = Group.objects.filter(course=course, language=language, number_of_students__lte=course.max_students)
    if len(groups) == 0:
        group = Group(course=course, language=language)
        group.save()
        group.students.add(student)
        group.save()
        return redirect('home')
    group = groups.first()
    group.students.add(student)
    group.number_of_students = group.number_of_students + 1
    group.save()
    return redirect('home')


@login_required(login_url='login')
def group_detail(request, pk):
    group = Group.objects.get(pk=pk)
    lessons = Lesson.objects.filter(group=group)
    lesson_count = len(lessons)
    assignments = Assignment.objects.filter(group=group)
    assignment_count = len(assignments)
    context = {'group': group, 'lessons': lessons, 'lesson_count': lesson_count, 'assignments': assignments,
               'assignment_count': assignment_count}
    return render(request, 'education/group.html', context)


@allowed_users(allowed_roles=['teacher'])
@login_required(login_url='login')
def create_lesson(request, pk):
    group = Group.objects.get(pk=pk)
    form = LessonForm()
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'education/create_lesson.html', {'group': group, 'form': form})
