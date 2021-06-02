from django.shortcuts import render

from .filters import CourseFilter
from .models import Course


def home_page(request):
    courses = Course.objects.all()[0:4]
    return render(request, "education/home.html", {'courses': courses})


def search_page(request):
    courses = Course.objects.all()
    my_filter = CourseFilter(request.GET, queryset=courses)
    courses = my_filter.qs
    return render(request, "education/search.html", {'my_filter': my_filter, 'courses': courses})
