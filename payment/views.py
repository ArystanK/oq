from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm

from accounts.models import Student
from education.models import Group, Course


@csrf_exempt
def payment_done(request):
    course_id = request.session.get('course_id')
    course = Course.objects.get(id=course_id)
    student_id = request.session.get('student_id')
    student = Student.objects.get(pk=student_id)
    language = request.session.get('language')
    groups = Group.objects.filter(course=course, language=language, number_of_students__lt=course.max_students)
    if len(groups) == 0:
        group = Group(course=course, language=language)
        group.save()
        group.students.add(student)
        group.save()
    group = groups.first()
    group.number_of_students = group.number_of_students + 1
    group.students.add(student)
    group.save()
    return render(request, 'payment/done.html')


@csrf_exempt
def payment_canceled(request):
    return redirect('home')


def payment_process(request):
    course_id = request.session.get('course_id')
    course = Course.objects.get(id=course_id)
    host = request.get_host()
    paypal_teacher_dict = {
        'business': course.teacher.user.username,
        'amount': '%.2f' % course.price,
        'item_name': 'Course {}'.format(course_id),
        'invoice': str(course_id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('done')),
        'cancel_url': 'http://{}{}'.format(host, reverse('canceled'))
    }
    teacher_form = PayPalPaymentsForm(initial=paypal_teacher_dict)
    return render(request, 'payment/process.html', {'course': course, 'teacher_form': teacher_form})
