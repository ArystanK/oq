import django_filters
from django_filters import DateFilter, NumberFilter, CharFilter

from .models import Course


class CourseFilter(django_filters.FilterSet):
    course_name = CharFilter(field_name='course_name', lookup_expr='icontains')
    languages = CharFilter(field_name='languages', lookup_expr='icontains')
    start_date = DateFilter(field_name='start_date', lookup_expr='gte')
    end_date = DateFilter(field_name='end_date', lookup_expr='lte')
    min_num_of_students = NumberFilter(field_name='max_students', lookup_expr='gte')
    max_num_of_students = NumberFilter(field_name='max_students', lookup_expr='lte')
    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Course
        fields = []
