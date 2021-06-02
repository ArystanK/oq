from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.decorators import allowed_users
from accounts.models import Teacher
from education.forms import LessonForm
from education.models import Group, Lesson


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
    return render(request, 'education/lesson/create_lesson.html', {'group': group, 'form': form})


@login_required(login_url='login')
def lesson_detail(request, pk):
    lesson = Lesson.objects.get(pk=pk)
    return render(request, 'education/lesson/lesson.html', {'lesson': lesson})


@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def delete_lesson(request, pk):
    lesson = Lesson.objects.get(pk=pk)
    if Teacher.objects.get(user=request.user) != lesson.group.course.teacher:
        return redirect('home')
    if request.method == 'POST':
        lesson.delete()
        return redirect('home')
    return render(request, 'education/lesson/delete_lesson.html', {'lesson': lesson})


@allowed_users(allowed_roles=['teacher'])
@login_required(login_url='login')
def update_lesson(request, pk):
    lesson = Lesson.objects.get(pk=pk)
    if Teacher.objects.get(user=request.user) != lesson.group.course.teacher:
        return redirect('home')
    form = LessonForm(instance=lesson)
    teacher_id = lesson.group.course.teacher.pk
    if request.method == "POST":
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('profile')
    context = {'form': form, 'teacher_id': teacher_id, 'lesson': lesson}
    return render(request, "education/lesson/update_lesson.html", context)
