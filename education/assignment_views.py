from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.decorators import allowed_users
from accounts.models import Teacher, Student
from education.forms import CreateAssignmentForm, UpdateAssignmentForm
from education.models import Assignment, Group


@allowed_users(allowed_roles=['teacher'])
@login_required(login_url='login')
def create_assignments(request, pk):
    group = Group.objects.get(pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        task = request.POST.get('task')
        for student in group.students.all():
            assignment = Assignment(title=title, description=description, task=task, student=student, group=group)
            assignment.save()
        return redirect('home')
    return render(request, 'education/assignment/create_assignments.html', {'group': group})


@allowed_users(allowed_roles=['teacher'])
@login_required(login_url='login')
def create_assignment(request, pk):
    group = Group.objects.get(pk=pk)
    form = CreateAssignmentForm()
    students = group.students
    if request.method == 'POST':
        form = CreateAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'education/assignment/create_assignment.html',
                  {'group': group, 'students': students, 'form': form})


@login_required(login_url='login')
def assignment_detail(request, pk):
    assignment = Assignment.objects.get(pk=pk)
    return render(request, 'education/assignment/assignment.html', {'assignment': assignment})


@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def delete_assignment(request, pk):
    assignment = Assignment.objects.get(pk=pk)
    if Teacher.objects.get(user=request.user) != assignment.group.course.teacher:
        return redirect('home')
    if request.method == 'POST':
        assignment.delete()
        return redirect('home')
    return render(request, 'education/assignment/delete_assignment.html', {'assignment': assignment})


@allowed_users(allowed_roles=['teacher'])
@login_required(login_url='login')
def update_assignment(request, pk):
    assignment = Assignment.objects.get(pk=pk)
    group = assignment.group
    students = assignment.group.students
    form = UpdateAssignmentForm(instance=assignment)
    if Teacher.objects.get(user=request.user) != assignment.group.course.teacher:
        return redirect('home')
    if request.method == "POST":
        form = UpdateAssignmentForm(request.POST, instance=assignment)
        form.save()
        return redirect('profile')
    context = {'assignment': assignment, 'students': students, 'form': form, 'group': group}
    return render(request, "education/assignment/update_assignment.html", context)
