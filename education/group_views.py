from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from accounts.decorators import allowed_users

from accounts.models import Student, Teacher
from education.models import Course, Group, Lesson, Assignment


# this function create new group or adds a new student to existing group
@allowed_users(allowed_roles=['student'])
@login_required(login_url='login')
def apply_for_course(request, course_id):
    student = Student.objects.get(user=request.user)
    course = Course.objects.get(pk=course_id)
    language = request.POST.get('language')
    request.session['course_id'] = course.id
    request.session['student_id'] = student.pk
    request.session['language'] = language
    return redirect(reverse('process'))


@allowed_users(allowed_roles=['teacher'])
@login_required(login_url='login')
def my_groups(request, course_id):
    groups = Group.objects.filter(course_id=course_id)
    return render(request, "education/group/my_groups.html", {'groups': groups})


@login_required(login_url='login')
def group_detail(request, pk):
    teacher = None
    student = None
    group = Group.objects.get(pk=pk)
    lessons = Lesson.objects.filter(group=group)
    if request.user.groups.first().name != 'student':
        teacher = Teacher.objects.get(user=request.user)
        assignments = Assignment.objects.filter(group=group)
    else:
        student = Student.objects.get(user=request.user)
        assignments = Assignment.objects.filter(group=group, student=student)
    assignment_count = len(assignments)
    lesson_count = len(lessons)
    context = {'group': group, 'lessons': lessons, 'lesson_count': lesson_count, 'assignments': assignments,
               'assignment_count': assignment_count, 'teacher': teacher, 'student': student}
    return render(request, 'education/group/group.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def delete_group(request, pk):
    group = Group.objects.get(pk=pk)
    if Teacher.objects.get(user=request.user) != group.course.teacher:
        return redirect('home')
    if request.method == 'POST':
        group.delete()
        return redirect('home')
    return render(request, 'education/group/delete_group.html', {'group': group})
