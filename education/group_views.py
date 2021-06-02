from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

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
    groups = Group.objects.filter(course=course, language=language, number_of_students__lt=course.max_students)
    if len(groups) == 0:
        group = Group(course=course, language=language)
        group.save()
        group.students.add(student)
        group.save()
        return redirect('home')
    group = groups.first()
    group.students.add(student)
    group.number_of_students = len(group.students.all())
    group.save()
    return redirect('home')


@login_required(login_url='login')
def group_detail(request, pk):
    teacher = None
    if request.user.groups.first() == 'teacher':
        teacher = Teacher.objects.get(user=request.user)
    group = Group.objects.get(pk=pk)
    lessons = Lesson.objects.filter(group=group)
    lesson_count = len(lessons)
    assignments = Assignment.objects.filter(group=group)
    assignment_count = len(assignments)
    context = {'group': group, 'lessons': lessons, 'lesson_count': lesson_count, 'assignments': assignments,
               'assignment_count': assignment_count, 'teacher': teacher}
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
