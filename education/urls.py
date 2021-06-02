"""oq URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from education import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('search/', views.search_page, name='search'),
    path('create_course', views.create_course_page, name="create_course"),
    path('update_course/<int:pk>', views.update_course_page, name="update_course"),
    path('delete_course/<int:pk>', views.delete_course_page, name="delete_course"),
    path('course_detail/<int:pk>', views.course_detail, name="course_detail"),
    path('create_group/<int:course_id>', views.apply_for_course, name="create_group"),
    path('group_detail/<int:pk>', views.group_detail, name="group_detail"),
    path('delete_group/<int:pk>', views.delete_group, name="delete_group"),
    path('create_lesson/<int:pk>', views.create_lesson, name="create_lesson"),
]
